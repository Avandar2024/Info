from http import HTTPStatus

from dashscope import Application

response = Application.call(
	api_key='sk-abf733f33ea64dcd9362d96bcfb77b6f',
	app_id='7c8a24304e1f4f4e943d4472904294de',  # 替换为实际的应用 ID
	prompt='我最近想参加一些志愿活动有什么推荐的吗',
)  # 记得改成你想要问的问题

if response.status_code != HTTPStatus.OK:
	print(f'request_id={response.request_id}')
	print(f'code={response.status_code}')
	print(f'message={response.message}')
	print('请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code')
else:
	print(response.output.text)
