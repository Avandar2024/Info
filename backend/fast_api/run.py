# Entry point for running the FastAPI backend application
import uvicorn

from .app.fastapi_app import create_fastapi_app

if __name__ == '__main__':
	app = create_fastapi_app()
	uvicorn.run(app, host='0.0.0.0', port=5000, reload=True)
