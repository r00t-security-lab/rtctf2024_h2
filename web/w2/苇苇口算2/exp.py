import requests
import time

BASE_URL = "http://124.222.157.100:32932/"  # 修改为你的服务器地址

# 启动游戏
def start_game():
    response = requests.post(f"{BASE_URL}/start_game")
    if response.status_code == 200:
        print("Game started successfully.")
    else:
        print("Failed to start the game.")
        exit(1)

# 获取问题
def get_question():
    for _ in range(3):  # 尝试3次获取问题
        response = requests.get(f"{BASE_URL}/get_question")
        if response.status_code == 200:
            data = response.json()
            if "question" in data:
                return data.get("question")
            else:
                time.sleep(0.1)  # 如果获取问题失败，等待0.1秒再试
    print("Failed to get question after 3 attempts.")
    exit(1)

# 提交答案
def submit_answer(answer):
    response = requests.post(f"{BASE_URL}/submit_answer", json={"answer": answer})
    if response.status_code == 200:
        data = response.json()
        print(data)
        return data
    else:
        print("Failed to submit answer.")
        exit(1)

# 自动答题脚本
def auto_play():
    start_game()
    correct_count = 0

    while correct_count < 10:
        question = get_question()
        if question:
            # 解析题目
            num1, _, num2 = question.split()
            num1, num2 = int(num1), int(num2)

            # 计算答案
            if num1 > num2:
                answer = ">"
            elif num1 < num2:
                answer = "<"
            else:
                answer = "="

            # 提交答案并获取结果
            result = submit_answer(answer)
            if result.get("status") == "correct":
                correct_count += 1
                print(f"Answered correctly: {correct_count}/10")
            elif result.get("status") == "incorrect":
                print("Incorrect answer, game over.")
                break
        time.sleep(0.1)  # 确保不会太快以防服务器压力过大


if __name__ == "__main__":

    auto_play()
