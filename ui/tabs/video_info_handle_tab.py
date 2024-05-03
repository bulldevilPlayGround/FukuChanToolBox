from ui.tabs.abstract_tab import tkTabFrame
import tkinter as tk
from video.videoHandle import videoHandler
import ui.items.file_items as file_items
import ui.items.text_items as text_items

class tkVideoInfoHandleTab(tkTabFrame):
    def create_widgets(self):
        self.video_speeder = videoHandler()
        self.inputFilesSelectItem = file_items.fileListSelectItem(self, "输入文件: ", "浏览")
        self.inputSpeedSelectItem = text_items.textSelectItem(self, "速度")

        self.run_button = tk.Button(self, text="运行", command=self.run_video_speeder)
        #使用grid布局，把run_button放在最下面,右对齐
        self.run_button.grid(row=file_items.fileAbstractItem.current_row+1, column=1, padx=5, pady=5, sticky='e')

    def run_video_speeder(self):
        input_files = self.inputFilesSelectItem.entry.get("1.0", tk.END).splitlines()
        speed = float(self.inputSpeedSelectItem.entry.get())  # Convert speed to float
        self.video_speeder.change_speed_all(input_files, speed)
