#!/usr/bin/env python3
"""
FastAPI应用启动脚本
使用uvicorn服务器运行FastAPI应用
"""

import uvicorn

from .app.fastapi_app import create_fastapi_app


def main():
	"""启动FastAPI应用"""
	app = create_fastapi_app()

	# 开发环境配置
	uvicorn.run(
		app,
		host='0.0.0.0',
		port=5000,
		reload=True,  # 开发环境启用热重载
		log_level='info',
	)


if __name__ == '__main__':
	main()
