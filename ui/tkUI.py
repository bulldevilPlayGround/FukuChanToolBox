import tkinter as tk
from tkinter import ttk
from ui.tabs.text_replacer_tab import tkTextReplacerTab
from ui.tabs.video_speeder_tab import tkVideoSpeederTab
from ui.tabs.video_info_handle_tab import tkVideoInfoHandleTab
class tkUIInstance(tk.Tk):
    def __init__(self, title):
        super().__init__()
        self.title(title);
        # 创建选项卡控件
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True)
        # 创建文字处理选项卡
        self.textReplacerTab = tkTextReplacerTab(self.notebook)
        self.videoSpeederTab = tkVideoSpeederTab(self.notebook)
        self.tkVideoInfoHandleTab = tkVideoInfoHandleTab(self.notebook)
        # 添加选项卡
        self.notebook.add(self.textReplacerTab, text="文本处理")
        self.notebook.add(self.videoSpeederTab, text="视频变速")
        self.notebook.add(self.tkVideoInfoHandleTab, text="视频信息解析")
