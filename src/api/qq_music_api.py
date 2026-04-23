import requests
import json
from config.settings import TIMEOUT

class QQMusicAPI:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Referer": "https://y.qq.com"
        }
    
    def search_songs(self, keyword, limit=10):
        """搜索QQ音乐"""
        url = "https://c.y.qq.com/soso/fcgi-bin/client_search_cp"
        params = {
            "ct": "24",
            "qqmusic_ver": "1298",
            "new_json": "1",
            "remoteplace": "txt.yqq.song",
            "searchid": "64405487069162918",
            "t": "0",
            "aggr": "1",
            "cr": "1",
            "catZhida": "1",
            "lossless": "0",
            "flag_qc": "0",
            "p": "1",
            "n": str(limit),
            "w": keyword,
            "g_tk_new_20200303": "5381",
            "g_tk": "5381",
            "loginUin": "0",
            "hostUin": "0",
            "format": "json",
            "inCharset": "utf8",
            "outCharset": "utf-8",
            "notice": "0",
            "platform": "yqq.json",
            "needNewCode": "0"
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=TIMEOUT)
            response.raise_for_status()
            data = response.json()
            
            songs = []
            if data.get("data", {}).get("song", {}).get("list"):
                for song in data["data"]["song"]["list"]:
                    song_info = {
                        "id": song.get("mid"),
                        "name": song.get("name"),
                        "artist": ", ".join([ar.get("name") for ar in song.get("singer", [])]),
                        "album": song.get("album", {}).get("name"),
                        "duration": song.get("interval")
                    }
                    songs.append(song_info)
            
            return songs
        except Exception as e:
            print(f"QQ音乐搜索异常: {str(e)}")
            return []
    
    def get_song_url(self, song_id):
        """获取QQ音乐下载链接"""
        # 注意：QQ音乐的下载链接获取比较复杂，需要签名等操作
        # 这里简化处理，实际项目中可能需要更复杂的实现
        url = "https://u.y.qq.com/cgi-bin/musicu.fcg"
        params = {
            "format": "json",
            "data": json.dumps({
                "req": {
                    "module": "CDN.SrfCdnDispatchServer",
                    "method": "GetCdnDispatch",
                    "param": {
                        "guid": "1234567890",
                        "calltype": 0,
                        "userip": ""
                    }
                },
                "req_0": {
                    "module": "vkey.GetVkeyServer",
                    "method": "CgiGetVkey",
                    "param": {
                        "guid": "1234567890",
                        "songmid": [song_id],
                        "songtype": [0],
                        "uin": "0",
                        "loginflag": 0,
                        "platform": "20"
                    }
                },
                "comm": {
                    "uin": 0,
                    "format": "json",
                    "ct": 24,
                    "cv": 0
                }
            })
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=TIMEOUT)
            response.raise_for_status()
            data = response.json()
            
            # 解析下载链接
            if data.get("req_0", {}).get("data", {}).get("midurlinfo"):
                info = data["req_0"]["data"]["midurlinfo"][0]
                vkey = info.get("vkey")
                if vkey:
                    return f"https://dl.stream.qqmusic.qq.com/{info.get('filename')}?vkey={vkey}&guid=1234567890&uin=0&fromtag=66"
            
            return None
        except Exception as e:
            print(f"获取QQ音乐下载链接异常: {str(e)}")
            return None