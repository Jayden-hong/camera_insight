import os
import io
import base64
from PIL import Image
import requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import traceback


# 初始化
app = Flask(__name__, static_folder='static')
CORS(app)
load_dotenv()

# API配置
SILICONFLOW_API_URL = "https://api.siliconflow.cn/v1/chat/completions"
STEPFUN_API_URL = "https://api.stepfun.com/v1/chat/completions"

# 从环境变量获取API密钥
SF_API_KEY = os.getenv("SILICONFLOW_API_KEY")
STEPFUN_API_KEY = os.getenv("STEPFUN_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# 模型配置
QWEN_MODEL = "Qwen/Qwen2.5-VL-32B-Instruct"
STEPFUN_MODEL = "step-1o-turbo-vision"

def file_to_webp_base64(file_storage):
    file_storage.seek(0)
    img = Image.open(file_storage)
    out_bytes = io.BytesIO()
    img.convert("RGB").save(out_bytes, format="WEBP")
    out_bytes = out_bytes.getvalue()
    return base64.b64encode(out_bytes).decode("utf-8")

print(">>> Flask 服务启动成功，当前 PID:", os.getpid())
print("=== 这是我想要的 app.py ===", flush=True)

# 添加根路由，返回前端页面
@app.route("/")
def index():
    return send_from_directory('static', 'index.html')

@app.route("/test", methods=["GET"])
def test():
    print(">>> /test 路由被访问", flush=True)
    return jsonify({"status": "ok", "message": "API服务正常运行"})

@app.route("/analyze_camera", methods=["POST"])
def analyze_camera():
    print("==== 收到 /analyze_camera 请求 ====", flush=True)
    
    # 获取请求参数
    camera_image = request.files.get("camera_image")
    map_image = request.files.get("map_image")
    prompt = request.form.get("prompt", "").strip()
    model = request.form.get("model", "qwen").strip()
    
    print("request.files:", request.files)
    print("camera_image:", camera_image)
    print("map_image:", map_image)
    print("prompt:", prompt[:100] + "..." if len(prompt) > 100 else prompt)
    print("model:", model)
    
    # 参数验证
    if not (camera_image and map_image and prompt):
        print("参数不全，返回400")
        return jsonify({"error": "Missing input"}), 400

    # 图片处理
    try:
        camera_b64 = file_to_webp_base64(camera_image)
        map_b64 = file_to_webp_base64(map_image)
        print("图片转base64成功")
    except Exception as e:
        print("图片处理失败：")
        print(traceback.format_exc())
        return jsonify({"error": f"图片处理失败: {str(e)}"}), 500

    # 根据模型选择API配置
    if model == "stepfun":
        if not STEPFUN_API_KEY:
            return jsonify({"error": "STEPFUN_API_KEY 环境变量未设置"}), 500
            
        payload = {
            "model": STEPFUN_MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/webp;base64,{map_b64}",
                                "detail": "high"
                            }
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/webp;base64,{camera_b64}",
                                "detail": "high"
                            }
                        },
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ],
            "stream": False,
            "max_tokens": 1024,
            "temperature": 0.5,
            "response_format": {"type": "text"}
        }
        headers = {
            "Authorization": f"Bearer {STEPFUN_API_KEY}",
            "Content-Type": "application/json"
        }
        api_url = STEPFUN_API_URL
        print("使用阶跃星辰API")
        
    else:  # 默认使用Qwen
        if not SF_API_KEY:
            return jsonify({"error": "SILICONFLOW_API_KEY 环境变量未设置"}), 500
            
        payload = {
            "model": QWEN_MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/webp;base64,{map_b64}",
                                "detail": "high"
                            }
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/webp;base64,{camera_b64}",
                                "detail": "high"
                            }
                        },
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ],
            "stream": False,
            "max_tokens": 1024,
            "temperature": 0.5,
            "response_format": {"type": "text"}
        }
        headers = {
            "Authorization": f"Bearer {SF_API_KEY}",
            "Content-Type": "application/json"
        }
        api_url = SILICONFLOW_API_URL
        print("使用Qwen API")

    print("API URL:", api_url)
    print("请求头已设置")

    # 调用AI API
    try:
        resp = requests.post(api_url, headers=headers, json=payload, timeout=60)
        print("API响应状态：", resp.status_code)
        print("API响应内容：", resp.text[:500] + "..." if len(resp.text) > 500 else resp.text)
        
        resp.raise_for_status()
        data = resp.json()
        
        result = ""
        if "choices" in data and data["choices"]:
            result = data["choices"][0]["message"].get("content", "")
        else:
            result = str(data)
            
        return jsonify({"success": True, "result": result, "raw": data})
        
    except requests.exceptions.Timeout:
        print("平台接口超时")
        return jsonify({"error": "平台接口超时，请稍后重试"}), 504
    except requests.exceptions.RequestException as e:
        print("平台API请求失败：", str(e))
        return jsonify({"error": "平台API请求失败", "detail": str(e)}), 500
    except Exception as e:
        print("后端服务异常：")
        print(traceback.format_exc())
        return jsonify({"error": "后端服务异常", "detail": str(e)}), 500


if __name__ == "__main__":
    # 获取端口，适配部署环境
    port = int(os.environ.get("PORT", 5001))
    debug = os.environ.get("FLASK_ENV", "production") == "development"
    
    print(f"启动Flask应用，端口: {port}, 调试模式: {debug}")
    app.run(host="0.0.0.0", port=port, debug=debug)