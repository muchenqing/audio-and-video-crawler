import requests
import json
from config.settings import TIMEOUT

class NeteaseMusicAPI:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Referer": "https://music.163.com"
        }
    
    def search_songs(self, keyword, limit=10):
        """搜索网易云音乐"""
        url = "https://music.163.com/api/search/get/web"
        params = {
            "s": keyword,
            "type": 1,
            "offset": 0,
            "total": True,
            "limit": limit
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=TIMEOUT)
            response.raise_for_status()
            data = response.json()
            
            songs = []
            if data.get("result", {}).get("songs"):
                for song in data["result"]["songs"]:
                    song_info = {
                        "id": song.get("id"),
                        "name": song.get("name"),
                        "artist": ", ".join([ar.get("name") for ar in song.get("artists", [])]),
                        "album": song.get("album", {}).get("name"),
                        "duration": song.get("duration") // 1000
                    }
                    songs.append(song_info)
            
            return songs
        except Exception as e:
            print(f"网易云音乐搜索异常: {str(e)}")
            return []
    
    def get_song_url(self, song_id):
        """获取网易云音乐下载链接"""
        # 注意：网易云音乐的下载链接获取需要签名等操作
        # 这里简化处理，实际项目中可能需要更复杂的实现
        url = "https://music.163.com/api/song/enhance/player/url"
        params = {
            "ids": [song_id],
            "br": 320000,
            "csrf_token": ""
        }
        
        try:
            response = requests.post(url, headers=self.headers, data=params, timeout=TIMEOUT)
            response.raise_for_status()
            data = response.json()
            
            if data.get("data"):
                song_data = data["data"][0]
                if song_data.get("url"):
                    return song_data.get("url")
            
            return None
        except Exception as e:
            print(f"获取网易云音乐下载链接异常: {str(e)}")
            return None