import os
import requests
from tqdm import tqdm
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import DOWNLOAD_DIR, MAX_RETRIES, TIMEOUT

class VideoDownloader:
    def __init__(self):
        self.download_dir = DOWNLOAD_DIR
    
    def download_video(self, url, filename, headers=None):
        """下载视频文件"""
        if not headers:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Referer": "https://www.bilibili.com"
            }
        
        filepath = os.path.join(self.download_dir, filename)
        
        # 检查文件是否已存在
        if os.path.exists(filepath):
            print(f"文件已存在: {filename}")
            return True
        
        # 确保目录存在
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        retry = 0
        while retry < MAX_RETRIES:
            try:
                print(f"开始下载: {filename}")
                
                # 发送请求
                response = requests.get(url, headers=headers, stream=True, timeout=TIMEOUT)
                response.raise_for_status()
                
                # 获取文件大小
                total_size = int(response.headers.get("content-length", 0))
                
                # 下载文件
                with open(filepath, "wb") as f:
                    with tqdm(
                        desc=filename,
                        total=total_size,
                        unit="B",
                        unit_scale=True,
                        unit_divisor=1024,
                        ascii=True
                    ) as pbar:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                                pbar.update(len(chunk))
                
                print(f"下载完成: {filename}")
                return True
                
            except Exception as e:
                retry += 1
                print(f"下载失败 (尝试 {retry}/{MAX_RETRIES}): {str(e)}")
                if retry >= MAX_RETRIES:
                    print(f"下载失败，已达到最大重试次数")
                    return False
    
    def check_ffmpeg(self):
        """检查ffmpeg是否安装"""
        try:
            import subprocess
            # 尝试直接使用ffmpeg命令
            try:
                subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
                return True
            except (subprocess.SubprocessError, FileNotFoundError):
                # 尝试使用完整路径
                ffmpeg_path = "D:\\ffmpeg-8.1-essentials_build\\bin\\ffmpeg.exe"
                subprocess.run([ffmpeg_path, "-version"], capture_output=True, check=True)
                return True
        except (subprocess.SubprocessError, FileNotFoundError):
            return False
    
    def merge_video_audio(self, video_path, audio_path, output_path):
        """使用ffmpeg合并视频和音频"""
        # 检查ffmpeg是否安装
        if not self.check_ffmpeg():
            print("错误: ffmpeg未安装，请先安装ffmpeg并添加到系统PATH中")
            print("下载地址: https://ffmpeg.org/download.html")
            return False
        
        try:
            # 尝试使用ffmpeg-python库
            try:
                import ffmpeg
                
                # 合并视频和音频
                input_video = ffmpeg.input(video_path)
                input_audio = ffmpeg.input(audio_path)
                
                (ffmpeg
                 .output(input_video, input_audio, output_path, vcodec='copy', acodec='copy')
                 .overwrite_output()
                 .run(capture_stdout=True, capture_stderr=True)
                )
            except Exception:
                # 如果ffmpeg-python库失败，使用subprocess直接调用ffmpeg
                import subprocess
                ffmpeg_path = "D:\\ffmpeg-8.1-essentials_build\\bin\\ffmpeg.exe"
                cmd = [
                    ffmpeg_path,
                    "-i", video_path,
                    "-i", audio_path,
                    "-c:v", "copy",
                    "-c:a", "copy",
                    "-y",
                    output_path
                ]
                subprocess.run(cmd, capture_output=True, check=True)
            
            # 删除临时文件
            os.remove(video_path)
            os.remove(audio_path)
            
            print(f"合并完成: {output_path}")
            return True
        except Exception as e:
            print(f"合并失败: {str(e)}")
            return False
    
    def download_video_info(self, video_info):
        """下载视频信息中的所有分P"""
        if not video_info:
            return False
        
        # 创建视频目录
        video_dir = os.path.join(self.download_dir, video_info.title)
        os.makedirs(video_dir, exist_ok=True)
        
        success_count = 0
        total_count = len(video_info.pages)
        
        for page in video_info.pages:
            if page.video_url and page.audio_url:
                # 下载视频文件
                video_filename = f"{video_info.title}_P{page.page}_{page.part}_video.mp4"
                video_filepath = os.path.join(video_dir, video_filename)
                
                # 下载音频文件
                audio_filename = f"{video_info.title}_P{page.page}_{page.part}_audio.mp4"
                audio_filepath = os.path.join(video_dir, audio_filename)
                
                # 下载视频
                if not self.download_video(page.video_url, video_filepath):
                    print(f"视频下载失败: {page.part}")
                    continue
                
                # 下载音频
                if not self.download_video(page.audio_url, audio_filepath):
                    print(f"音频下载失败: {page.part}")
                    continue
                
                # 合并视频和音频
                output_filename = f"{video_info.title}_P{page.page}_{page.part}.mp4"
                output_filepath = os.path.join(video_dir, output_filename)
                
                if self.merge_video_audio(video_filepath, audio_filepath, output_filepath):
                    success_count += 1
                else:
                    print(f"合并失败: {page.part}")
        
        print(f"下载完成，成功: {success_count}/{total_count}")
        return success_count > 0
    
    def download_audio_info(self, video_info):
        """下载音频信息中的所有分P"""
        if not video_info:
            return False
        
        # 创建音频目录
        audio_dir = os.path.join(self.download_dir, "音乐", video_info.title)
        os.makedirs(audio_dir, exist_ok=True)
        
        success_count = 0
        total_count = len(video_info.pages)
        
        for page in video_info.pages:
            if page.audio_url:
                # 下载音频文件
                audio_filename = f"{video_info.title}_P{page.page}_{page.part}.mp3"
                audio_filepath = os.path.join(audio_dir, audio_filename)
                
                # 下载音频
                if self.download_video(page.audio_url, audio_filepath):
                    success_count += 1
                else:
                    print(f"音频下载失败: {page.part}")
        
        print(f"音频下载完成，成功: {success_count}/{total_count}")
        return success_count > 0
    
    def download_music(self, url, platform, song_id):
        """下载音乐文件"""
        # 创建音乐目录
        music_dir = os.path.join(self.download_dir, "音乐", platform)
        os.makedirs(music_dir, exist_ok=True)
        
        # 下载音乐文件
        music_filename = f"{song_id}.mp3"
        music_filepath = os.path.join(music_dir, music_filename)
        
        if self.download_video(url, music_filepath):
            print(f"{platform}音乐下载成功: {song_id}")
            return True
        else:
            print(f"{platform}音乐下载失败: {song_id}")
            return False