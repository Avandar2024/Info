# DDL事件服务
import datetime

from sqlmodel import Session, text

from app.settings import MESSAGE_TYPES

# DDL字段映射配置


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
