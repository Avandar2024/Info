# FastAPI路由
from http import HTTPStatus
from typing import Any

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlmodel import Session, select

from ..db import user_engine
from ..models.user import User
from ..services.date_query_service import generate_date_data
from ..services.mcp_query_function import get_query_progress
from ..services.query_service import query_by_question

# 创建路由器
router = APIRouter()


# Pydantic模型用于请求验证
class RegisterRequest(BaseModel):
	username: str
	password: str


class LoginRequest(BaseModel):
	username: str
	password: str


class CustomDDLRequest(BaseModel):
	content: str
	date: str | None = None


class UnsubscribedAccountsRequest(BaseModel):
	accounts: list[str]


class KnowledgeQueryRequest(BaseModel):
	question: str
	model: str = 'RAG'


# 依赖注入：获取数据库会话
def get_db_session():
	with Session(user_engine) as session:
		yield session


# 创建依赖注入工厂函数
db_dependency = Depends(get_db_session)


# 统一的响应格式函数
def api_response(
	data: Any = None, message: str = 'Success', code: int = 200, errors: Any = None
) -> JSONResponse:
	"""统一的API响应格式"""
	response_data = {'code': code, 'message': message, 'data': data}
	if errors:
		response_data['errors'] = errors

	return JSONResponse(
		content=response_data, status_code=200 if code == 200 else (400 if code < 500 else 500)
	)


@router.post('/register')
async def register(request_data: RegisterRequest, request: Request, db: Session = db_dependency):
	"""用户注册"""
	# 检查用户名是否已存在
	statement = select(User).where(User.username == request_data.username)
	existing_user = db.exec(statement).first()
	if existing_user:
		return api_response(message='用户名已存在', code=400)

	# 创建新用户
	user = User(username=request_data.username)
	user.set_password(request_data.password)

	try:
		db.add(user)
		db.commit()
		db.refresh(user)  # 刷新以获取生成的ID
		return api_response(data=user.to_dict(), message='注册成功')
	except Exception as e:
		db.rollback()
		return api_response(message='注册失败', code=500, errors=str(e))


@router.post('/login')
async def login(request_data: LoginRequest, request: Request, db: Session = db_dependency):
	"""用户登录"""
	# 查找用户
	statement = select(User).where(User.username == request_data.username)
	user = db.exec(statement).first()
	if not user or not user.check_password(request_data.password):
		return api_response(message='用户名或密码错误', code=401)

	try:
		# 设置会话
		request.session['user_id'] = user.id
		return api_response(data=user.to_dict(), message='登录成功')
	except Exception as e:
		return api_response(message='登录失败', code=500, errors=str(e))


@router.post('/custom-ddl')
async def add_custom_ddl(
	request_data: CustomDDLRequest, request: Request, db: Session = db_dependency
):
	"""添加自定义DDL"""
	user_id = request.session.get('user_id')
	if not user_id:
		return api_response(message='请先登录', code=401)

	user_obj = db.get(User, user_id)
	if not user_obj:
		return api_response(message='请先登录', code=401)

	try:
		user_obj.add_custom_ddl(request_data.content, request_data.date)
		db.add(user_obj)
		db.commit()
		db.refresh(user_obj)

		return api_response(data=user_obj.to_dict(), message='添加自定义DDL成功')
	except Exception as e:
		db.rollback()
		return api_response(message='添加自定义DDL失败', code=500, errors=str(e))


@router.delete('/custom-ddl/{index}')
async def remove_custom_ddl(index: int, request: Request, db: Session = db_dependency):
	"""删除自定义DDL"""
	user_id = request.session.get('user_id')
	if not user_id:
		return api_response(message='请先登录', code=401)

	current_user = db.get(User, user_id)
	if not current_user:
		return api_response(message='请先登录', code=401)

	try:
		current_user.remove_custom_ddl(index)
		db.add(current_user)
		db.commit()
		db.refresh(current_user)

		return api_response(data=current_user.to_dict(), message='删除自定义DDL成功')
	except Exception as e:
		db.rollback()
		return api_response(message='删除自定义DDL失败', code=500, errors=str(e))


@router.put('/unsubscribed-accounts')
async def update_unsubscribed_accounts(
	request_data: UnsubscribedAccountsRequest, request: Request, db: Session = db_dependency
):
	"""更新用户不想看的公众号列表"""
	user_id = request.session.get('user_id')
	if not user_id:
		return api_response(message='请先登录', code=401)

	current_user = db.get(User, user_id)
	if not current_user:
		return api_response(message='请先登录', code=401)

	try:
		current_user.update_unsubscribed_accounts(request_data.accounts)
		db.add(current_user)
		db.commit()
		db.refresh(current_user)

		return api_response(data=current_user.to_dict(), message='更新订阅公众号成功')
	except ValueError as e:
		return api_response(message=str(e), code=400)
	except Exception as e:
		db.rollback()
		return api_response(message='更新订阅公众号失败', code=500, errors=str(e))


@router.get('/date-query')
async def query_by_date(date: str):
	"""根据日期获取新闻和DDL事件"""
	try:
		if not date:
			return api_response(message='日期参数不能为空', code=400)

		# 调用日期查询服务
		result_data = generate_date_data(date)

		# 检查是否有错误
		if 'error' in result_data:
			return api_response(result_data, message=result_data['error'], code=400)

		return api_response(result_data, message='查询成功')
	except Exception as e:
		print(f'日期查询失败: {str(e)}')
		return api_response(message='日期查询失败，请稍后重试', code=500)


@router.post('/knowledge/query')
async def knowledge_query(request_data: KnowledgeQueryRequest):
	"""知识库问答"""
	try:
		result = query_by_question(request_data.question, request_data.model)
		# 如果返回结果包含错误信息
		if isinstance(result, dict) and 'code' in result and result['code'] != HTTPStatus.OK:
			return api_response(result, message=result['message'])
		# 这里直接返回queryId，不等待处理完成
		return api_response(data=result)
	except Exception as e:
		print(f'知识查询失败: {str(e)}')
		return api_response(message='知识查询失败，请稍后重试', code=500)


@router.get('/query-progress/{query_id}')
async def query_progress(query_id: str):
	"""获取查询进度"""
	progress_info = get_query_progress(query_id)
	return api_response(data=progress_info, message='Success')


@router.get('/check-login')
async def check_login(request: Request, db: Session = db_dependency):
	"""检查登录状态"""
	user_id = request.session.get('user_id')
	if user_id:
		user = db.get(User, user_id)
		if user:
			return api_response(data=user.to_dict(), message='已登录')
	return api_response(message='未登录', code=401)


@router.post('/logout')
async def logout(request: Request):
	"""用户登出"""
	try:
		request.session.clear()  # 清除所有会话数据
		return api_response(message='登出成功')
	except Exception as e:
		return api_response(message='登出失败', code=500, errors=str(e))


@router.get('/docs')
async def api_docs():
	"""返回API文档"""
	from ..settings import MESSAGE_TYPES

	docs = {
		'api_version': '1.0',
		'base_url': '/api',
		'description': '南京大学信息聚合平台API文档',
		'message_types': {
			'description': '系统支持的消息类型',
			'types': list(MESSAGE_TYPES.keys()),
		},
		'response_format': {
			'description': '所有API响应都遵循以下统一格式',
			'schema': {
				'code': '状态码，200表示成功，其他值表示错误',
				'message': '响应消息，用于描述请求结果',
				'data': '响应数据，具体格式参见各接口说明',
				'errors': '错误详情，仅在发生错误时出现',
			},
		},
		'endpoints': [
			{
				'path': '/api/register',
				'method': 'POST',
				'description': '用户注册',
				'content_type': 'application/json',
				'request_body': {'username': '用户名', 'password': '密码'},
				'responses': {
					'200': {
						'description': '注册成功',
						'schema': {
							'id': '用户ID',
							'username': '用户名',
						},
					},
					'400': {'description': '请求参数错误或用户名已存在'},
					'500': {'description': '服务器错误'},
				},
			},
			# 可以继续添加其他端点的文档
		],
	}
	return api_response(docs)
