import requests
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import BILI_API_URL, BILI_USER_AGENT, TIMEOUT

class BilibiliAPI:
    def __init__(self):
        self.headers = {
            "User-Agent": BILI_USER_AGENT,
            "Referer": "https://www.bilibili.com"
        }
    
    def get_video_info(self, bvid):
        """获取视频基本信息"""
        url = f"{BILI_API_URL}/x/web-interface/view"
        params = {"bvid": bvid}
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=TIMEOUT)
            response.raise_for_status()
            data = response.json()
            
            if data.get("code") == 0:
                return data.get("data")
            else:
                print(f"获取视频信息失败: {data.get('message')}")
                return None
        except Exception as e:
            print(f"获取视频信息异常: {str(e)}")
            return None
    
    def get_video_pages(self, bvid):
        """获取视频分P信息"""
        video_info = self.get_video_info(bvid)
        if video_info:
            return video_info.get("pages", [])
        return []
    
    def get_video_download_url(self, bvid, cid, quality=116):
        """获取视频和音频下载链接"""
        url = f"{BILI_API_URL}/x/player/playurl"
        params = {
            "bvid": bvid,
            "cid": cid,
            "qn": quality,  # 125=4K, 120=1080P60, 116=1080P, 80=720P
            "fnval": 16
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=TIMEOUT)
            response.raise_for_status()
            data = response.json()
            
            if data.get("code") == 0:
                return data.get("data")
            else:
                print(f"获取下载链接失败: {data.get('message')}")
                return None
        except Exception as e:
            print(f"获取下载链接异常: {str(e)}")
            return None
    
    def search_videos(self, keyword, page=1, limit=20):
        """搜索视频"""
        url = f"{BILI_API_URL}/x/web-interface/search/all"
        params = {
            "keyword": keyword,
            "page": page,
            "limit": limit
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=TIMEOUT)
            response.raise_for_status()
            data = response.json()
            
            if data.get("code") == 0:
                return data.get("data", {}).get("result", [])
            else:
                print(f"搜索失败: {data.get('message')}")
                return []
        except Exception as e:
            print(f"搜索异常: {str(e)}")
            return []