from flask import Flask, render_template, jsonify, request
import random,os
from datetime import datetime

app = Flask(__name__)

# 存储用户的比赛时间和题目进度
game_sessions = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_question', methods=['GET'])
def get_question():
    user_id = request.remote_addr
    if user_id not in game_sessions:
        return jsonify({"error": "No game in progress"}), 400

    current_question = game_sessions[user_id]['current_question']
    if current_question >= 10:
        return jsonify({"error": "All questions answered"}), 400

    num1 = random.randint(1, 20)
    num2 = random.randint(1, 20)
    question = f"{num1} ? {num2}"
    answer = ">" if num1 > num2 else "<" if num1 < num2 else "="

    game_sessions[user_id]['questions'].append((question, answer))
    return jsonify({"question": question})

@app.route('/start_game', methods=['POST'])
def start_game():
    user_id = request.remote_addr
    game_sessions[user_id] = {
        'start_time': datetime.now(),
        'current_question': 0,
        'questions': []
    }
    return jsonify({"status": "success"})

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    user_id = request.remote_addr
    if user_id not in game_sessions:
        return jsonify({"error": "No game in progress"}), 400

    data = request.json
    user_answer = data.get('answer')

    current_question = game_sessions[user_id]['current_question']
    if current_question >= 10:
        return jsonify({"error": "All questions answered"}), 400

    correct_answer = game_sessions[user_id]['questions'][current_question][1]
    if user_answer == correct_answer:
        game_sessions[user_id]['current_question'] += 1
        if game_sessions[user_id]['current_question'] == 10:
            end_time = datetime.now()
            time_diff = (end_time - game_sessions[user_id]['start_time']).total_seconds()
            del game_sessions[user_id]
            if time_diff < 2.0:
                flag_value = os.environ.get("GZCTF_FLAG", "default_flag_value")
                return jsonify({
                    "time": time_diff,
                    "flag": flag_value,
                    "message": "你赢了!"
                })
            return jsonify({
                "time": time_diff,
                "flag": None,
                "message": "太慢了！"
            })
        return jsonify({"status": "correct"})
    else:
        del game_sessions[user_id]
        return jsonify({"status": "incorrect", "message": "怎么回事！！这都能错"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8800, debug=True)
