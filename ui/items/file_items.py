from tkinter import filedialog
import tkinter as tk

#创建一个接口类，是fileSelectItem的抽象类
class fileAbstractItem:
    current_row = 0  # 静态变量,用于跟踪当前行号

    def __init__(self, master, labelStr, buttonStr, default_path=None):
        # 创建标签
        self.label = tk.Label(master, text=labelStr)
        self.label.grid(row=fileAbstractItem.current_row, column=0, padx=5, pady=5, sticky='w')  # 标签左对齐

        # 创建文本框
        self.entry = tk.Text(master, height=4, wrap='word')
        self.entry.grid(row=fileAbstractItem.current_row, column=1, padx=5, pady=5, sticky='ew')  # 文本框左对齐,水平填充
        master.grid_columnconfigure(1, weight=1)  # 设置第二列的权重为1,使文本框长度自适应窗口大小
        # 设置默认路径
        if default_path:
            self.entry.insert("1.0", default_path)

        # 创建按钮
        self.select_button = tk.Button(master, text=buttonStr, command=self.command)
        self.select_button.grid(row=fileAbstractItem.current_row, column=2, padx=5, pady=5)  # 按钮在文本框的右下方

        fileAbstractItem.current_row += 1  # 递增行号
    def command(self):
        pass

class fileNameSelectItem(fileAbstractItem):
    def __init__(self, master, labelStr, buttonStr, default_path=None):
        super().__init__(master, labelStr, buttonStr, default_path)

    def command(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        self.entry.delete("1.0", tk.END) #"1.0"代表第一行第0列
        self.entry.insert("1.0", file_path)

class fileSelectItem(fileAbstractItem):
    def __init__(self, master, labelStr, buttonStr, default_path=None):
        super().__init__(master, labelStr, buttonStr, default_path)

    def command(self):
        file_path = filedialog.askopenfilename(filetypes=[("所有文件", "*.*")])
        self.entry.delete("1.0", tk.END)
        self.entry.insert("1.0", file_path)
#创建一个fileListSelectItem类，它可以选择多个文件，并保存到一个列表中
#按下按钮后，会弹出文件选择对话框，选择多个文件，并显示在文本框中,文本框每一行显示一个文件
class fileListSelectItem(fileAbstractItem):
    def __init__(self, master, labelStr, buttonStr, default_path=None):
        super().__init__(master, labelStr, buttonStr, default_path)

    def command(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("所有文件", "*.*")])
        for file_path in file_paths:
            self.entry.insert(tk.END, file_path + '\n')  # 将文件路径插入到文本框末尾，并换行
