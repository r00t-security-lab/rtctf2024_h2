from flask import Flask, render_template, request, render_template_string
import re
import os

app = Flask(__name__)
app.secret_key = os.urandom(32)

# 设置黑名单
BLACKLIST = [
    "config", "self", "class", "mro", "arg", 
    "warn", "system",
    "os", "subprocess", "eval", "exec",
    "\\", "&", "|", ";", "`", "request", "open",
    "chr", "ord","flag"
]

def waf(s):
    s = s.lower()
    for word in BLACKLIST:
        if word in s:
            return True
    return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/divine', methods=['POST'])
def divine():
    question = request.form.get('question', '')
    
    if waf(question):
        return render_template('divine.html', 
                             prediction="⚠️ 邪恶的能量干扰了预言，大预言家需要休息...",
                             error=True)
    
    template = '''
    <div class="prophecy-result">
        <div class="mystic-symbols">✧･ﾟ: *✧･ﾟ:* </div>
        <div class="crystal-ball">
            <img src="/static/img/crystal.png" alt="crystal" class="crystal-img">
        </div>
        <div class="oracle-speaks">预言之灵说：</div>
        <div class="prophecy-content">%s</div>
        <div class="mystic-symbols">*:･ﾟ✧*:･ﾟ✧</div>
        <div class="oracle-signature">— 来自虚空的回响 —</div>
    </div>
    ''' % question
    
    try:
        result = render_template_string(template)
        return render_template('divine.html', prediction=result)
    except:
        return render_template('divine.html', 
                             prediction="🌌 预言之力过于强大，水晶球暂时无法承载...",
                             error=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)