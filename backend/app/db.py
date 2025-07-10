# 数据库模型和交互
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

from app.settings import SQLALCHEMY_DATABASE_URI, USER_DATABASE_URI

# 创建主数据库引擎
engine = create_engine(
	SQLALCHEMY_DATABASE_URI,
	poolclass=StaticPool,
	connect_args={'check_same_thread': False} if 'sqlite' in SQLALCHEMY_DATABASE_URI else {},
	echo=True,  # 开发环境显示SQL语句，生产环境可设为False
)

# 创建用户数据库引擎
user_engine = create_engine(
	USER_DATABASE_URI,
	poolclass=StaticPool,
	connect_args={'check_same_thread': False} if 'sqlite' in USER_DATABASE_URI else {},
	echo=True,
)


def create_db_and_tables():
	"""创建数据库表"""
	SQLModel.metadata.create_all(engine)
	SQLModel.metadata.create_all(user_engine)


def get_session():
	"""获取数据库会话"""
	with Session(engine) as session:
		yield session


def get_user_session():
	"""获取用户数据库会话"""
	with Session(user_engine) as session:
		yield session


def init_app(app):
	"""使用应用初始化数据库"""
	# 在应用启动时创建表
	with app.app_context():
		create_db_and_tables()

	# 将引擎添加到应用配置中，方便其他地方使用
	app.config['DB_ENGINE'] = engine
	app.config['USER_DB_ENGINE'] = user_engine
