import json
import re

from tenacity import retry, stop_after_attempt, wait_fixed


@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
def safe_json_parse(raw_str):
	# 安全解析JSON加自动修复
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
		raise AttributeError('No JSON found')
	json_str = match.group()
	return json.loads(json_str)
