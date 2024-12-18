## 终极谜语人

*Misc ? (Week 2)*, by EZForever

### 题目描述

无论怎么测量都是1:4:9的完美石碑，「其中」篆刻着不可言宣的至高奥义……

本题要找的不是flag，而是十二个两字词语，共24个汉字。在游戏里找到之后~~点击这里~~使用`get_flag.htm`计算flag。

~~服务器地址：`xxx.xxx.xxx.xxx:xxxxx`~~（地图见`RTCTF24H2.7z`），MC版本：1.20.6

**flag格式：`r00t{%32x}`**

*提示：这道题不是Web也不是逆向，不要试着去分析那个计算flag的网页（逆不出来的，不要浪费时间）。*

### 解析

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

### 花絮

这道题的点子来自week1弃坑的MC题的备用点子（人话：废案的废案）：用一块基岩挡住flag的一部分，让玩家们使出全身解数想办法看到基岩挡住的部分；结果week1的游戏题出完了之后谜语人之魂发作，想着“不能破坏的方块上记录着众人的终极追求”这一概念很有神秘感，多整了一堆活，就变成了这么一道题。新的题目名称“终极谜语人”~~除了在说出题人实在不柿个好人钠之外~~更是在指代题目中的神秘元素。

（不指望有人能看出的）预告图和题目中的梗是出自小说/电影《2001：太空漫游》的[黑方碑](https://2001.fandom.com/wiki/Monolith)，MC地图的环境布置也是在模拟TMA-0和TMA-1两块黑方碑的周遭环境（To ~~群萌新~~ 滑稽：自定义维度令主世界使用末地生物群系且地表Y<0，就能创造天上有太阳、四周有光亮但天是黑色的奇景）。看不懂也没关系，这个梗和做题一点关系都没有就是了（

