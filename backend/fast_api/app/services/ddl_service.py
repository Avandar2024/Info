# DDL事件服务
import datetime
import json
import re

from sqlmodel import Session, text

from app.settings import MESSAGE_TYPES

# DDL字段映射配置


def safe_json_parse(raw_str, max_retries=3):
	# 安全解析JSON加自动修复
	for _ in range(max_retries):
		try:
			return json.loads(raw_str)
		except json.JSONDecodeError:
			# 去除代码块包裹
			repaired = re.sub(
				r'^.*?```(?:json)?\s*({.*?})\s*```.*$', r'\1', raw_str, flags=re.DOTALL
			)
			# 替换中文引号
			repaired = repaired.replace('"', '"').replace('"', '"')
			# 处理尾随逗号
			repaired = re.sub(r',\s*([}\]])', r'\1', repaired)
			try:
				return json.loads(repaired)
			except Exception as e:
				raw_str = repaired
				print(f'尝试修复JSON格式失败: {str(e)}')

	# 若上述手段都不行，暴力提取第一个完整JSON
	match = re.search(r'\{.*\}', raw_str, flags=re.DOTALL)
	if match is None:
		raise ValueError('找不到有效的JSON内容')
	json_str = match.group()
	return json.loads(json_str)


def generate_ddl_events(session: Session):
	"""从数据库获取5月20日发布的消息并提取DDL信息"""
	target_date = datetime.date(2025, 5, 20)
	ddl_events = []

	# 遍历所有消息类型
	for _, config in MESSAGE_TYPES.items():
		table_name = config['table_name']
		# print(f"正在查询 {table_name} 表...")

		# 构建SQL查询
		query = text(f"""
            SELECT '{config['name']}' AS type, summary, publisher, publish_time, deadline
            FROM {table_name}
            WHERE DATE(publish_time) = :target_date AND deadline IS NOT NULL
        """)

		try:
			result = session.execute(query, {'target_date': target_date})
			# Use a mapping for clarity
			row_mapping = result.mappings().all()
			for item in row_mapping:
				event = {
					'类型': item['type'],
					'消息摘要': item['summary'],
					'发布单位': item['publisher'],
					'发布时间': item['publish_time'],
					'截止时间': item['deadline'],
				}
				ddl_events.append(event)
		except Exception:
			# print(f"An error occurred while querying {table_name}: {e}")
			# print(f"查询{message_type}失败")
			continue

	# 构建符合要求的JSON列表
	formatted_events = [
		{
			'date': target_date.isoformat(),
			'summary': {
				'类型': event['类型'],
				'标题': event['消息摘要'],  # Use '消息摘要' for '标题'
				'截止时间': event['截止时间'],
				# '原文链接': event['原文链接'], # This key is not available
			},
			# 'abstract': event['原文信息']
		}
		for event in ddl_events
	]

	return formatted_events
