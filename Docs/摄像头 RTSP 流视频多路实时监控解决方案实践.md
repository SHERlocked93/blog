# 摄像头 RTSP 流视频多路实时监控解决方案实践

本文记录我在摄像头 RTSP 流视频多路实时监控项目里，落地的一套「多路 RTSP 低延迟播放」方案的全过程：从选型、编码、到Web/桌面端播放与硬解优化。

## 一、需求现状

现场有一个远程监控端，需要同时监控多台车载设备的摄像头画面，每台设备约 6 路摄像头，摄像头输出 RTSP（视频 H.264；部分摄像头型号还有音频），由于是车载实时摄像头，关键的不是能播，而是多路、低延迟（由于在现场操作需要实时反馈，所以需要 1 秒以内）、低 CPU 占用，因此核心需求可以总结成四点：

1. 多路并发：同屏 6+ 路播放，最多一个监控端同时播放 12 路视频;
2. 低延迟：操作链路希望接近实时（目标 < 500ms 级）;
3. 桌面端：需要有编码控制能力，最好 Qt 桌面程序;
4. 性能与稳定性：客户端需要稳定走 GPU 硬解，否则多路全走 CPU 软解解码会被拖死；
5. 部署/运维复杂度：比如要更换视频流接入的时候要足够方便，最好能配置后一键部署；

## 二、技术选型

经过一番调研，主要有下面几个方案：

### HLS

HLS 的核心思路是把连续视频切成一段段 TS 分片（segment），服务器创建并动态更新一个 .m3u8 播放列表文件，这个文件里记录了所有 .ts 视频切片的文件名、顺序、时长等信息，客户端按 m3u8 索引列表去拉分片播放。它的优点是兼容性很好，所有现代浏览器和操作系统都原生支持，适合普通直播、点播和 CDN 分发。

在一个 TS 分片没有播完并同步到 m3u8 之前，客户端是无法看到最新画面的。这天生决定了 HLS 的实时性不高，一般在 3 秒以上，加上各个链路的延迟和缓冲，总延迟轻松到达 10 秒左右，这对于实时监控是完全不可接受的。

### HTTP-FLV

HTTP-FLV 通常是服务器将音视频数据用 FLV（Flash Video）格式进行封装，通过客户端和服务端建立的 HTTP 长连接流式传输到播放器上，延迟在 1-3s，可以满足一定的实时性需求。缺点是需要前端引入 flv.js 之类的 JS 库在 JS 层对 FLV 流解封装成 H.264、音频等数据，尤其在多路并发时，CPU 占用会比较高，且浏览器对 FLV 的支持不如 HLS/WebRTC 原生。

### 海康 WebSDK 的 WebSocket

海康的 WebSDK 提供了基于 WebSocket 的视频流传输能力，延迟可以做到 1 秒以内，适合海康设备的接入，但我看有些老一些的海康设备可能不支持 WebSocket，而且 WebSDK 要求 Chrome 版本不低于 91，如果你的摄像头都支持 WebSocket 且能保证浏览器的 chromium 内核版本在 91+，那么这个方式也是可行的。

### WebRTC

WebRTC（Web Real-Time Communication）是目前实时音视频通信的主流技术，现代浏览器（Chrome, Firefox, Safari 等）都原生支持 WebRTC 协议栈，无需安装插件，实时性通常能做到 500ms 左右，非常适合对实时性要求高的监控场景。WebRTC 的设计目标就是实时通话与互动，浏览器对其实现非常成熟。对于 H.264 等常见编码格式，浏览器能直接调用 GPU 进行硬件加速解码，显著降低 CPU 占用。

## 三、核心实践：通过 SRS 将 RTSP + H.264 视频流转封装为 WebRTC + H.264

我最终使用 SRS（Simple Realtime Server）开源流媒体服务器，一直在稳定维护，也有不少用到生产级环境的案例，文档有中文，部署也比较简单，直接 docker 拉一个镜像然后一行命令就能启动，另外它自带视频流录制功能，后期做录制也方便。

在远程监控服务器上用 Docker 部署 SRS，把摄像头 RTSP 拉到本机后，再以 WebRTC 的方式提供给前端播放。

这里要强调一个关键点：尽量做转封装（Remux），避免转码（Transcode），摄像头已经输出 RTSP 包着的 H.264 服务器只需要转协议成 WebRTC 包着 H.264 即可，不需要重新编码，转码会带来很大的 CPU 负担和延迟。

整体思路：摄像头推流 RTSP(H.264) ，经过 SRS ingest 拉流并通过 rtmp_to_rtc 转封装为 WebRTC(H.264) ，前端浏览器用 `<video>` 播放。

### 3.1 SRS 核心配置解析

SRS 的配置文件 `srs.conf` 是核心。下面用一个最小配置片段：

```nginx
listen 1935;
max_connections 1000;
daemon off;
srs_log_tank file;
srs_log_file /usr/local/srs/objs/logs/srs.log;

rtc_server {
    enabled on;           # 启用 RTC 服务器
    listen 8000;          # WebRTC UDP 端口
    candidate $CANDIDATE; # 自动获取服务器 IP
}

http_server {
    enabled on;            # 启用 HTTP 服务器
    listen 8080;
    dir ./objs/nginx/html; # 默认打开是控制台，也可以改为自己的前端页面
    crossdomain on;
}

vhost __defaultVhost__ {
    rtc {
        enabled on;     # 启用 RTC 功能
        rtmp_to_rtc on; # 开启 RTMP 到 RTC 的转换
        nack on;        # 开启丢包重传
        twcc on;        # 开启拥塞控制
    }

    ingest camera_RIG001_0 {      # 定义 Ingest 拉流配置，主动拉取摄像头 RTSP 流
        enabled on;
        input {
            type stream;
            url rtsp://admin:password@192.168.1.60:554/Streaming/Channels/101;  # 你摄像头的rtsp地址
        }
        ffmpeg ./objs/ffmpeg/bin/ffmpeg; # 使用 SRS 内置的 FFmpeg
        engine {
            enabled on;
            perfile {
                rtsp_transport tcp;
                fflags nobuffer;
                flags low_delay;
                probesize 32;
                analyzeduration 0;
                max_delay 0;
            }
            vcodec copy; # 视频流直接复制，不转码
            acodec copy; # 音频流直接复制，我将摄像头的音频输出格式配为 AAC
            output rtmp://127.0.0.1:[port]/live/camera_RIG001_0?vhost=[vhost];
        }
    }
}
```

### 3.2 Docker 一键配置

由于现场设备的 IP 和摄像头数量可能会变化，手动修改 `srs.conf` 比较繁琐且容易出错。我做了一套自动化配置流程：

1. 配置文件：提供一个 JSON 文件，维护用户摄像头的 IP/Port 列表。
2. 生成脚本：读取摄像头列表，生成 `srs.conf`，并在上一部配置变更时更新文件。
3. 自动重启：检测到配置变更后，执行 `docker restart srs` 让配置生效。

Docker 命令：

```bash
# 拉取 SRS 镜像并打标签
docker pull registry.cn-hangzhou.aliyuncs.com/ossrs/srs:5
docker tag registry.cn-hangzhou.aliyuncs.com/ossrs/srs:5 ossrs/srs:5

# 运行 SRS 容器
docker run -d --name srs \
   --restart=always \
    -p 1935:1935 \
    -p 1985:1985 \
    -p 8080:8080 \
    -p 8000:8000/udp \
    -e CANDIDATE="127.0.0.1" \
    -v ~/hello/config/srs_latest.conf:/usr/local/srs/conf/srs.conf \
   ossrs/srs:5 \
   ./objs/srs -c conf/srs.conf
```

其中：

- `1935/tcp`：RTMP（SRS 内部回环推流也会用到）
- `1985/tcp`：HTTP API
- `8080/tcp`：HTTP Server（SRS 自带的控制台页面）
- `8000/udp`：WebRTC（RTC Server）

我实际工程里会把 改摄像头配置 -> 生成 srs.conf -> 重启容器 这套动作做成一键脚本，避免手工改配置带来的维护成本，规范一点可以弄个网页让用户维护摄像头配置。

## 四、前端落地

### 1. Web 端播放

由于浏览器对 WebRTC 原生支持比较好，标准 HTML5 `<video>` 可以直接接住 WebRTC 流播放，我在前端页面里直接用 `<video>` 标签播放 SRS 输出的 WebRTC 流，让浏览器原生解码器（通常能自动走 H.264 硬解）解码，前端不需要引入其他第三方库，CPU 占用也更可控。

前端的静态资源服务器可以是 Nginx，也可以是其它轻量方案，比如 SRS 自带的 HTTP Server 就可以直接用来托管前端页面，或者 nodejs、python 都行。

### 2. 桌面化（Qt / QWebEngine）

为了集成到现有的 Qt@6.8.3 桌面应用中，我用 `QWebEngineView` 直接嵌入前端页面，这样 UI 与 Web 端可以最大化复用。

这里有一个必踩的坑：

QT 官方包里带的 QWebEngine 因为专利原因是不包含 H.264 编解码能力的，需要下载源码自行编译并[增加 `-webengine-proprietary-codecs` 编译指令启用专有编解码器支持](https://doc.qt.io/qt-6/qtwebengine-features.html#feature-h264) ，才能让 QWebEngineView 的 Chromium 内核支持 H.264 编码。

另外注意让内置浏览器的视频解码尽可能走 VA-API 等硬解路径，可以在 QWebEngineView 里打开 `chrome://gpu` 看一下最下面的 `Video Acceleration Information` 有没有 H.264 硬解支持。我增加的 QT 环境变量如下：

```cpp
// 开启 H.264 和 WebRTC 支持
qputenv("QTWEBENGINE_CHROMIUM_FLAGS", "--enable-features=VaapiVideoDecoder,VaapiVideoEncoder,VaapiIgnoreDriverChecks,VaapiVideoDecodeLinuxGL --ignore-gpu-blocklist --enable-gpu-rasterization --in-process-gpu --disable-features=UseChromeOSDirectVideoDecoder --limit-fps=20 --num-raster-threads=4 ");
```

#### 优化项：SmartH264

注意在摄像头的配置中，将摄像头的 H.264 编码参数调优为 SmartH264，可以让摄像头在画面静止时降低码率（在画面不怎么动的情况下可以最大降低 90% 码流），减少网络带宽占用，同时在画面有变化时提升码率和帧率，保证画面质量。这样在多路并发时，可以显著降低整体的网络和解码压力。

![](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo202512191659281.png)

#### 优化项：硬解验证与驱动选择

在使用 intel 集显的 i7-7700 测试时，通过指定集显使用特定的 VA-API 硬件加速驱动 `export LIBVA_DRIVER_NAME=iHD`，强制开启 VA-API 硬解：

```bash
# 通过下面这个命令查看当前 GPU 使用情况
sudo intel_gpu_top
```

![](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo202512191647279.png)

如果 intel_gpu_top 命令 Engine 的 Video 不为 0，则说明硬解成功，事实证明如果可以成功开启 GPU 硬解，那么即使使用集显，CPU 负载也能保持较低水平。如果使用 AMD/NVIDIA 显卡，需要参考对应的 VA-API 驱动文档，确保硬解被正确启用。

## 五、总结

通过 SRS 将 RTSP + H.264 视频流转封装为 WebRTC + H.264，并在前端浏览器和 Qt 桌面应用中播放，成功实现了多路低延迟的实时视频监控需求。我这边在实际测试中，i7-7700 的 CPU 上使用集显 GPU 播放 6 路 1080p H.264 流，CPU 总占用保持在 20% 左右，延迟控制在 300-500ms 之间。

---

网上的帖子大多深浅不一，甚至有些前后矛盾，在下的文章都是学习过程中的总结，如果发现错误，欢迎留言指出，如果本文帮助到了你，别忘了点赞支持一下，你的点赞是我更新的最大动力！~

> 1. [SRS Getting Started](https://ossrs.io/lts/zh-cn/docs/v5/doc/getting-started)
> 2. [Qt WebEngine H.264 Feature](https://doc.qt.io/qt-6/qtwebengine-features.html#feature-h264)

PS：本文同步更新于在下的博客 [Github - SHERlocked93/blog](https://github.com/SHERlocked93/blog)
系列文章中，欢迎大家关注我的公众号 `CPP下午茶`，直接搜索即可添加，持续为大家推送 CPP 以及 CPP 周边相关优质技术文，共同进步，一起加油\~
