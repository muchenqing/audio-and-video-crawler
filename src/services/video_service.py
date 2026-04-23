from crawler.video_crawler import VideoCrawler
from downloader.video_downloader import VideoDownloader
from api.qq_music_api import QQMusicAPI
from api.netease_music_api import NeteaseMusicAPI

class VideoService:
    def __init__(self):
        self.crawler = VideoCrawler()
        self.downloader = VideoDownloader()
        self.qq_music_api = QQMusicAPI()
        self.netease_music_api = NeteaseMusicAPI()
    
    def get_video_info(self, bvid):
        """获取视频信息"""
        return self.crawler.crawl_video(bvid)
    
    def download_video(self, bvid):
        """下载视频"""
        video_info = self.get_video_info(bvid)
        if video_info:
            return self.downloader.download_video_info(video_info)
        return False
    
    def search_and_download(self, keyword, limit=5, download_type="video"):
        """搜索并下载视频或音乐"""
        videos = self.crawler.search_and_crawl(keyword, limit)
        success_count = 0
        
        for video in videos:
            if download_type == "audio":
                if self.downloader.download_audio_info(video):
                    success_count += 1
            else:
                if self.downloader.download_video_info(video):
                    success_count += 1
        
        print(f"搜索并下载完成，成功: {success_count}/{len(videos)}")
        return success_count > 0
    
    def download_audio(self, bvid):
        """下载音频"""
        video_info = self.get_video_info(bvid)
        if video_info:
            return self.downloader.download_audio_info(video_info)
        return False
    
    def search_qq_music(self, keyword, limit=10):
        """搜索QQ音乐"""
        return self.qq_music_api.search_songs(keyword, limit)
    
    def download_qq_music(self, song_id):
        """下载QQ音乐"""
        url = self.qq_music_api.get_song_url(song_id)
        if url:
            return self.downloader.download_music(url, "QQ音乐", song_id)
        return False
    
    def search_netease_music(self, keyword, limit=10):
        """搜索网易云音乐"""
        return self.netease_music_api.search_songs(keyword, limit)
    
    def download_netease_music(self, song_id):
        """下载网易云音乐"""
        url = self.netease_music_api.get_song_url(song_id)
        if url:
            return self.downloader.download_music(url, "网易云音乐", song_id)
        return False