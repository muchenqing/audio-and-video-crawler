import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 哔哩哔哩API配置
BILI_API_URL = "https://api.bilibili.com"
BILI_VIDEO_URL = "https://www.bilibili.com/video"
BILI_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

# 下载配置
DOWNLOAD_DIR = os.path.join(os.getcwd(), "downloads")
MAX_RETRIES = 3
TIMEOUT = 30

# 并发配置
MAX_CONCURRENT_DOWNLOADS = 5

# 日志配置
LOG_LEVEL = "INFO"

# 创建下载目录
os.makedirs(DOWNLOAD_DIR, exist_ok=True)