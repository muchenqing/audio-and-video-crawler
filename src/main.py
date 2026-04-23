import argparse
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.video_service import VideoService

def main():
    parser = argparse.ArgumentParser(description="哔哩哔哩视频爬虫")
    
    # 子命令
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # 下载单个视频命令
    download_parser = subparsers.add_parser("download", help="下载单个视频")
    download_parser.add_argument("bvid", help="视频BV号")
    
    # 搜索并下载命令
    search_parser = subparsers.add_parser("search", help="搜索并下载视频")
    search_parser.add_argument("keyword", help="搜索关键词")
    search_parser.add_argument("--limit", type=int, default=5, help="下载数量限制")
    
    # 解析参数
    args = parser.parse_args()
    
    service = VideoService()
    
    if args.command == "download":
        # 下载单个视频
        print(f"准备下载视频: BV{args.bvid}")
        success = service.download_video(args.bvid)
        if success:
            print("视频下载成功！")
        else:
            print("视频下载失败！")
    
    elif args.command == "search":
        # 搜索并下载视频
        print(f"准备搜索并下载视频: {args.keyword}")
        success = service.search_and_download(args.keyword, args.limit)
        if success:
            print("视频搜索并下载成功！")
        else:
            print("视频搜索或下载失败！")
    
    else:
        # 显示帮助信息
        parser.print_help()

if __name__ == "__main__":
    main()