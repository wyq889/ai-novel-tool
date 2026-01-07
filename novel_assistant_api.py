import requests
import json

# 配置基础信息（替换为你自己的 api_key）
BASE_URL = "https://api.deepseek.com"
API_KEY = "sk-0974d18972c543419b645f6dfbf278cb"  # 这里替换成你的真实 API Key

def call_deepseek_api(prompt):
    """
    调用 DeepSeek API 进行对话
    :param prompt: 你的提问内容
    :return: API 返回的回答内容
    """
    # 接口完整地址（对话接口）
    url = f"{BASE_URL}/v1/chat/completions"
    
    # 请求头（必须包含 API Key 和内容类型）
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # 请求体（按 DeepSeek 接口要求构造参数）
    data = {
        "model": "deepseek-chat",  # 使用的模型名称
        "messages": [
            {"role": "user", "content": prompt}  # 用户的提问
        ],
        "temperature": 0.7,  # 回答的随机性，0-1 之间
        "stream": False  # 非流式返回
    }
    
    try:
        # 发送 POST 请求
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # 检查请求是否成功
        
        # 解析返回结果
        result = response.json()
        answer = result["choices"][0]["message"]["content"]
        return answer
    
    except Exception as e:
        return f"调用失败：{str(e)}"

# 测试调用
if __name__ == "__main__":
    question = "请解释一下 Python 中的列表推导式"
    answer = call_deepseek_api(question)
    print("DeepSeek 回答：\n", answer)
