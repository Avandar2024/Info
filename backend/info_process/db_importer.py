# 导入数据库的函数
from sqlmodel import Session, create_engine, select

from .models import model_map


def get_engine(db_config):
	# 从db_config字典创建数据库引擎
	user = db_config.get('user')
	password = db_config.get('password')
	host = db_config.get('host')
	port = db_config.get('port', 3306)
	db = db_config.get('db')
	charset = db_config.get('charset', 'utf8mb4')
	return create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{db}?charset={charset}')


def save_to_database(json_data, db_config):
	engine = get_engine(db_config)

	table_name = json_data.get('类型')
	if not table_name or table_name not in model_map:
		raise ValueError(f'无效的类型或类型未在model_map中定义: {table_name}')

	model_class = model_map[table_name]

	# 清理和转换数据
	processed_data = {}
	for key, value in json_data.items():
		if value in ['无', '']:
			processed_data[key] = None
		elif isinstance(value, list):
			processed_data[key] = ' '.join(map(str, value)) if value else None
		else:
			processed_data[key] = value

	# 创建模型实例
	db_item = model_class(**processed_data)

	with Session(engine) as session:
		try:
			session.add(db_item)
			session.commit()
			return True
		except Exception as e:
			session.rollback()
			raise RuntimeError(f'数据库错误: {e}') from e


def is_url_exists(url, db_config):
	# 检查url是否已经存在，防止重复导入
	if url is None:
		return False

	engine = get_engine(db_config)
	with Session(engine) as session:
		for table_name, model_class in model_map.items():
			try:
				statement = select(model_class).where(model_class.原文链接 == url)
				result = session.exec(statement).first()
				if result:
					print('避免1个文件重复导入')
					return True
			except Exception as e:
				print(f'查询表 {table_name} 失败: {e}')
				continue
	return False
