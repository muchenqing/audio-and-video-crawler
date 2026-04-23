from api.bilibili_api import BilibiliAPI
from models.video import VideoInfo, VideoPage

class VideoCrawler:
    def __init__(self):
        self.api = BilibiliAPI()
    
    def crawl_video(self, bvid):
        """爬取视频信息"""
        print(f"开始爬取视频: {bvid}")
        
        # 获取视频基本信息
        video_data = self.api.get_video_info(bvid)
        if not video_data:
            return None
        
        # 解析视频信息
        video_info = VideoInfo(
            bvid=video_data.get("bvid"),
            title=video_data.get("title"),
            author=video_data.get("owner", {}).get("name"),
            view=video_data.get("stat", {}).get("view"),
            danmaku=video_data.get("stat", {}).get("danmaku"),
            reply=video_data.get("stat", {}).get("reply"),
            favorite=video_data.get("stat", {}).get("favorite"),
            coin=video_data.get("stat", {}).get("coin"),
            share=video_data.get("stat", {}).get("share"),
            cover=video_data.get("pic"),
            desc=video_data.get("desc")
        )
        
        # 获取分P信息
        pages = self.api.get_video_pages(bvid)
        for page in pages:
            video_page = VideoPage(
                cid=page.get("cid"),
                page=page.get("page"),
                part=page.get("part"),
                duration=page.get("duration")
            )
            
            # 获取下载链接
            download_data = self.api.get_video_download_url(bvid, page.get("cid"))
            if download_data:
                # 获取视频链接
                video_url = download_data.get("dash", {}).get("video", [{}])[0].get("baseUrl")
                if video_url:
                    video_page.set_video_url(video_url)
                # 获取音频链接
                audio_url = download_data.get("dash", {}).get("audio", [{}])[0].get("baseUrl")
                if audio_url:
                    video_page.set_audio_url(audio_url)
            
            video_info.add_page(video_page)
        
        print(f"视频爬取完成: {video_info.title}")
        return video_info
    
    def search_and_crawl(self, keyword, limit=5):
        """搜索并爬取视频"""
        print(f"搜索视频: {keyword}")
        
        results = self.api.search_videos(keyword)
        videos = []
        
        for i, result in enumerate(results):
            if i >= limit:
                break
            
            bvid = result.get("bvid")
            if bvid:
                video = self.crawl_video(bvid)
                if video:
                    videos.append(video)
        
        print(f"搜索完成，共找到 {len(videos)} 个视频")
        return videos