from ui.tabs.abstract_tab import tkTabFrame
import tkinter as tk
import threading
from video.videoSplitter import videoSplitter
from text.videoInfoParserWord import videoInfoParserWord
from text.videoInfoParserExcel import videoInfoParserExcel
import ui.items.file_items as file_items
from utils.naming import change_file_type
from tkinter import messagebox

class tkVideoInfoHandleTab(tkTabFrame):
    def create_widgets(self):
        self.videoSplitter = videoSplitter()
        self.inputInfoFilesSelectItem = file_items.fileSelectItem(self, "输入视频信息文件📄: ", "浏览🔍")
        self.inputVideoFilesSelectItem = file_items.fileListSelectItem(self, "输入视频文件📽️: ", "浏览🔍")

        # 添加圆点勾选器
        self.file_format_var = tk.StringVar(value="word")
        self.format1_radiobutton = tk.Radiobutton(self, text="word格式", variable=self.file_format_var, value="word")
        self.format2_radiobutton = tk.Radiobutton(self, text="excel格式", variable=self.file_format_var, value="excel")
        self.format1_radiobutton.grid(row=file_items.fileAbstractItem.current_row+1, column=0, padx=5, pady=5, sticky='w')
        self.format2_radiobutton.grid(row=file_items.fileAbstractItem.current_row+1, column=1, padx=5, pady=5, sticky='w')

        self.label = tk.Label(self, text="😺😺😺")
        self.label.grid(row=file_items.fileAbstractItem.current_row+2, column=0, columnspan=3, padx=5, pady=5)
        #使用grid布局，把run_button放在最下面,右对齐
        self.run_button = tk.Button(self, text="运行😺", command=self.run_videoSplitter)
        self.run_button.grid(row=file_items.fileAbstractItem.current_row+3, column=1, padx=5, pady=5, sticky='e')
        self.stop_button = tk.Button(self, text="停止😾", command=self.stop_videoSplitter)
        self.stop_button.grid(row=file_items.fileAbstractItem.current_row+3, column=2, padx=5, pady=5, sticky='e')

    def check_input_files(self):
        if not self.video_info_file:
            raise ValueError("视频信息文件路径不能为空🙀。")
        if not self.video_files or all(not file for file in self.video_files):
            raise ValueError("视频文件列表不能为空🙀。")

    def check_file_format(self):
        selected_format = self.file_format_var.get()
        if selected_format == "word" and not self.video_info_file.endswith(".docx"):
            messagebox.showerror("文件格式错误", "请选择word格式的文件🙀。")
            return False
        elif selected_format == "excel" and not self.video_info_file.endswith(".xlsx"):
            messagebox.showerror("文件格式错误", "请选择excel格式的文件🙀。")
            return False
        return True

    def run_videoSplitter(self):
        self.video_info_file = self.inputInfoFilesSelectItem.entry.get("1.0", tk.END).splitlines()[0]
        self.video_files = [line for line in self.inputVideoFilesSelectItem.entry.get("1.0", tk.END).splitlines() if line]
        self.check_input_files()

        # 检查文件格式
        if not self.check_file_format():
            return

        # 根据选择的文件格式进行不同处理
        selected_format = self.file_format_var.get()
        if selected_format == "word":
            video_info_excel = change_file_type(self.video_info_file, 'xlsx')
            self.video_info = videoInfoParserWord(self.video_info_file)
            self.video_info.doc_dict_to_excel(self.video_info.doc_dict, video_info_excel)
            if len(self.video_info.timestamps) != len(self.video_files):
                raise ValueError(f"视频信息数量{len(self.video_info.timestamps)}与视频文件数量{len(self.video_files)}不匹配🙀。")
        elif selected_format == "excel":
            # 处理格式2的逻辑
            self.video_info = videoInfoParserExcel(self.video_info_file)
            if len(self.video_info.videoInfo) != len(self.video_files):
                raise ValueError(f"视频信息数量{len(self.video_info.videoInfo)}与视频文件数量{len(self.video_files)}不匹配🙀。")

        with self.videoSplitter.lock:
            if not self.videoSplitter.running:
                self.label.config(text="😾开始切割✂️⏳...")
                self.videoSplitter.running = True
                if selected_format == "word":
                    threading.Thread(target=self.videoSplitter.split_videos, args=(self.video_files, self.video_info.timestamps, self.video_info.videoTexts)).start()
                elif selected_format == "excel":
                    threading.Thread(target=self.videoSplitter.split_videos_execl, args=(self.video_files, self.video_info.videoInfo)).start()
            else:
                self.label.config(text="🙀处理中❌")
        self.check_status()

    def check_status(self):
        if self.videoSplitter.atomic_is_running():
            self.master.after(500, self.check_status)
        else:
            self.label.config(text="😼处理完成🆗")

    def stop_videoSplitter(self):
            self.videoSplitter.stop_processing()
            self.label.config(text="😾取消处理❌")
