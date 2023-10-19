# C++ 中 Linux 下 Socket 编程

[TOC]

Socket 套接字是网络间不同计算机上的进程通信的一种常用方法，利用三元组（ip地址，协议，端口）就可以唯一标识网络中的进程，网络中的进程通信可以利用这个标志与其它进程进行交互。Socket 也是对 TCP/IP 协议族的一种封装，是应用层与 TCP/IP 协议族通信的中间软件抽象层。

## 1. Socket 基本概念与基本流程

Socket 起源于 Unix ，Unix/Linux 基本哲学之一就是**一切皆文件**，普通文件、目录、硬件设备、进程、管道是文件，Socket 也可以被认为是文件，所以也可以对 Socket 使用文件 I/O 的相关操作，可以用打开(open) –> 读写(read/write) –> 关闭(close)模式来进行操作。

> Unix的另一创新是把磁盘、终端等外围设备都看作文件系统中的文件，磁盘是功能列表中提到的“可拆卸卷”。访问设备的系统调用和访问文件的系统调用是一样的，所以同样的代码既可以操作文件也可以操作设备。
>
> 今天的读者可能很难体会到这一切是做了多大简化之后的结果。早期操作系统中，真实设备的所有复杂情况都会反馈给用户。用户必须知道磁盘名称，了解磁盘的物理结构，如有多少柱面和磁道，以及数据是如何安放在上面。
>
> ——《UNIX传奇：历史与回忆》

Linux 平台下，`socket()` 返回的值被称为文件描述符 fd（File Descriptor），用来唯一标识一个套接字，在 Windows 平台它称为句柄 `handle`。本文用前者的叫法，下文句柄关键字一般用 `fd` 来表示。

套接字的主流程很简单，在服务端下，用 `socket` 创建套接字，使用 `bind` 分配 IP 地址和端口号，`listen` 将套接字转换成可受连接状态，开始监听前面分配的 IP 和端口号，然后调用 `accept` 受理连接请求，使用 `write/read` 来和客户端交换数据，使用 `close` 关闭连接。

客户端下就不需要 `bind` 分配 IP 和端口号，而是由 `connect` 自动分配端口号加上自身的 IP，然后使用 `write/read` 和服务端交换数据，最后 `close` 关闭连接。

![Linux平台下的socket通信](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/cpp-socket%E9%80%9A%E4%BF%A1linux.drawio-20231019-YzDlxj.png)

Windows 平台和 Linux 的差别较小，在创建套接字之前需要调用 `WSAStartUp()`，关闭连接使用 `closesocket()`，关闭连接之后使用 `WSACleanUp()` 注销，其他没差别了，所以在项目中可以很方便地使用通过 `_WIN32_` 宏来判断环境写跨端代码。

![Win平台下的socket通信](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/cpp-socket%E9%80%9A%E4%BF%A1win.drawio-20231019-P18SzD.png)

## 2. 套接字创建

使用 `socket()` 函数创建一个套接字：

```cpp
#include <sys/socket.h>
int socket(int domain, int type, int protocol);
// 创建套接字，返回 文件描述符，失败时返回-1
// domain： 套接字中使用的协议族（Protocol Family）
// type： 套接字数据传输的类型信息
// protocol： 计算机间通信中使用的协议信息
```

常用的套接字创建有两种：

```cpp
int tcpFD = socket(PF_INET, SOCK_STREAM, IPPROTO_TCP);  
int udpFD = socket(PF_INET, SOCK_DGRAM，IPPROTO_UDP);
```

分别解释一下这两行，socket 第一个参数 `PF_INET` 表示是 IPv4 协议族，有时候用 `AF_INET` 宏，`PF` 的意思是 Protocol Family 协议族，`AF` 意为 Address Family，在 `socket.h` 文件中可以看到，其实是同一个值。

![socket.h中的define](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/image-20230824151529147-20230824-3PeJgh.png)

第一个参数还有其他取值 `PF_INET6` 表示 IPv6，`PF_LOCAL` 表示本地协议 UNIX 协议族，这些都不常用，还有其他的就更不常用了。

第二个参数是套接字类型，第三个是协议类型。下面重点介绍一下套接字类型，主要分两种 `SOCK_STREAM` 和 `SOCK_DGRAM`。

### 2.1 `SOCK_STREAM` 面向连接的套接字 TCP

TCP 用**重传机制**（Retransmission）保证数据一定传递到，如果指定时间内未收到某数据包的应答，则会重发来保证数据的完整性。

此外，即使接收方的缓存被填满，数据的传输也不会中断。TCP 会根据接收端的状态来调整数据传输速度，如果接收方的缓存已满，那么发送方将暂时停止发送数据，以防数据丢失。

传输数据没有数据边界，`write` 好几次，可能一次 `read` 就全取出，也可能 `write` 一次，需要 `read` 好几次才取出（粘包问题）。这是因为调用 `write` 函数时，`write` 在数据被移到输出 I/O 缓冲的时候就已经返回了，TCP 协议会保证在适当的时候（不管是分别传送还是一次性传送）传向对方的输入 I/O 缓冲，这时对方调用 `read` 函数会从输入缓冲读取数据。

![TCP套接字的IO缓冲](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/TCP%E5%A5%97%E6%8E%A5%E5%AD%97%E7%9A%84IO%E7%BC%93%E5%86%B2.drawio-20230829-r7UdCu.png)

每个套接字创建时，I/O 缓冲就会自动创建，并且每个套接字中单独存在。即使关闭套接字，输出缓冲中遗留的数据也会继续传递，但输入缓冲中的数据会丢失。

`write` 到输出缓冲区后，TCP 会将内容分段（Segmentation）并封装为 TCP 数据包进行发送。TCP 的封包主要是增加 TCP 首部，一些重要的字段比如 `Win`（窗口）、`Seq`（序列号）、`Len`（数据段长度）、`Ack`（确认号，确认接受到了哪些字节）等等，可以打开 `wireshark` 看一下具体的包。接收方在接收到这些数据包后，重新组装成原始的字节流。

![TCP包](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/image-20230829155648493-20230829-l6GUjX.png)

至于一次传输的数据量大小，则取决于 TCP 的**滑动窗口**（Sliding Window）和**拥塞控制**（Congestion Control），它们可以动态地调整 TCP 数据传输的速度以及窗口大小，以此来实现流量控制并防止网络拥塞。

这样的话，多次传输的数据要如何分辨内容的含义，这个字节是这个包还是那个包的呢？

TCP 确实无法分辨内容的边界，只能保证内容完整并正确地传输到了目的地，而分辨内容的边界只能在应用层协议中做，比如 HTTP 协议就会在头部增加 `content-type`、`content-length` 等字段来帮助对方确定消息的边界，还有校验位等手段来保证消息的可靠性。

总结 TCP 套接字的特点如下：

1. 传输过程中数据不会丢失（协议保证）。
2. 按序传输数据。
3. 传输的数据不存在数据边界。

### 2.2 `SOCK_DGRAM` 面向消息的套接字 UDP

如果说 TCP 是打电话，那么 UDP 就像发短信，短信更方便更快捷，但发出去并不知道对方有没有收到，传输的内容可能丢失也可能损毁，在强调速度的视频实时传输等场景，丢失一部分数据影响并不大，此时一般会使用 UDP。

为了提供可靠的数据传输服务，TCP 在不可靠的网络层（IP 层）进行流控制，而 UDP 就缺少这种流控制机制，而去除握手、挥手、拥塞和窗口控制等等流控制机制之后，TCP 和 UDP 的速度差别并不大，可以说流控制机制是 TCP 的灵魂。

UDP 套接字的特点如下：

1. 强调快速传输而非传输顺序，后发也可能先至。
2. 传输的数据有数据边界，`write` 几次，如果没有丢失的话也就需要 `read` 几次。
3. 限制每次传输的数据大小。
4. 传输的数据可能丢失也可能损毁。


## 3. 基于 TCP 的套接字

### 3.1 分配地址信息 bind

结构体 `sockaddr` 的声明在头文件 `<sys/socket.h>` 中：

```cpp
struct sockaddr {       // in socket.h
	__uint8_t       sa_len;         /* total length */
	sa_family_t     sa_family;      /* [XSI] address family */
	char            sa_data[14];    /* [XSI] addr value (actually smaller or larger) */
};
```

地址和端口信息要存在 `sa_data[]` 这个字节数组中，但直接转换成字节赋值进去很麻烦，所以一般把数据放在 `sockaddr_in` 结构体中，然后在 `bind` 的时候强转一下类型。下面是一个典型的从创建套接字到 `bind` 的使用场景：

```cpp
int sock_fd;
if ((sock_fd = socket(PF_INET, SOCK_STREAM, 0)) == -1) {
  printf("socket() error!");
}

struct sockaddr_in serv_addr;
memset(&serv_addr, 0, sizeof(serv_addr));
serv_addr.sin_family = AF_INET;
serv_addr.sin_addr.s_addr = inet_addr("127.0.0.1");  // ip
serv_addr.sin_port = htons(atoi("9001"));            // port

if (bind(sock_fd, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) == -1) {  // 注意这里的强制转换
  printf("bind() error!");
}
```

这里的 `s_addr` 有时候我们会这样赋值：

```cpp
serv_addr.sin_addr.s_addr = htonl(INADDR_ANY);
```

此处 `INADDR_ANY` 的值为 0，表示任意 IP 地址，所以如果 `s_addr` 设置为 `INADDR_ANY`，意思是这个服务可以接受来自任意网络接口的连接请求。

#### 3.1.1 端口号

端口号是在同一操作系统内为区分不同套接字而设置的，因此无法将一个端口号分配给不同套接字。

端口号 16 位，2 个字节，可分配的端口号范围是 `0-65535`，`0-1023` 一般分配给特定应用程序，所以应当分配此范围之外的值，由于是 2 个字节，所以 `serv_addr.sin_port` 这里需要的就是一个 `USHORT` 数据，对应 `htons` 函数，关于这个函数下面会有解释。

IP 地址 32 位，4 个字节，比如 `255.255.255.255`，每一个 `255` 是一个字节，由于是 4 个字节，所以 `serv_addr.sin_addr.s_addr` 这里需要的就是一个 `unsigned long` 数据，对应 `htonl` 函数，当然这里 `inet_addr` 直接返回的 `unsigned long` 就不用再转换了。

#### 3.1.2 字节序转换

上面典型使用场景中 `htons`、`ntohs`、`htonl`、`ntohl` 这几个字节序转换函数，以 `htons` 为例：

`htons` 的 `h` 代表主机（host）字节序，主机可能是大端序也可能是小端序，不同系统的情况不一样，无论你的主机序是大端序还是小端序，都要加上这个。`htons` 的 `n` 代表网络（network）字节序，网络序一般为大端序。`s` 代表 `short`，`l` 代表 `long`。

所以 `htons` 的意思就是：把 short 数据从网络字节序转化为主机字节序。

另外两个函数 `inet_addr`、`atoi` 还有个 `inet_aton` 也很常用：

1. `inet_addr`：将 `const char*` 的用点号分隔开的十进制 IPv4 地址转换为网络字节序的 `UINT`，失败返回 `INADDR_NONE`。
2. `inet_aton` ：将 `const char*` 的用点号分隔开的十进制 IPv4 地址转换为网络字节序的 `UINT` 并直接写入 `sockaddr_in` 结构体中的 `in_addr`，比如 `inet_aton("127.0.0.1", &serv_addr.sin_addr)`，成功返回 0。
3. `net_ntoa`：与 `inet_aton` 刚好相反，把 `UINT` 转换为 `const char*` 的 IPv4 地址。
4. `atoi`: 将 `const char*` 转换为 `int`。

### 3.2 服务端受理连接并通信 listen/accept

作为服务器，创建 `socket` 并 `bind` 分配地址后，就会使用 `listen` 来监听套接字，套接字进入可发出连接请求的状态，此时还没有受理连接请求。`listen` 函数的第二个参数为连接请求等待队列的长度，表示最多多少个连接请求进入队列。如果等待连接队列已满，新的连接请求可能会被拒绝或丢失，因此需要适当设置等待连接队列的大小。

```cpp
#include <sys/socket.h>
int listen(int serv_sock, int backlog);
// serv_sock: 希望进入等待连接请求状态的套接字文件描述符，传递的描述符套接字参数称为服务端套接字
// backlog: 连接请求等待队列的长度          
```

`listen` 之后，客户端套接字通过 `connect` 就可以进入等待连接队列了，服务端再 `accept` 就可以从等待连接队列中取出一个连接请求进行处理。

```cpp
#include <sys/socket.h>
int accept(int serv_sock, struct sockaddr *clnt_addr, socklen_t *addrlen);
// serv_sock: 服务端套接字的文件描述符
// clnt_addr: 保存发起连接请求的客户端地址信息的变量地址值
// addrlen: 第二个参数的长度
```

如果在没有连接请求的情况下调用 `accept`，`accept` 会阻塞等待客户端连接，当有新的客户端连接发起时，受理连接请求队列中待处理的客户端连接请求，函数调用成功后，`accept` 内部将产生用于数据 I/O 的套接字，并返回其文件描述符，新创建的套接字会继承监听套接字的地址和端口号，并自动与发起连接请求的客户端建立连接。

强调一下，原来的 `socket` 创建的是**监听套接字**，是监听连接请求队列的，而 `accept` 成功返回后的文字描述符是已经和发起连接请求的客户端连接后的**连接套接字**。`accept` 成功返回新的连接套接字后，就可以通过给连接套接字用 `read/write` 向连接的客户端发送和接受数据了，原来的监听套接字仍然处于监听状态。所以服务器同时处理多个连接请求的时候，是每个连接都有自己的套接字独立地进行通信的，服务器可以用这些套接字与不同的客户端进行交互。

所以一个服务端通常只维护一个监听套接字，在这个服务端的生命周期内始终存在，通过该套接字接受多个客户端的连接请求，并为每个连接创建独立的连接套接字，以实现与不同客户端的通信，当服务端与某个客户端完成服务后关闭相对应地连接套接字。这样，服务器可以同时处理多个连接，提高系统的并发性和可扩展性。

### 3.3 客户端发起连接并通信 connect

客户端通过 `socket` 创建套接字后用 `connet` 就可以向服务端发起连接请求了，但需要服务器端 `listen` 进入监听状态后才能 `connect`，此时客户端的连接请求进入到服务端的等待连接队列等待被 `accept` 取用。

```cpp
#include <sys/socket.h>
int connect(int clnt_sock, struct sockaddr *serv_addr, socklen_t addrlen);
// clnt_sock:客户端套接字文件描述符
// serv_addr: 目标服务器端地址信息的变量地址值
// addrlen: 第二个参数的长度
```

客户端套接字的 IP 地址和端口其实也是需要的，但是在调用 `connect` 时操作系统会自动分配，无需调用 `bind` 进行分配。

随后 TCP 建立连接的过程就是三次握手（Three-way Handshaking），断开链接的过程就是四次挥手（Four-way Handshaking）了。

### 3.4 发送与接收数据 write/read

发送与接收数据提供了多组 I/O 函数：

1. `read / write`：向任意文件描述符中读/写数据，只能向已经建立连接的文件描述符中读/写数据。
2. `recv / send`：向任意文件描述符中读/写多个缓冲区的数据，只能向已经建立连接的文件描述符中读/写数据。
3. `readv / writev`： `writev` 将多个散布在不同缓冲区中的数据从`iovec`数组写入到套接字，`readv` 读取多个散布在不同缓冲区中的数据，将其存储到`iovec`数组中的多个缓冲区中。
4. `recvmsg / sendmsg`：`recvmsg` 从套接字中接收数据并存储在 `msghdr` 结构体中，允许接收更多的附加信息，比如控制消息，`sendmsg` 则从 `msghdr` 结构体发信息到套接字中。

这些 I/O 函数具有不同功能，用在不同场景，活学活用。

### 3.5 结束连接 close

类似于关闭文件，在读写操作完成后关闭相应的描述字也是使用 `close`：

```cpp
#include <unistd.h>
int close(int fd);
// 成功时返回 0 ，失败时返回 -1
// fd : 需要关闭的套接字的文件描述符
```

结束链接调用的 `close` 其实就是向服务端发送了 `EOF`。

#### 3.5.1 优雅断开

某些情况下，通信一方单方面的断开套接字连接，显得不太优雅。

比如客户端接收到服务端发的最后消息后还回传一个消息，但此时服务端如果已经 `close` 就会丢失回传的消息。此时就需要只关闭一部分数据交换中使用的流，断开一部分连接指可以传输数据但是无法接收，或可以接受数据但无法传输，称为半关闭 Half-close。

```cpp
#include <sys/socket.h>
int shutdown(int sock, int howto);
// 成功时返回 0 ，失败时返回 -1
// sock: 需要断开套接字文件描述符
// howto: 传递断开方式信息
//     SHUT_RD : 断开输入流，套接字无法接受数据
//     SHUT_WR : 断开输出流，套接字无法传输数据
//     SHUT_RDWR : 同时断开 I/O 流
```
#### 3.5.2 Time-Wait 状态

当使用 TCP 协议进行通信时，其中一方主动关闭连接后，会进入 Time-Wait 状态。在该状态下，该端口在一段时间内不接受新的连接请求。这个时间段通常是两倍的最大段生存时间 MSL（Maximum Segment Lifetime），MSL 的值在不同操作系统中可能有所不同，一般为 30 秒到几分钟。

Time-Wait 状态的持续时间是为了保证网络中所有的剩余数据包都能够传递到目的地或被丢弃，以及确保所有的连接关闭消息都能够传达给对方。在 Time-Wait 状态下，端口会保持开放，以便接收对方可能发送的最后一个确认（ACK）包。这样做可以确保双方都能成功关闭连接，并防止已关闭连接的端口被新的连接误用。此时如果连接，会报 `bind() error` 错，需要等待一段时间之后才可以重新连这个端口。

![](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/image-20230905144451817-20230905-JkCOh2.png)

Time-Wait 不仅存在于服务器端，不管是服务器端还是客户端，先断开连接的套接字必然会有 Time-Wait。但客户端 Time-Wait 并没有多少感知，因为客户端每次都会动态分配端口号，因此无需过多关注 Time-Wait 状态。

通常，Time-Wait 状态对网络应用的正常运行没有太大影响，但如果服务器需要频繁地关闭和重新打开连接，Time-Wait 可能会导致端口资源的消耗。此时可以通过调整操作系统的参数来缩短 Time-Wait 状态的持续时间，或设置重用地址 `SO_REUSEADDR` 参数来更好地管理端口资源。

```cpp
setsockopt(serv_sock, SOL_SOCKET, SO_REUSEADDR, (void*)&option, optlen);
```

### 3.6 TCP 服务端实现

在客户端读到什么就原样发回去的实现：

```cpp
#include <arpa/inet.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

#define BUF_SIZE 1024
void error_handling(char *message) {
  fputs(message, stderr);
  fputc('\n', stderr);
  exit(1);
}

int main(int argc, char *argv[]) {
  int serv_sock, clnt_sock;
  char message[BUF_SIZE];
  int str_len, i;

  struct sockaddr_in serv_adr, clnt_adr;
  socklen_t clnt_adr_sz;

  serv_sock = socket(PF_INET, SOCK_STREAM, 0);      // 创建套接字
  if (serv_sock == -1)  error_handling("socket() error");

  memset(&serv_adr, 0, sizeof(serv_adr));
  serv_adr.sin_family = AF_INET;                   // ipv4
  serv_adr.sin_addr.s_addr = htonl(INADDR_ANY);    // 监听任意地址的请求
  serv_adr.sin_port = htons(atoi("60001"));        // 端口号

  if (bind(serv_sock, (struct sockaddr *)&serv_adr, sizeof(serv_adr)) == -1) // 分配地址
    error_handling("bind() error");

  if (listen(serv_sock, 5) == -1)     // 开始监听
    error_handling("listen() error");

  clnt_adr_sz = sizeof(clnt_adr);
  
  // 调用 5 次 accept 函数，共为 5 个客户端提供服务
  for (i = 0; i < 5; i++) {
    clnt_sock = accept(serv_sock, (struct sockaddr *)&clnt_adr, &clnt_adr_sz);   // 受理连接
    if (clnt_sock == -1) error_handling("accept() error");
    else printf("Connect client %d : %s \n", i + 1, inet_ntoa(clnt_adr.sin_addr));

    while ((str_len = read(clnt_sock, message, BUF_SIZE)) != 0) {    // 读到消息就处理
      printf("Message : %s   from client %s \n", message, inet_ntoa(clnt_adr.sin_addr));
      write(clnt_sock, message, str_len);   // 把读的发回去
    }
    close(clnt_sock);    // 别忘了关
  }
  close(serv_sock);      // 别忘了关
  return 0;
}
```

### 3.7 TCP 客户端实现

一个输入什么就发送什么的简单 TCP 客户端最小实现：

```cpp
// 头部参考 3.6 节的代码
int main(int argc, char *argv[]) {
  int sock, str_len;
  char message[BUF_SIZE];
  struct sockaddr_in serv_adr;

  sock = socket(PF_INET, SOCK_STREAM, 0);      // 创建
  if (sock == -1)
    error_handling("socket() error");

  memset(&serv_adr, 0, sizeof(serv_adr)); 
  serv_adr.sin_family = AF_INET;                       // ipv4
  serv_adr.sin_addr.s_addr = inet_addr("127.0.0.1");   // 在本地起一个客户端
  serv_adr.sin_port = htons(atoi("60001"));            // 端口号

  if (connect(sock, (struct sockaddr *)&serv_adr, sizeof(serv_adr)) == -1)    // 客户端发起链接
    error_handling("connect() error!");
  else puts("Connected...........");

  while (1) {
    fputs("Input message(Q to quit): ", stdout);  // 打印啥发送啥
    fgets(message, BUF_SIZE, stdin);              // 从终端读

    if (!strcmp(message, "q\n") || !strcmp(message, "Q\n")) // 输入Q就退出
      break;

    write(sock, message, strlen(message));       // 写
    str_len = read(sock, message, BUF_SIZE - 1); // 读
    message[str_len] = 0;
    printf("Message from server: %s", message);
  }
  close(sock);    // 别忘了关
  return 0;
}
```

## 4. 基于 UDP 的套接字

由于 UDP 是无连接的传输协议，所以基于 UDP 的套接字无需经过连接过程，包括 `listen`、`accept`、`connect`，只需要创建套接字，然后就可以发送和接收消息了。

UDP 不同于 TCP，不存在谁 `listen` 或者谁是 `connect` 一方，因此在某种意义上无法明确区分服务器端和客户端。

### 4.1 发送与接收数据 sendto/recvfrom

创建好 TCP 套接字以后，传输数据时无需加上地址信息。因为 TCP 套接字将保持与对方套接字的连接。换言之，TCP 套接字知道目标地址信息。但 UDP 套接字不会保持连接状态（UDP 套接字只有简单的邮筒功能），因此每次传输数据时都需要添加目标的地址信息。这相当于寄信前在信件中填写地址。

```cpp
#include <sys/socket.h>
ssize_t sendto(int sock, void *buff, size_t nbytes, int flags,
               struct sockaddr *to, socklen_t addrlen);
// 向目标地址发送UDP信息，成功时返回传输的字节数，失败是返回 -1
// sock: 用于传输数据的 UDP 套接字
// buff: 保存待传输数据的缓冲地址值
// nbytes: 待传输的数据长度，以字节为单位
// flags: 可选项参数，若没有则传递 0
// to: 存有目标地址的 sockaddr 结构体变量的地址值
// addrlen: 传递给参数 to 的地址值结构体变量长度

ssize_t recvfrom(int sock, void *buff, size_t nbytes, int flags,
                 struct sockaddr *from, socklen_t *addrlen);
// 读取某地址信息发送过来的UDP信息，成功时返回传输的字节数，失败是返回 -1
// sock: 用于接收数据的UDP套接字文件描述符
// buff: 保存接收数据的缓冲地址值
// nbytes: 可接收的最大字节数，故无法超过参数buff所指的缓冲大小
// flags: 可选项参数，若没有则传递 0
// from: 结果参数，存有发送端地址信息的 sockaddr 结构体变量的地址值
// addrlen: 保存参数 from 的结构体变量长度的变量地址值。
```

所有套接字都应分配 IP 地址和端口，只是直接分配还是自动分配的区别，TCP 和 UDP 的服务端需要 `bind` 一个本地的端口（地址一般用 `INADDR_ANY`），TCP 客户端套接字是在调用 `connect` 函数时自动分配 IP 和端口号，而 UDP 的客户端一般在首次调用 `sendto` 的时候会给套接字自动分配 IP （主机 IP）和端口，分配的 IP 和端口号会保留到程序结束。

![cpp-socket通信linux_udp](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/cpp-socket%E9%80%9A%E4%BF%A1linux_udp.drawio-20230905-L02C1f.png)

与 TCP 发送多次一次就可以接收到不同，UDP 里 `sendto` 发送几次，就需要调用几次 `recvfrom`。

### 4.2 已连接 UDP 套接字

TCP 套接字中需注册待传传输数据的目标 IP 和端口号，而在 UDP 中无需注册。因此通过 `sendto` 函数传输数据的过程大概可以分为以下 3 个阶段：

- 第 1 阶段：向 UDP 套接字注册目标 IP 和端口号
- 第 2 阶段：传输数据
- 第 3 阶段：删除 UDP 套接字中注册的目标地址信息。

每次调用 `sendto` 函数时重复上述过程，每次使用都变更目标地址，因此可以重复利用同一 UDP 套接字向不同目标传递数据。要与同一主机进行长时间通信时，将 UDP 套接字变成已连接套接字会节约第 1 和第 3 阶段的时间，从而提高整体性能。

与 TCP 类似，UDP 套接字默认没调用 `connect` 就属于未连接套接字，没有注册目标地址信息。反之，注册了目标地址的套接字称为**已连接套接字** `connected`。

使用 `connect` 函数后，并不会建立像 TCP 那样的可靠连接，UDP 仍然是无连接的，只是向 UDP 套接字注册目标 IP 和端口信息，绑定了默认的地址。如果不 `connect`，则需要在每次 `sendto` 时指定目标地址和端口，在 `recvfrom` 时获取数据的源地址信息。

`connect` 之后就与 TCP 套接字一致，每次调用 `sendto` 函数时只需传递信息数据。因为已经指定了默认的收发地址信息，所以不仅可以使用 `sendto`、`recvfrom` 函数，还可以使用 `write`、`read`，这两个函数相比前者，少了每次调用时传入指定目标地址参数，使用的是 `connect` 指定的默认地址。

### 4.3 UDP 服务端实现

```cpp
// 头部参考 3.6 节的代码
int main(int argc, char *argv[]) {
  int serv_sock, str_len;
  char message[BUF_SIZE];
  socklen_t clnt_adr_sz;

  struct sockaddr_in serv_adr, clnt_adr;

  // socket 的第二个参数传递 SOCK_DGRAM
  serv_sock = socket(PF_INET, SOCK_DGRAM, 0);
  if (serv_sock == -1)
    error_handling("UDP socket creation eerror");

  memset(&serv_adr, 0, sizeof(serv_adr));
  serv_adr.sin_family = AF_INET;                 // ipv4
  serv_adr.sin_addr.s_addr = htonl(INADDR_ANY);  // 接受任意地址的请求
  serv_adr.sin_port = htons(atoi("60001"));      // 端口号
  // 分配地址接受数据，不限制数据传输对象
  if (bind(serv_sock, (struct sockaddr *)&serv_adr, sizeof(serv_adr)) == -1)   // 绑定地址信息
    error_handling("bind() error");

  while (1) {
    clnt_adr_sz = sizeof(clnt_adr);
    str_len = recvfrom(serv_sock, message, BUF_SIZE, 0, (struct sockaddr *)&clnt_adr, &clnt_adr_sz);  // 读
    printf("Received data: %s from:%s\n", message, inet_ntoa(clnt_adr.sin_addr));
    
    // 通过上面的函数调用同时获取数据传输端的地址，利用该地址进行逆向重传
    sendto(serv_sock, message, str_len, 0, (struct sockaddr *)&clnt_adr, clnt_adr_sz);
  }
  close(serv_sock);    // 别忘了关
  return 0;
}
```

### 4.4 UDP 客户端实现

一个输入什么就发送什么的简单 UDP 客户端最小实现：

```cpp
// 头部参考 3.6 节的代码
int main(int argc, char *argv[])
{
    int sock, str_len;
    char message[BUF_SIZE];
    socklen_t adr_sz;

    struct sockaddr_in serv_adr, from_adr;

    sock = socket(PF_INET, SOCK_DGRAM, 0);    // 创建 UDP 套接字
    if (sock == -1)
        error_handling("socket() error");

    memset(&serv_adr, 0, sizeof(serv_adr));
    serv_adr.sin_family = AF_INET;                   // ipv4
    serv_adr.sin_addr.s_addr = inet_addr("0.0.0.0"); // 本地起客户端
    serv_adr.sin_port = htons(atoi("60001"));        // 端口号

    while (1) {
        fputs("Insert message(q to quit): ", stdout);
        fgets(message, sizeof(message), stdin);
        if (!strcmp(message, "q\n") || !strcmp(message, "Q\n"))
            break;
        // 向服务器传输数据，自动给自己分配IP地址和端口号
        sendto(sock, message, strlen(message), 0,
               (struct sockaddr *)&serv_adr, sizeof(serv_adr));
        adr_sz = sizeof(from_adr);
        str_len = recvfrom(sock, message, BUF_SIZE, 0, (struct sockaddr *)&from_adr, &adr_sz);
        message[str_len] = 0;
        printf("Message from server: %s", message);
    }
    close(sock);    // 别忘了关
    return 0;
}
```

## 5. 域名和 IP 互转（DNS）

DNS（Domain Name System） 是对 IP 地址和域名进行相互转换的系统。比如向一个域名发起请求后，首先会去向上一级的 DNS 服务器去查询，通过这种方式逐级向上传递信息，一直到达根服务器，它知道应该向哪个 DNS 服务器发起询问。再向下传递解析请求，得到 IP 地址候原路返回，最后会将解析的IP地址传递到发起请求的主机。

使用下面两个函数可将域名转化为 IP，或者将 IP 转化为域名，返回的信息在 `hostent` 结构体中。

```cpp
#include <netdb.h>
struct hostent *gethostbyname(const char *hostname);
// 域名转IP。成功时返回 hostent 结构体地址，失败时返回 NULL 指针

struct hostent *gethostbyaddr(const char *addr, socklen_t len, int family);
// IP转域名。成功时返回 hostent 结构体变量地址值，失败时返回 NULL 指针
// addr: 含有IP地址信息的 in_addr 结构体指针。为了同时传递 IPV4 地址之外的全部信息，该变量的类型声明为 char 指针
// len: 向第一个参数传递的地址信息的字节数，IPV4时为 4 ，IPV6 时为16.
// family: 传递地址族信息，ipv4 是 AF_INET ，IPV6是 AF_INET6
```

关于 `socket` 编程的更多内容，比如多线程服务器端、`epoll` 等，我们将在下一篇文章里继续讨论。


***

网上的帖子大多深浅不一，甚至有些前后矛盾，在下的文章都是学习过程中的总结，如果发现错误，欢迎留言指出，如果本文帮助到了你，别忘了点赞支持一下哦，你的点赞是我更新的最大动力！\~

> 参考文档：
>
> 1.  [TCP/IP网络编程](https://book.douban.com/subject/25911735/)

PS：本文收录在在下的博客 [Github - SHERlocked93/blog](https://github.com/SHERlocked93/blog) 系列文章中，欢迎大家关注我的公众号 `CPP下午茶`，直接搜索即可添加，持续为大家推送 CPP 以及 CPP 周边相关优质技术文，共同进步，一起加油\~

另外可以加入「前端下午茶交流qun」，vx 搜索  `sherlocked_93` 加我，备注 **1**，我拉你～