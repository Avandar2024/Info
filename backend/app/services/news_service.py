# 新闻服务
import datetime

from sqlmodel import Session, text

from app.settings import MESSAGE_TYPES

# API配置
# API_KEY = "sk-*****************************************"
# API_URL = "https://api.siliconflow.cn/v1/chat/completions"
# SLEEP_TIME = 7  # API调用间隔时间


def generate_daily_news(session: Session):  # -> dict[str, Any] | list[dict[str, Any]]:
	"""从数据库获取2025年5月20日的所有消息并返回格式化的新闻摘要"""
	target_date = datetime.date(2025, 5, 20)

	# 收集所有类型的更新
	all_messages = []
	# 创建应用上下文

	# 遍历所有消息类型
	for _, config in MESSAGE_TYPES.items():
		table_name = config['table_name']
		# 构建查询SQL，直接查询所需字段
		query = text(
			f'SELECT `类型`, `标题`, `关键词`, `原文信息`, `原文链接` '
			f'FROM `{table_name}` WHERE `发布日期` = :target_date'
		)
		try:
			# 执行查询
			result = session.execute(query, {'target_date': target_date})
			rows = result.mappings().all()

			# 处理查询结果
			for row in rows:
				message = {
					'类型': row['类型'],
					'标题': row['标题'],
					'关键词': row['关键词'],
					'原文信息': row['原文信息'],
					'原文链接': row['原文链接'],
				}
				all_messages.append(message)
		except Exception:
			# print(f"查询{message_type}失败")
			continue

	# 如果没有数据，返回默认消息
	if not all_messages:
		return {'date': target_date.isoformat(), 'summary': [], 'abstract': []}

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

	abstract = [msg['原文信息'] for msg in all_messages]

	# 为每条消息生成独立JSON对象
	news_list = [
		{'date': target_date.isoformat(), 'summary': item, 'abstract': abstract[i]}
		for i, item in enumerate(summary)
	]

	return news_list
