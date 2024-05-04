import threading
import tkinter as tk
from ui.tabs.abstract_tab import tkTabFrame
import ui.items.file_items as file_items
import ui.items.text_items as text_items
from video.videoSpeeder import videoSpeeder

class tkVideoSpeederTab(tkTabFrame):
    def create_widgets(self):
        self.videoSpeeder = videoSpeeder()
        self.inputFilesSelectItem = file_items.fileListSelectItem(self, "输入文件📂: ", "浏览🔍")
        self.inputSpeedSelectItem = text_items.textSelectItem(self, "速度⏱️")
        #在速度下方增加一个文字标签
        self.label = tk.Label(self, text="😺😺😺")
        self.label.grid(row=file_items.fileAbstractItem.current_row+1, column=0, columnspan=3, padx=5, pady=5)
        #使用grid布局，把run_button放在最下面,右对齐
        self.run_button = tk.Button(self, text="运行😺", command=self.run_videoSpeeder)
        self.run_button.grid(row=file_items.fileAbstractItem.current_row+1, column=1, padx=5, pady=5, sticky='e')
        self.stop_button = tk.Button(self, text="停止😾", command=self.stop_videoSpeeder)
        self.stop_button.grid(row=file_items.fileAbstractItem.current_row+1, column=2, padx=5, pady=5, sticky='e')

    def run_videoSpeeder(self):
        input_files = [line for line in self.inputFilesSelectItem.entry.get("1.0", tk.END).splitlines() if line]
        speed = float(self.inputSpeedSelectItem.entry.get())  # Convert speed to float
        with self.videoSpeeder.lock:
            if not self.videoSpeeder.running:
                self.label.config(text="😾正在处理⏳...")
                self.videoSpeeder.running = True
                threading.Thread(target=self.videoSpeeder.change_speed_all, args=(input_files, speed)).start()
            else:
                self.label.config(text="🙀处理中❌")
        self.check_status()

    def check_status(self):
        if self.videoSpeeder.atomic_is_running():
            self.master.after(500, self.check_status)
        else:
            self.label.config(text="😼处理完成🆗")

    def stop_videoSpeeder(self):
        self.videoSpeeder.stop_processing()
        self.label.config(text="😾取消处理❌")