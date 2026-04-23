class VideoInfo:
    """视频信息模型"""
    def __init__(self, bvid, title, author, view, danmaku, reply, favorite, coin, share, cover, desc):
        self.bvid = bvid
        self.title = title
        self.author = author
        self.view = view
        self.danmaku = danmaku
        self.reply = reply
        self.favorite = favorite
        self.coin = coin
        self.share = share
        self.cover = cover
        self.desc = desc
        self.pages = []
    
    def add_page(self, page):
        """添加分P信息"""
        self.pages.append(page)
    
    def to_dict(self):
        """转换为字典"""
        return {
            "bvid": self.bvid,
            "title": self.title,
            "author": self.author,
            "view": self.view,
            "danmaku": self.danmaku,
            "reply": self.reply,
            "favorite": self.favorite,
            "coin": self.coin,
            "share": self.share,
            "cover": self.cover,
            "desc": self.desc,
            "pages": [page.to_dict() for page in self.pages]
        }

class VideoPage:
    """视频分P信息模型"""
    def __init__(self, cid, page, part, duration):
        self.cid = cid
        self.page = page
        self.part = part
        self.duration = duration
        self.video_url = None
        self.audio_url = None
    
    def set_video_url(self, url):
        """设置视频下载链接"""
        self.video_url = url
    
    def set_audio_url(self, url):
        """设置音频下载链接"""
        self.audio_url = url
    
    def to_dict(self):
        """转换为字典"""
        return {
            "cid": self.cid,
            "page": self.page,
            "part": self.part,
            "duration": self.duration,
            "video_url": self.video_url,
            "audio_url": self.audio_url
        }