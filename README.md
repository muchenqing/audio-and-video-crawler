# 哔哩哔哩视频爬虫

一个用于爬取和下载哔哩哔哩视频的Python程序。

## 功能特点

- 支持根据BV号下载单个视频
- 支持根据关键词搜索并下载多个视频
- 支持视频分P下载
- 支持断点续传和下载进度显示
- 支持高清晰度视频下载

## 环境要求

- Python 3.7+
- 依赖库：见requirements.txt

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 1. 下载单个视频

```bash
python src/main.py download BV1xx411c7mW
```

### 2. 搜索并下载视频

```bash
python src/main.py search "Python教程" --limit 5
```

## 项目结构

```
pachong/
├── config/
│   └── settings.py       # 配置文件
├── src/
│   ├── api/
│   │   └── bilibili_api.py  # 哔哩哔哩API接口封装
│   ├── crawler/
│   │   └── video_crawler.py # 视频爬虫核心逻辑
│   ├── downloader/
│   │   └── video_downloader.py # 视频下载功能
│   ├── models/
│   │   └── video.py       # 视频数据模型
│   ├── services/
│   │   └── video_service.py # 视频服务层
│   └── main.py           # 主程序入口
├── downloads/            # 下载目录
├── requirements.txt      # 项目依赖
└── README.md             # 项目说明
```

## 注意事项

1. 本工具仅供个人学习和研究使用，请勿用于商业用途
2. 请遵守哔哩哔哩的用户协议和相关法律法规
3. 下载视频时请尊重版权，仅下载自己有权使用的视频
4. 大量下载可能会导致IP被封禁，请合理使用

## 配置说明

在 `config/settings.py` 文件中可以修改以下配置：

- `DOWNLOAD_DIR`：下载目录路径
- `MAX_RETRIES`：最大重试次数
- `TIMEOUT`：请求超时时间
- `MAX_CONCURRENT_DOWNLOADS`：最大并发下载数

## 常见问题

1. **下载失败**：可能是网络问题或视频已被删除，请检查网络连接和视频状态
2. **IP被封禁**：请减少下载频率，或使用代理
3. **视频清晰度**：默认下载最高清晰度，可在代码中修改 `quality` 参数

## 许可证

MIT License