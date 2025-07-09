# 日期查询服务
import datetime
import re

import pendulum
from sqlmodel import Session, text

from ..db import user_engine
from ..models.user import User
from ..settings import MESSAGE_TYPES


def generate_date_data(
	session: Session, target_date_str: str, user_id: int | None = None
) -> dict:
	"""
    根据指定日期生成新闻和DDL事件数据

    参数:
		session: SQLModel会话对象
        target_date_str: 日期字符串，格式为'YYYY-MM-DD'
        user_id: 用户ID, 可选

    返回:
        包含新闻和DDL事件的字典
    """
	# example of result_data:
	# {
	#     'date': '2025-05-20',
	#     'news': [
	#         {
	#             'date': '2025-05-20',
	#             'summary': {
	#                 '类型': '学术讲座',
	#                 '标题': '人工智能与未来教育发展论坛',
	#                 '关键词': 'AI, 教育创新, 未来发展',
	#                 '原文链接': 'https://www.nju.edu.cn/events/ai-forum-2025'
	#             },
	#             'abstract': '南京大学人工智能学院将于2025年5月20日举办...'
	#         }
	#     ],
	#     'ddl_events': [
	#         {
	#             'date': '2025-05-20',
	#             'summary': {
	#                 '类型': '讲座/分享会信息',
	#                 '标题': '2025春季校园招聘宣讲会',
	#                 '截止时间': '2025-05-25 18:00:00',
	#                 '原文链接': 'https://www.nju.edu.cn/events/career-talk-2025'
	#             }
	#         }
	#     ]
	# }
	try:
		# 解析日期字符串
		target_date = datetime.datetime.strptime(target_date_str, '%Y-%m-%d').date()

		# 获取用户自定义DDL
		user_ddls = []
		print(f'[DEBUG] User ID from parameter: {user_id}')  # 添加调试日志
		if user_id:
			with Session(user_engine) as user_session:
				user = user_session.get(User, user_id)
				if user and user.custom_ddls:
					for ddl in user.custom_ddls:
						ddl_date = datetime.datetime.strptime(
							ddl['date'].split('T')[0], '%Y-%m-%d'
						).date()
						# 检查DDL日期是否在target_date及其后5天内
						if target_date <= ddl_date <= target_date + datetime.timedelta(
							days=5
						):
							# 将 'YYYY-MM-DDTHH:MM:SS' 转为 'YYYY-MM-DD HH:MM:SS'
							formatted_ddl_time = ddl['date'].replace('T', ' ')
							user_ddls.append(
								{
									'date': ddl['date'].split('T')[0],
									'summary': {
										'类型': '用户自定义',
										'标题': ddl['content'],
										'截止时间': formatted_ddl_time,
									},
								}
							)

		# 修改news_service和ddl_service中的函数调用，传入目标日期
		news_data = generate_news_by_date(target_date, session)

		# 获取未来5天的DDL事件
		ddl_data = []
		for i in range(6):  # 包括目标日期和之后5天
			current_date = target_date + datetime.timedelta(days=i)
			ddl_data.extend(generate_ddl_by_date(current_date, session))

		# 将用户自定义DDL放在ddl_events的开头
		ddl_data = user_ddls + ddl_data

		# 构建返回数据
		return {
			'date': target_date.isoformat(),
			'news': news_data,
			'ddl_events': ddl_data,
		}
	except ValueError:
		# 日期格式错误
		return {
			'date': target_date_str,
			'news': [],
			'ddl_events': [],
			'error': '日期格式错误，请使用YYYY-MM-DD格式',
		}
	except Exception as e:
		# 其他错误
		return {
			'date': target_date_str,
			'news': [],
			'ddl_events': [],
			'error': f'查询失败: {str(e)}',
		}


def generate_news_by_date(target_date: datetime.date, session: Session) -> list:
    """
    根据指定日期生成新闻数据

    参数:
        target_date: datetime.date对象
        session: SQLModel会话对象

    返回:
        新闻数据列表
    """
    # 收集所有类型的更新
    all_messages = []

    # 遍历所有消息类型
    for _, config in MESSAGE_TYPES.items():
        table_name = config['table_name']
        # 构建查询SQL，直接查询所需字段
        query = text(
            f"""
            SELECT "类型", "标题", "关键词", "原文信息", "原文链接"
            FROM {table_name} WHERE "发布日期" = :target_date
            """
        )
        try:
            # 执行查询
            result = session.execute(query, {'target_date': target_date})
            rows = result.fetchall()

            # 处理查询结果
            for row in rows:
                message = {
                    '类型': row[0],
                    '标题': row[1],
                    '关键词': row[2],
                    '原文信息': row[3],
                    '原文链接': row[4],
                }
                all_messages.append(message)
        except Exception:
            # print(f"查询失败")
            continue

    # 如果没有数据，返回空列表
    if not all_messages:
        return []

    # 格式化消息内容
    summary = [
        {
            '类型': msg['类型'],
            '标题': msg['标题'],
            '关键词': msg['关键词'],
            '原文链接': msg['原文链接'],
        }
        for msg in all_messages
    ]

    # 提取第一个||之间的内容作为摘要
    abstract = []
    for msg in all_messages:
        content = msg['原文信息']
        # 修改正则表达式以匹配单竖线 |
        match = re.search(r'\|([^|]*)\|', content)
        extracted_content = match.group(1) if match else content
        extracted_content = re.sub(r'(\*\*.*?\*\*)(?!\s)', r'\1 ', extracted_content)
        # 移除"核心摘要: "前缀
        if extracted_content.startswith('核心摘要: ##'):
            extracted_content = extracted_content[len('核心摘要: ##') :]
        abstract.append(extracted_content)

    # 为每条消息生成独立JSON对象
    news_list = [
        {'date': target_date.isoformat(), 'summary': item, 'abstract': abstract[i]}
        for i, item in enumerate(summary)
    ]

    return news_list


def generate_ddl_by_date(target_date: datetime.date, session: Session) -> list:
    """
    根据指定日期生成DDL事件数据

    参数:
        target_date: datetime.date对象
        session: SQLModel会话对象

    返回:
        DDL事件数据列表
    """
    ddl_events = []

    # 遍历所有消息类型
    for _, config in MESSAGE_TYPES.items():
        table_name = config['table_name']
        date_column = config.get('date_column')

        # 如果没有日期列，则跳过
        if not date_column:
            continue

        # 构建查询，只选择必要的字段
        query = text(
            f"""
            SELECT "类型", "标题", "原文信息", "原文链接", "{date_column}"
            FROM {table_name}
            WHERE DATE("{date_column}") = :target_date AND "{date_column}" IS NOT NULL
            """
        )

        try:
            result = session.execute(query, {'target_date': target_date})
            rows = result.fetchall()

            for row in rows:
                # 将row转换为可修改的列表
                row_list = list(row)
                deadline = row_list[4]  # 截止时间在第5个位置

                # 格式化截止时间
                if isinstance(deadline, datetime.datetime):
                    formatted_deadline = deadline.strftime('%Y-%m-%d %H:%M:%S')
                elif isinstance(deadline, str):
                    try:
                        # 使用pendulum解析，并格式化为标准格式
                        dt_obj = pendulum.parse(deadline)
                        if isinstance(dt_obj, pendulum.DateTime):
                            formatted_deadline = dt_obj.in_timezone(
                                'Asia/Shanghai'
                            ).strftime('%Y-%m-%d %H:%M:%S')
                        else:
                            formatted_deadline = str(dt_obj)
                    except Exception:
                        formatted_deadline = deadline  # 解析失败则保留原样
                else:
                    formatted_deadline = str(deadline)

                # 创建事件字典
                event = {
                    '类型': row_list[0],
                    '标题': row_list[1],
                    '原文信息': row_list[2],
                    '原文链接': row_list[3],
                    '截止时间': formatted_deadline,
                }
                ddl_events.append(event)
        except Exception:
            # print(f"查询失败: {e}")
            continue

    # 构建符合要求的JSON列表
    formatted_events = [
        {
            'date': target_date.isoformat(),
            'summary': {
                '类型': event['类型'],
                '标题': event['标题'],
                '截止时间': event['截止时间'],
                '原文链接': event['原文链接'],
            },
        }
        for event in ddl_events
    ]

    return formatted_events
