# 安装依赖：pip install openai flask flask-cors
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

# 初始化Flask应用
app = Flask(__name__)
# 解决跨域问题
CORS(app)

# 初始化DeepSeek客户端
client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),  # 从环境变量获取API Key
    base_url="https://api.deepseek.com"
)

# 定义提示词模板，适配不同的小说生成需求
PROMPT_TEMPLATES = {
    "beginning": "请根据以下灵感，生成一个精彩的小说开头（300-500字），语言生动有画面感：{input_text}",
    "continue": "请根据以下故事灵感和已有内容，续写后续情节（400-600字），情节连贯且有吸引力：\n【灵感】{input_text}\n【已有内容】{output_text}",
    "characters": "请根据以下故事灵感，生成详细的人物设定（至少3个核心人物），包含姓名、年龄、身份、性格、外貌、能力/特点：{input_text}",
    "highlights": "请根据以下故事灵感，构思5个以上的剧情爽点，每个爽点简要说明（50字左右），符合网文爽点逻辑：{input_text}"
}

@app.route('/generate_novel', methods=['POST'])
def generate_novel():
    """处理小说生成请求的接口"""
    try:
        # 获取前端传递的参数
        data = request.get_json()
        action_type = data.get('action_type')  # 生成类型：beginning/continue/characters/highlights
        input_text = data.get('input_text', '').strip()
        output_text = data.get('output_text', '').strip()

        # 参数校验
        if not action_type or action_type not in PROMPT_TEMPLATES:
            return jsonify({"success": False, "message": "无效的生成类型"}), 400
        if not input_text:
            return jsonify({"success": False, "message": "请输入故事灵感"}), 400
        # 续写功能需要已有内容
        if action_type == "continue" and not output_text:
            return jsonify({"success": False, "message": "请先生成开头后再续写"}), 400

        # 构造提示词
        if action_type == "continue":
            prompt = PROMPT_TEMPLATES[action_type].format(input_text=input_text, output_text=output_text)
        else:
            prompt = PROMPT_TEMPLATES[action_type].format(input_text=input_text)

        # 调用DeepSeek API
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一个专业的小说创作助手，擅长写网文、短篇小说，语言风格生动有吸引力，严格按照用户要求的字数和格式生成内容。"},
                {"role": "user", "content": prompt},
            ],
            stream=False,
            temperature=0.8,  # 创意度，0-1之间，越高越有创意
            max_tokens=2000   # 最大生成字数
        )

        # 提取生成的内容
        result = response.choices[0].message.content.strip()

        # 返回成功结果
        return jsonify({
            "success": True,
            "content": result
        })

    except Exception as e:
        # 捕获异常并返回错误信息
        return jsonify({
            "success": False,
            "message": f"生成失败：{str(e)}"
        }), 500

if __name__ == '__main__':
    # 启动服务，默认端口5000
    app.run(host='0.0.0.0', port=5000, debug=True)
