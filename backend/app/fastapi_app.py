# FastAPI应用程序工厂函数
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.db import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
	"""应用程序生命周期管理"""
	# 启动时创建数据库表
	create_db_and_tables()
	yield
	# 关闭时的清理工作（如果需要）


def create_fastapi_app() -> FastAPI:
	"""FastAPI应用程序工厂函数"""
	app = FastAPI(
		title='南京大学信息聚合平台API',
		description='提供新闻聚合、DDL管理、知识问答等功能的API服务',
		version='1.0.0',
		lifespan=lifespan,
	)

	# 启用CORS以支持跨域请求
	app.add_middleware(
		CORSMiddleware,
		allow_origins=['http://47.115.222.10:80', 'http://localhost:3000'],  # 添加开发环境支持
		allow_credentials=True,
		allow_methods=['*'],
		allow_headers=['*'],
	)

	# 添加会话中间件
	app.add_middleware(
		SessionMiddleware,
		secret_key='your_secret_key_here',  # 生产环境中请使用复杂且保密的密钥
		max_age=3600,  # 会话有效期为1小时
		same_site='lax',
		https_only=True,  # 生产环境启用
	)

	# 注册路由
	from routes.fastapi_routes import router as api_router

	app.include_router(api_router, prefix='/api')

	return app


# 创建应用实例供导入使用
def get_app():
	"""获取FastAPI应用实例"""
	return create_fastapi_app()
