from flask import Flask, render_template, jsonify,make_response,request
import jwt
import datetime
import random
import os

app = Flask(__name__)

# 配置图片文件夹路径
IMG_FOLDER = os.path.join('static', 'img')
app.config['IMG_FOLDER'] = IMG_FOLDER
key="secret"
# flag内容
Flag = os.getenv("GZCTF_FLAG")

def get_random_image():
    """从img文件夹中随机获取一张图片"""
    try:
        images = [f for f in os.listdir(IMG_FOLDER) if f.endswith(('.png'))]
        if images:
            return random.choice(images)
        return None
    except Exception as e:
        print(f"Error getting random image: {e}")
        return None

@app.route('/')
def index():
    payload={
        "role":"guest"
    }
    token = jwt.encode(payload, key, algorithm="HS256")
    if isinstance(token, bytes):
        token = token.decode('utf-8')
    response = make_response(render_template('index.html'))
    response.set_cookie(
        'jwt', 
        token,
        max_age=3600,
        httponly=True,    # 防止 JavaScript 访问
        samesite='Lax'    # 防止 CSRF 攻击
    )
    return response

@app.route('/draw')
def draw():
    """处理抽卡请求"""
    token = request.cookies.get('jwt')
    if not token:
        return jsonify({"message": "缺少 JWT Cookie"}), 401
    try:
        # 解码 JWT
        payload = jwt.decode(token, key, algorithms='HS256')
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "JWT 已过期"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "无效的 JWT"}), 401
    # 设置抽中flag的概率为0.1%
    if payload['role']=='vv':
        prob=1
    else :
        prob=0
    if random.random() < prob:
        result = {
            'type': 'flag',
            'message': Flag,
            'image': None  # 不需要图片
        }
    else:
        image = get_random_image()
        result = {
            'type': 'normal',
            'message': '罗德岛干员+1',
            'image': image if image else 'default.png'
        }
    return jsonify(result)

if __name__ == '__main__':
    # 确保必要的文件夹存在
    os.makedirs(IMG_FOLDER, exist_ok=True)
    app.run(host='0.0.0.0', port=8000, debug=True)