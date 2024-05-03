from ui.tabs.abstract_tab import tkTabFrame
import tkinter as tk
from video.videoHandle import videoHandler
from text.wordToExcel import wordToExcel
import ui.items.file_items as file_items
from utils.naming import change_file_type

class tkVideoInfoHandleTab(tkTabFrame):
    def create_widgets(self):
        self.videoHandler = videoHandler()
        self.video_info_excel = ""
        self.inputInfoFilesSelectItem = file_items.fileSelectItem(self, "输入视频信息文件: ", "浏览")
        self.inputVideoFilesSelectItem = file_items.fileListSelectItem(self, "输入视频文件列表: ", "浏览")
        #使用grid布局，把run_button放在最下面,右对齐
        self.run_button = tk.Button(self, text="运行", command=self.run_handle)
        self.run_button.grid(row=file_items.fileAbstractItem.current_row+1, column=1, padx=5, pady=5, sticky='e')

    def check_input_files(self):
        if not self.video_info_file:
            raise ValueError("视频信息文件路径不能为空。")
        if not self.video_files or all(not file for file in self.video_files):
            raise ValueError("视频文件列表不能为空。")

    def run_handle(self):
        self.video_info_file = self.inputInfoFilesSelectItem.entry.get("1.0", tk.END).splitlines()[0]
        self.video_files = [line for line in self.inputVideoFilesSelectItem.entry.get("1.0", tk.END).splitlines() if line]
        self.check_input_files()
        self.video_info_excel = change_file_type(self.video_info_file, 'xlsx')
        self.video_info = wordToExcel(self.video_info_file)
        self.video_info.doc_dict_to_excel(self.video_info.doc_dict, self.video_info_excel)
        if len(self.video_info.timestamps) != len(self.video_files):
            raise ValueError(f"视频信息数量{len(self.video_info.timestamps)}与视频文件数量{len(self.video_files)}不匹配。")
        self.videoHandler.split_videos(self.video_files, self.video_info.timestamps, self.video_info.videoTexts)
