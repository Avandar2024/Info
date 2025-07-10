import os
import re
import time

from db_importer import is_url_exists, save_to_database  # 数据库导入函数
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_fixed

from utils.json_util import safe_json_parse  # 安全解析JSON的函数

# 每次调用 api 后休眠时间，避免短时间请求次数过多
SLEEP_TIME = 2

# 配置参数
API_KEY_FILTER = 'sk-******************************'  # 数据清洗的大模型API密钥
API_KEY_STRUCTURING = 'sk-******************************'  # 数据结构化的大模型API密钥
API_URL_FILTER = 'https://dashscope.aliyuncs.com/compatible-mode/v1'
API_URL_STRUCTURING = 'https://dashscope.aliyuncs.com/compatible-mode/v1'
MARKDOWN_PATH = 'C:/Users/ASUS/Desktop/input_example'

# DESTINATION_PATH = "C:/Users/ASUS/Desktop/output"
# 这是经清洗后的文章存放的地址，仅测试使用

# JSON_STORAGE_PATH = "C:/Users/ASUS/Desktop/JSON"
# JSON文件存入路径，仅用于保证代码完整性，整合到数据库导入部分时注释掉

# 数据库配置信息
DB_CONFIG = {
	'host': '47.122.**.**',
	'user': 'user_w',
	'password': '**********',
	'database': 'information_for_students',
	'charset': 'utf8mb4',
}

def extract_and_remove_original_link(content):
	pattern = r'\|原文链接\|:\s*(https?://\S+)'
	match = re.search(pattern, content)
	if match:
		original_link = match.group(1)
		content = re.sub(r'\|原文链接\|:\s*https?://\S+\s*', '', content)
		return original_link, content.strip()
	else:
		print(
			'缺少原文链接或原文链接格式错误。格式必须为：“|原文链接|: http://xxx”或“|原文链接|: https://xxx”'
		)
		return None, content


def extract_and_remove_publish_date(content):
	pattern = r'\|发布日期\|:\s*\d{4}-\d{1,2}-\d{1,2}\s*'
	match = re.search(pattern, content)
	if match:
		date_str = re.search(r'\d{4}-\d{1,2}-\d{1,2}', match.group(0))
		if date_str is None:
			print('发布日期格式错误。格式必须为：“|发布日期|: YYYY-M-D”')
			return None, content
		date_str = date_str.group(0)
		content = re.sub(pattern, '', content)
		return date_str, content.strip()
	else:
		print('缺少发布日期或发布日期格式错误。格式必须为：“|发布日期|: YYYY-M-D”')
		return None, content


# 读取提示词
def read_prompt_file(prompt_type='structuring'):
	"""
	读取指定类型的提示词文件。
	成功则返回文件内容，失败则打印错误并返回 None。
	"""
	prompt_files = {
		'filter': 'prompt_filter.txt',
		'structuring': 'prompt_structuring.txt',
		'summary': 'prompt_summary.txt',
	}
	filename = prompt_files.get(prompt_type)
	if not filename:
		print(f"错误：未知的提示词类型 '{prompt_type}'")
		return None

	try:
		# 假设提示词文件与脚本在同一目录下
		script_dir = os.path.dirname(__file__)
		filepath = os.path.join(script_dir, filename)
		with open(filepath, encoding='utf-8') as f:
			return f.read()
	except FileNotFoundError:
		print(f"错误：提示词文件未找到，请确保 '{filename}' 文件存在于脚本目录中。")
		return None
	except Exception as e:
		print(f"读取提示词文件 '{filename}' 时发生未知错误: {e}")
		return None


@retry(stop=stop_after_attempt(3), wait=wait_fixed(SLEEP_TIME))
def get_structured_data_with_retry(client, messages):
	"""
	调用OpenAI API获取结构化数据，并解析返回的JSON。
	使用装饰器内置了重试逻辑。
	"""
	completion = client.chat.completions.create(
		model='qwen-plus',
		messages=messages,
		temperature=0.1,
		max_tokens=4096,
	)
	raw_output_content = completion.choices[0].message.content
	raw_output = raw_output_content.strip() if raw_output_content else ''
	return safe_json_parse(raw_output)


@retry(stop=stop_after_attempt(3), wait=wait_fixed(SLEEP_TIME))
def get_summary_with_retry(client, messages):
	"""
	调用OpenAI API获取摘要。
	使用装饰器内置了重试逻辑。
	"""
	completion_summary = client.chat.completions.create(
		model='qwen-plus',
		messages=messages,
		temperature=0.1,
		max_tokens=500,
	)
	summary_content = completion_summary.choices[0].message.content
	return summary_content.strip() if summary_content else ''


def analyze_article(content):
	"""分析文章是否有用，处理内部的API调用和提示词读取错误。"""
	try:
		prompt_filter = read_prompt_file('filter')
		if not prompt_filter:
			return False  # 或者根据您的逻辑返回 True

		messages = [
			{'role': 'system', 'content': prompt_filter},
			{'role': 'user', 'content': content},
		]

		client = OpenAI(api_key=API_KEY_FILTER, base_url=API_URL_FILTER)
		completion = client.chat.completions.create(
			model='qwen-plus', messages=messages, temperature=0, max_tokens=10
		)
		time.sleep(SLEEP_TIME)

		# 增加对None的检查
		result_content = completion.choices[0].message.content
		result = result_content.strip() if result_content else ''
		return result.lower() == '有用'

	except Exception as e:
		print(f'分析文章时发生错误 (API_FILTER): {e}')
		return True  # 保持原逻辑，失败时默认视为有用


def process_files_to_db():
	if not os.path.exists(MARKDOWN_PATH):
		print('处理失败\n路径有误')
		return

	# 测试用
	# os.makedirs(DESTINATION_PATH, exist_ok=True)
	# os.makedirs(JSON_STORAGE_PATH, exist_ok=True)

	# 在循环外一次性读取，如果失败则直接终止
	prompt_structuring = read_prompt_file('structuring')
	prompt_summary = read_prompt_file('summary')
	if not all([prompt_structuring, prompt_summary]):
		print('初始化失败，无法读取结构化或摘要提示词，程序终止。')
		return

	for filename in os.listdir(MARKDOWN_PATH):
		if not filename.endswith('.md'):
			# 这不是一个严重错误，只是跳过非Markdown文件
			continue

		filepath = os.path.join(MARKDOWN_PATH, filename)
		print(f'--- 开始处理文件: {filename} ---')

		try:
			with open(filepath, encoding='utf-8') as f:
				original_content = f.read()

			url, content_temp = extract_and_remove_original_link(original_content)
			if url is None or is_url_exists(url, DB_CONFIG):
				print('跳过：URL不存在或已在数据库中。')
				continue

			date, content = extract_and_remove_publish_date(content_temp)
			if date is None:
				print('跳过：缺少发布日期。')
				continue

			if not analyze_article(content):
				print('跳过：文章被分类为无用。')
				continue

			# 数据结构化部分
			messages = [
				{'role': 'system', 'content': prompt_structuring},
				{'role': 'user', 'content': content},
			]
			client = OpenAI(api_key=API_KEY_STRUCTURING, base_url=API_URL_STRUCTURING)

			# 使用带重试逻辑的装饰器函数
			json_data = get_structured_data_with_retry(client, messages)

			# 生成文章摘要
			messages_summary = [
				{'role': 'system', 'content': prompt_summary},
				{'role': 'user', 'content': content},
			]
			summary = get_summary_with_retry(client, messages_summary)
			content = f'|核心摘要: {summary}|\n\n{content}' if summary else content

			# 组合最终数据并存入数据库
			json_data['原文信息'] = content
			json_data['发布日期'] = date
			json_data['原文链接'] = url

			if save_to_database(json_data, DB_CONFIG):
				print(f'成功：文件 {filename} 已导入数据库。')

		except Exception as e:
			# 捕获处理单个文件时发生的所有预料之外的错误
			print(f'严重错误：处理文件 {filename} 时失败，跳过。原因: {e}')
			# 循环将继续处理下一个文件


if __name__ == '__main__':
	process_files_to_db()
