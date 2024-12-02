from flask import Flask, render_template, jsonify
from flask_caching import Cache
import random
import os

app = Flask(__name__)

# 配置缓存
cache = Cache(app, config={'CACHE_TYPE': 'simple'})  # 这里可以选择不同的缓存类型，如 Redis 或 Memcached

# 配置图片文件夹路径
IMG_FOLDER = os.path.join('static', 'img')
app.config['IMG_FOLDER'] = IMG_FOLDER

# flag内容
Flag = os.getenv("GZCTF_FLAG")

def get_random_image():
    """从img文件夹中随机获取一张图片"""
    try:
        images = [f for f in os.listdir(IMG_FOLDER) if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        if images:
            return random.choice(images)
        return None
    except Exception as e:
        print(f"Error getting random image: {e}")
        return None

@app.route('/')
def index():
    """渲染主页"""
    return render_template('index.html')

@app.route('/draw')
@cache.cached(timeout=60)  # 缓存响应，设置为 60 秒
def draw():
    """处理抽卡请求"""
    # 设置抽中flag的概率为0.1%
    if random.random() < 0.001:
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
