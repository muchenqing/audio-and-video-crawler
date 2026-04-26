import tkinter as tk
from tkinter import ttk, messagebox
from services.video_service import VideoService
import threading
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import DOWNLOAD_DIR
from api.image_api import ImageAPI
from PIL import Image, ImageTk

class ModernDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("多媒体下载器")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # 设置主题颜色
        self.bg_color = "#f0f2f5"
        self.primary_color = "#1890ff"
        self.secondary_color = "#52c41a"
        self.text_color = "#333333"
        self.accent_color = "#faad14"
        
        # 创建服务实例
        self.service = VideoService()
        self.image_api = ImageAPI()
        
        # 创建主框架
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建界面元素
        self.create_widgets()
        
        # 初始化图片相关变量
        self.current_image = None
    
    def create_widgets(self):
        # 标题
        title_frame = ttk.Frame(self.main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(
            title_frame, 
            text="多媒体下载器", 
            font=("微软雅黑", 24, "bold"),
            foreground=self.primary_color
        )
        title_label.pack(side=tk.LEFT)
        
        # 平台选择
        platform_frame = ttk.LabelFrame(self.main_frame, text="选择平台", padding="15")
        platform_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.platform = tk.StringVar(value="bilibili")
        
        platform_inner_frame = ttk.Frame(platform_frame)
        platform_inner_frame.pack(fill=tk.X, expand=True)
        
        bilibili_radio = ttk.Radiobutton(
            platform_inner_frame, 
            text="哔哩哔哩", 
            value="bilibili", 
            variable=self.platform, 
            command=self.update_ui
        )
        bilibili_radio.pack(side=tk.LEFT, padx=10)
        
        qq_music_radio = ttk.Radiobutton(
            platform_inner_frame, 
            text="QQ音乐", 
            value="qq_music", 
            variable=self.platform, 
            command=self.update_ui
        )
        qq_music_radio.pack(side=tk.LEFT, padx=10)
        
        netease_music_radio = ttk.Radiobutton(
            platform_inner_frame, 
            text="网易云音乐", 
            value="netease_music", 
            variable=self.platform, 
            command=self.update_ui
        )
        netease_music_radio.pack(side=tk.LEFT, padx=10)
        
        image_radio = ttk.Radiobutton(
            platform_inner_frame, 
            text="图片查看", 
            value="image", 
            variable=self.platform, 
            command=self.update_ui
        )
        image_radio.pack(side=tk.LEFT, padx=10)
        
        # 下载类型选择（仅B站）
        self.type_frame = ttk.LabelFrame(self.main_frame, text="下载类型", padding="15")
        
        self.download_type = tk.StringVar(value="video")
        
        type_inner_frame = ttk.Frame(self.type_frame)
        type_inner_frame.pack(fill=tk.X, expand=True)
        
        video_radio = ttk.Radiobutton(
            type_inner_frame, 
            text="视频", 
            value="video", 
            variable=self.download_type
        )
        video_radio.pack(side=tk.LEFT, padx=10)
        
        audio_radio = ttk.Radiobutton(
            type_inner_frame, 
            text="音乐", 
            value="audio", 
            variable=self.download_type
        )
        audio_radio.pack(side=tk.LEFT, padx=10)
        
        # 输入区域
        self.input_frame = ttk.LabelFrame(self.main_frame, text="输入信息", padding="15")
        
        id_frame = ttk.Frame(self.input_frame)
        id_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.id_label = ttk.Label(id_frame, text="BV号:", width=8)
        self.id_label.pack(side=tk.LEFT, padx=10)
        
        self.id_entry = ttk.Entry(id_frame)
        self.id_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        
        # 搜索功能（仅音乐平台）
        self.search_frame = ttk.LabelFrame(self.main_frame, text="音乐搜索", padding="15")
        
        search_inner_frame = ttk.Frame(self.search_frame)
        search_inner_frame.pack(fill=tk.X, pady=(0, 10))
        
        search_label = ttk.Label(search_inner_frame, text="歌名:", width=8)
        search_label.pack(side=tk.LEFT, padx=10)
        
        self.search_entry = ttk.Entry(search_inner_frame)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        
        self.search_button = ttk.Button(
            search_inner_frame, 
            text="搜索", 
            command=self.start_search,
            style="Accent.TButton",
            width=10
        )
        self.search_button.pack(side=tk.LEFT, padx=10, pady=5)
        
        # 搜索结果操作
        result_action_frame = ttk.Frame(self.search_frame)
        result_action_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.select_button = ttk.Button(
            result_action_frame, 
            text="选择歌曲", 
            command=self.select_song,
            style="Primary.TButton",
            width=12
        )
        self.select_button.pack(side=tk.LEFT, padx=10, pady=5)
        
        # 搜索结果列表
        self.result_frame = ttk.LabelFrame(self.main_frame, text="搜索结果", padding="15")
        
        columns = ("id", "name", "artist", "album")
        self.result_tree = ttk.Treeview(self.result_frame, columns=columns, show="headings")
        
        # 配置列宽，使用相对宽度
        for col in columns:
            self.result_tree.heading(col, text=col)
            if col == "id":
                self.result_tree.column(col, width=100, minwidth=80)
            elif col == "name":
                self.result_tree.column(col, width=200, minwidth=150, stretch=tk.YES)
            elif col == "artist":
                self.result_tree.column(col, width=120, minwidth=100)
            else:
                self.result_tree.column(col, width=120, minwidth=100)
        
        scrollbar = ttk.Scrollbar(self.result_frame, orient=tk.VERTICAL, command=self.result_tree.yview)
        self.result_tree.configure(yscroll=scrollbar.set)
        
        self.result_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 下载按钮
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(fill=tk.X, pady=15)
        
        self.download_button = ttk.Button(
            button_frame, 
            text="开始下载", 
            command=self.start_download,
            style="Primary.TButton",
            width=15
        )
        self.download_button.pack(side=tk.RIGHT, padx=10, pady=10)
        
        # 状态区域
        self.status_frame = ttk.LabelFrame(self.main_frame, text="状态信息", padding="15")
        self.status_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.status_var = tk.StringVar()
        self.status_var.set("就绪")
        status_label = ttk.Label(
            self.status_frame, 
            textvariable=self.status_var, 
            font=("微软雅黑", 12),
            foreground=self.text_color
        )
        status_label.pack(anchor=tk.W)
        
        # 下载目录信息
        download_dir_frame = ttk.Frame(self.status_frame)
        download_dir_frame.pack(fill=tk.X, pady=(10, 0))
        
        download_dir_label = ttk.Label(
            download_dir_frame, 
            text="下载目录:", 
            font=("微软雅黑", 10)
        )
        download_dir_label.pack(side=tk.LEFT)
        
        self.download_dir_var = tk.StringVar()
        self.download_dir_var.set(DOWNLOAD_DIR)
        download_dir_value = ttk.Label(
            download_dir_frame, 
            textvariable=self.download_dir_var, 
            font=("微软雅黑", 10),
            foreground=self.primary_color,
            wraplength=600
        )
        download_dir_value.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        # 初始化UI
        self.update_ui()
        
        # 配置样式
        self.configure_styles()
        
        # 添加窗口大小变化事件处理
        self.root.bind("<Configure>", self.on_resize)
    
    def configure_styles(self):
        """配置UI样式"""
        style = ttk.Style()
        
        # 主窗口样式
        style.configure(
            "TFrame",
            background=self.bg_color
        )
        
        # 标签样式
        style.configure(
            "TLabel",
            background=self.bg_color,
            foreground=self.text_color,
            font=("微软雅黑", 10)
        )
        
        # 按钮样式
        style.configure(
            "Primary.TButton",
            background=self.primary_color,
            foreground="black",
            font=("微软雅黑", 12, "bold"),
            padding=15,
            relief=tk.RAISED,
            borderwidth=2
        )
        
        style.configure(
            "Accent.TButton",
            background=self.accent_color,
            foreground="black",
            font=("微软雅黑", 12, "bold"),
            padding=15,
            relief=tk.RAISED,
            borderwidth=2
        )
        
        # 增加按钮高度
        style.configure(
            "TButton",
            height=3
        )
        
        # 按钮悬停效果
        style.map(
            "Primary.TButton",
            background=[("active", "#40a9ff")],
            foreground=[("active", "black")]
        )
        
        style.map(
            "Accent.TButton",
            background=[("active", "#ffc53d")],
            foreground=[("active", "black")]
        )
        
        # 标签框架样式
        style.configure(
            "TLabelframe",
            background=self.bg_color,
            foreground=self.text_color,
            font=("微软雅黑", 12, "bold")
        )
        
        style.configure(
            "TLabelframe.Label",
            background=self.bg_color,
            foreground=self.text_color,
            font=("微软雅黑", 12, "bold")
        )
        
        # 输入框样式
        style.configure(
            "TEntry",
            font=("微软雅黑", 10)
        )
        
        # 树视图样式
        style.configure(
            "Treeview",
            background="white",
            foreground=self.text_color,
            font=("微软雅黑", 10),
            rowheight=25
        )
        
        style.configure(
            "Treeview.Heading",
            background=self.bg_color,
            foreground=self.text_color,
            font=("微软雅黑", 10, "bold")
        )
    
    def update_ui(self):
        """根据选择的平台更新界面"""
        platform = self.platform.get()
        
        # 隐藏所有框架
        self.type_frame.pack_forget()
        self.input_frame.pack_forget()
        self.search_frame.pack_forget()
        self.result_frame.pack_forget()
        
        # 隐藏图片查看框架
        if hasattr(self, 'image_frame'):
            self.image_frame.pack_forget()
        
        if platform == "bilibili":
            # 显示B站相关界面
            self.input_frame.pack(fill=tk.X, pady=(0, 20))
            self.type_frame.pack(fill=tk.X, pady=(0, 20))
            self.id_label.config(text="BV号:")
        elif platform == "qq_music" or platform == "netease_music":
            # 显示音乐平台相关界面
            self.input_frame.pack(fill=tk.X, pady=(0, 20))
            self.search_frame.pack(fill=tk.X, pady=(0, 20))
            self.result_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
            self.id_label.config(text="歌曲ID:")
        elif platform == "image":
            # 显示图片查看界面
            self.create_image_viewer()
            self.download_button.config(text="获取10张随机图片")
    
    def start_download(self):
        platform = self.platform.get()
        
        # 禁用按钮，避免重复点击
        self.status_var.set("正在获取...")
        self.download_button.config(state=tk.DISABLED)
        
        # 在新线程中执行操作，避免阻塞UI
        if platform == "bilibili":
            item_id = self.id_entry.get().strip()
            if not item_id:
                messagebox.showerror("错误", "请输入BV号")
                self.download_button.config(state=tk.NORMAL)
                self.status_var.set("就绪")
                return
            download_type = self.download_type.get()
            thread = threading.Thread(target=self.download_content, args=(item_id, download_type))
        elif platform == "qq_music":
            item_id = self.id_entry.get().strip()
            if not item_id:
                messagebox.showerror("错误", "请输入歌曲ID")
                self.download_button.config(state=tk.NORMAL)
                self.status_var.set("就绪")
                return
            thread = threading.Thread(target=self.download_qq_music, args=(item_id,))
        elif platform == "netease_music":
            item_id = self.id_entry.get().strip()
            if not item_id:
                messagebox.showerror("错误", "请输入歌曲ID")
                self.download_button.config(state=tk.NORMAL)
                self.status_var.set("就绪")
                return
            thread = threading.Thread(target=self.download_netease_music, args=(item_id,))
        elif platform == "image":
            thread = threading.Thread(target=self.get_random_image)
        
        thread.daemon = True
        thread.start()
    
    def start_search(self):
        platform = self.platform.get()
        keyword = self.search_entry.get().strip()
        
        if not keyword:
            messagebox.showerror("错误", "请输入搜索关键词")
            return
        
        # 禁用按钮，避免重复点击
        self.status_var.set("正在搜索...")
        self.search_button.config(state=tk.DISABLED)
        
        # 在新线程中执行搜索，避免阻塞UI
        thread = threading.Thread(target=self.search_music, args=(platform, keyword))
        thread.daemon = True
        thread.start()
    
    def download_content(self, bvid, download_type):
        try:
            self.status_var.set(f"正在获取信息...")
            if download_type == "audio":
                success = self.service.download_audio(bvid)
                if success:
                    self.status_var.set("下载成功！")
                    messagebox.showinfo("成功", "音乐下载成功！")
                else:
                    self.status_var.set("下载失败")
                    messagebox.showerror("错误", "音乐下载失败，请检查BV号是否正确")
            else:
                success = self.service.download_video(bvid)
                if success:
                    self.status_var.set("下载成功！")
                    messagebox.showinfo("成功", "视频下载成功！")
                else:
                    self.status_var.set("下载失败")
                    messagebox.showerror("错误", "视频下载失败，请检查BV号是否正确")
        except Exception as e:
            self.status_var.set("下载失败")
            messagebox.showerror("错误", f"下载过程中出现错误: {str(e)}")
        finally:
            self.status_var.set("就绪")
            self.download_button.config(state=tk.NORMAL)
    
    def search_music(self, platform, keyword):
        try:
            self.status_var.set(f"正在搜索...")
            
            # 清空结果列表
            for item in self.result_tree.get_children():
                self.result_tree.delete(item)
            
            # 搜索音乐
            if platform == "qq_music":
                songs = self.service.search_qq_music(keyword)
            elif platform == "netease_music":
                songs = self.service.search_netease_music(keyword)
            else:
                songs = []
            
            # 添加搜索结果
            for song in songs:
                self.result_tree.insert("", tk.END, values=(song.get("id"), song.get("name"), song.get("artist"), song.get("album")))
            
            self.status_var.set(f"搜索完成，找到 {len(songs)} 首歌曲")
        except Exception as e:
            self.status_var.set("搜索失败")
            messagebox.showerror("错误", f"搜索过程中出现错误: {str(e)}")
        finally:
            if self.status_var.get() != f"搜索完成，找到 {len(songs)} 首歌曲":
                self.status_var.set("就绪")
            self.search_button.config(state=tk.NORMAL)
    
    def download_qq_music(self, song_id):
        try:
            self.status_var.set(f"正在下载QQ音乐...")
            success = self.service.download_qq_music(song_id)
            
            if success:
                self.status_var.set("下载成功！")
                messagebox.showinfo("成功", "QQ音乐下载成功！")
            else:
                self.status_var.set("下载失败")
                messagebox.showerror("错误", "QQ音乐下载失败，请检查歌曲ID是否正确")
        except Exception as e:
            self.status_var.set("下载失败")
            messagebox.showerror("错误", f"下载过程中出现错误: {str(e)}")
        finally:
            self.status_var.set("就绪")
            self.download_button.config(state=tk.NORMAL)
    
    def download_netease_music(self, song_id):
        try:
            self.status_var.set(f"正在下载网易云音乐...")
            success = self.service.download_netease_music(song_id)
            
            if success:
                self.status_var.set("下载成功！")
                messagebox.showinfo("成功", "网易云音乐下载成功！")
            else:
                self.status_var.set("下载失败")
                messagebox.showerror("错误", "网易云音乐下载失败，请检查歌曲ID是否正确")
        except Exception as e:
            self.status_var.set("下载失败")
            messagebox.showerror("错误", f"下载过程中出现错误: {str(e)}")
        finally:
            self.status_var.set("就绪")
            self.download_button.config(state=tk.NORMAL)
    
    def select_song(self):
        """从搜索结果中选择歌曲并填充到输入框"""
        selected_item = self.result_tree.selection()
        if not selected_item:
            messagebox.showerror("错误", "请先选择一首歌曲")
            return
        
        # 获取选中歌曲的信息
        item = selected_item[0]
        song_id = self.result_tree.item(item, "values")[0]
        song_name = self.result_tree.item(item, "values")[1]
        
        # 填充到输入框
        self.id_entry.delete(0, tk.END)
        self.id_entry.insert(0, song_id)
        
        # 显示提示
        self.status_var.set(f"已选择歌曲: {song_name}")
    
    def get_random_image(self):
        """获取10张随机图片并显示"""
        try:
            self.status_var.set("正在获取10张随机图片...")
            
            # 清空之前的图片
            for widget in self.canvas_frame.winfo_children():
                widget.destroy()
            
            # 并行获取10张随机图片
            import concurrent.futures
            image_data_list = []
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                # 提交10个任务
                futures = [executor.submit(self.image_api.get_random_image) for _ in range(10)]
                # 收集结果
                for future in concurrent.futures.as_completed(futures):
                    image_data = future.result()
                    if image_data:
                        image_data_list.append(image_data)
            
            if image_data_list:
                self.image_data_list = image_data_list  # 保存图片数据列表
                
                # 显示图片，保持比例不变
                from io import BytesIO
                for i, image_data in enumerate(image_data_list):
                    # 加载图片
                    image = Image.open(BytesIO(image_data))
                    
                    # 计算缩放后的尺寸（保持比例）
                    max_width = 800
                    if image.width > max_width:
                        ratio = max_width / image.width
                        new_width = max_width
                        new_height = int(image.height * ratio)
                        image = image.resize((new_width, new_height), Image.LANCZOS)
                    
                    # 显示图片
                    photo = ImageTk.PhotoImage(image)
                    image_label = ttk.Label(self.canvas_frame, image=photo)
                    image_label.image = photo  # 保持引用
                    image_label.pack(pady=10)
                    
                    # 添加下载按钮
                    download_btn = ttk.Button(
                        self.canvas_frame, 
                        text=f"下载图片 {i+1}", 
                        command=lambda data=image_data, index=i: self.download_image(data, index),
                        style="Primary.TButton",
                        width=12
                    )
                    download_btn.pack(pady=5)
                
                # 更新画布滚动区域
                self.canvas_frame.update_idletasks()
                self.canvas.config(scrollregion=self.canvas.bbox("all"))
                
                self.status_var.set("10张图片加载成功！")
            else:
                self.status_var.set("获取图片失败")
                messagebox.showerror("错误", "获取随机图片失败，请稍后重试")
        except Exception as e:
            self.status_var.set("获取图片失败")
            messagebox.showerror("错误", f"获取图片过程中出现错误: {str(e)}")
        finally:
            self.status_var.set("就绪")
            self.download_button.config(state=tk.NORMAL)
    
    def download_image(self, image_data, index):
        """下载指定的图片"""
        try:
            self.status_var.set("正在下载图片...")
            
            # 创建图片下载目录
            image_dir = os.path.join(DOWNLOAD_DIR, "图片")
            os.makedirs(image_dir, exist_ok=True)
            
            # 生成文件名
            import time
            timestamp = int(time.time())
            filename = f"image_{timestamp}_{index+1}.jpg"
            filepath = os.path.join(image_dir, filename)
            
            # 保存图片
            with open(filepath, "wb") as f:
                f.write(image_data)
            
            self.status_var.set("图片下载成功！")
            messagebox.showinfo("成功", f"图片已下载到: {filepath}")
        except Exception as e:
            self.status_var.set("下载失败")
            messagebox.showerror("错误", f"下载图片过程中出现错误: {str(e)}")
        finally:
            self.status_var.set("就绪")
    
    def create_image_viewer(self):
        """创建图片查看界面"""
        # 隐藏其他框架
        self.type_frame.pack_forget()
        self.input_frame.pack_forget()
        self.search_frame.pack_forget()
        self.result_frame.pack_forget()
        
        # 创建图片查看框架
        self.image_frame = ttk.LabelFrame(self.main_frame, text="图片查看", padding="15")
        self.image_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # 创建图片显示区域（带滚动条）
        self.image_display_frame = ttk.Frame(self.image_frame)
        self.image_display_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建画布和滚动条
        self.canvas = tk.Canvas(self.image_display_frame)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 添加垂直滚动条
        vscrollbar = ttk.Scrollbar(self.image_display_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        vscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.config(yscrollcommand=vscrollbar.set)
        
        # 添加水平滚动条
        hscrollbar = ttk.Scrollbar(self.image_display_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        hscrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.config(xscrollcommand=hscrollbar.set)
        
        # 创建内部框架用于放置图片
        self.canvas_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.canvas_frame, anchor=tk.NW)
        
        # 重置下载按钮文本
        self.download_button.config(text="获取10张随机图片")
    
    def resize_image(self):
        """调整图片大小以适应窗口"""
        if hasattr(self, 'current_image') and self.current_image:
            try:
                # 获取显示区域的尺寸
                display_width = self.image_display_frame.winfo_width()
                display_height = self.image_display_frame.winfo_height()
                
                if display_width > 0 and display_height > 0:
                    # 调整图片大小
                    resized_image = self.current_image.resize(
                        (display_width, display_height), 
                        Image.LANCZOS
                    )
                    photo = ImageTk.PhotoImage(resized_image)
                    
                    # 更新图片显示
                    self.image_label.config(image=photo)
                    self.image_label.image = photo
            except Exception as e:
                print(f"调整图片大小失败: {str(e)}")
    
    def on_resize(self, event):
        """处理窗口大小变化事件"""
        # 获取新的窗口宽度
        new_width = event.width
        
        # 更新下载目录标签的换行长度
        if new_width > 200:
            # 留出一些边距
            wrap_length = new_width - 100
            for widget in self.status_frame.winfo_children():
                if isinstance(widget, ttk.Frame):
                    for label in widget.winfo_children():
                        if isinstance(label, ttk.Label) and label.cget("textvariable") == self.download_dir_var:
                            label.config(wraplength=wrap_length)
        
        # 确保搜索结果列表能够适应窗口大小
        if hasattr(self, 'result_tree'):
            # 调整搜索结果列表的列宽
            tree_width = self.result_frame.winfo_width() - 20  # 留出滚动条的宽度
            if tree_width > 0:
                # 重新分配列宽
                id_width = min(120, tree_width * 0.15)
                name_width = max(150, tree_width * 0.4)
                artist_width = min(150, tree_width * 0.2)
                album_width = min(150, tree_width * 0.25)
                
                self.result_tree.column("id", width=id_width)
                self.result_tree.column("name", width=name_width)
                self.result_tree.column("artist", width=artist_width)
                self.result_tree.column("album", width=album_width)
        


if __name__ == "__main__":
    root = tk.Tk()
    app = ModernDownloaderGUI(root)
    root.mainloop()