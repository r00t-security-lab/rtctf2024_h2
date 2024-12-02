from flask import Flask, render_template, jsonify, request
import random,os
from datetime import datetime

app = Flask(__name__)

# 存储用户的比赛时间
game_times = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_questions', methods=['GET'])
def get_questions():
    questions = []
    answers = []
    
    for _ in range(10):
        num1 = random.randint(1, 20)
        num2 = random.randint(1, 20)
        questions.append(f"{num1} ? {num2}")
        
        if num1 > num2:
            answers.append(">")
        elif num1 < num2:
            answers.append("<")
        else:
            answers.append("=")
    
    return jsonify({
        "questions": questions,
        "answers": answers
    })

@app.route('/start_game', methods=['POST'])
def start_game():
    user_id = request.remote_addr
    game_times[user_id] = datetime.now()
    return jsonify({"status": "success"})

@app.route('/end_game', methods=['POST'])
def end_game():
    user_id = request.remote_addr
    if user_id in game_times:
        start_time = game_times[user_id]
        end_time = datetime.now()
        time_diff = (end_time - start_time).total_seconds()
        
        del game_times[user_id]
        
        if time_diff < 2.0:
            flag_value = os.environ.get("GZCTF_FLAG", "default_flag_value")
            return jsonify({
                "time": time_diff,
                "flag": flag_value
            })
        return jsonify({
            "time": time_diff,
            "flag": None
        })
    return jsonify({"error": "No game in progress"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8800, debug=True)