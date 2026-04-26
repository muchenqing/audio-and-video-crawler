import requests

class ImageAPI:
    def __init__(self):
        self.base_url = "https://cnmiw.com/api.php"
        self.headers = {
            "Referer": "https://weibo.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
    
    def get_random_image(self):
        """获取随机图片"""
        try:
            params = {
                "sort": "random"
            }
            response = requests.get(self.base_url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.content
        except Exception as e:
            print(f"获取图片失败: {str(e)}")
            return None
    
    def get_random_images(self, num=1):
        """获取多张随机图片"""
        try:
            params = {
                "sort": "random",
                "type": "json",
                "num": min(num, 100)  # 最多100张
            }
            response = requests.get(self.base_url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"获取图片失败: {str(e)}")
            return None
    
    def get_image_content(self, url):
        """根据URL获取图片内容"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.content
        except Exception as e:
            print(f"获取图片内容失败: {str(e)}")
            return None