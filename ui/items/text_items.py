import tkinter as tk

#创建一个textSelectItem类，它只有一个文本框，用来输入文字，没有按钮，也不是fileAbstractItem的子类
class textSelectItem:
    current_row = 0  # 静态变量,用于跟踪当前行号
    def __init__(self, master, labelStr):
        self.label = tk.Label(master, text=labelStr)
        self.label.grid(row=self.current_row, column=0, padx=5, pady=5, sticky='w')  # 标签左对齐

        # 创建文本框
        self.entry = tk.Entry(master)
        self.entry.grid(row=self.current_row, column=1, padx=5, pady=5, sticky='ew')  # 文本框左对齐,水平填充
        master.grid_columnconfigure(1, weight=1)  # 设置第二列的权重为1,使文本框长度自适应窗口大小

        self.current_row += 1  # 递增行号
