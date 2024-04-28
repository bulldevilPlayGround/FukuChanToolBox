import tkinter as tk
from tkinter import filedialog
from replacer import TextReplacer

#创建一个接口类，是fileSelectItem的抽象类
class fileAbstractItem:
    current_row = 0  # 静态变量,用于跟踪当前行号

    def __init__(self, master, labelStr, buttonStr):
        # 创建标签
        self.label = tk.Label(master, text=labelStr)
        self.label.grid(row=fileAbstractItem.current_row, column=0, padx=5, pady=5, sticky='w')  # 标签左对齐

        # 创建文本框
        self.entry = tk.Entry(master)
        self.entry.grid(row=fileAbstractItem.current_row, column=1, padx=5, pady=5, sticky='ew')  # 文本框左对齐,水平填充
        master.grid_columnconfigure(1, weight=1)  # 设置第二列的权重为1,使文本框长度自适应窗口大小

        # 创建按钮
        self.select_button = tk.Button(master, text=buttonStr, command=self.command)
        self.select_button.grid(row=fileAbstractItem.current_row, column=2, padx=5, pady=5)  # 按钮在文本框的右下方

        fileAbstractItem.current_row += 1  # 递增行号
    def command(self):
        pass

class fileNameSelectItem(fileAbstractItem):
    def __init__(self, master, labelStr, buttonStr):
        super().__init__(master, labelStr, buttonStr)

    def command(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        self.entry.delete(0, tk.END)
        self.entry.insert(0, file_path)

class fileSelectItem(fileAbstractItem):
    def __init__(self, master, labelStr, buttonStr):
        super().__init__(master, labelStr, buttonStr)

    def command(self):
        file_path = filedialog.askopenfilename(filetypes=[("所有文件", "*.*")])
        self.entry.delete(0, tk.END)
        self.entry.insert(0, file_path)

class tkUIInstance(tk.Tk):
    def __init__(self, title):
        super().__init__()
        self.title(title);
        # 创建UI组件
        self.replacer = TextReplacer()
        self.create_widgets()

    def create_widgets(self):
        #create a fileSelectItem object
        self.inputFileSelectItem = fileSelectItem(self, "输入文件: ", "浏览")
        self.outPutFileSelectItem = fileNameSelectItem(self, "输出文件: ", "浏览")
        self.ruleListFileSelectItem = fileSelectItem(self, "规则列表文件: ", "浏览")

        self.run_button = tk.Button(self, text="运行替换", command=self.run_replacer)
        #使用grid布局，把run_button放在最下面,右对齐
        self.run_button.grid(row=fileAbstractItem.current_row+1, column=1, padx=5, pady=5, sticky='e')


    def run_replacer(self):
        input_file = self.inputFileSelectItem.entry.get()
        output_file = self.outPutFileSelectItem.entry.get()
        rule_list_file = self.ruleListFileSelectItem.entry.get()

        self.replacer.update_files(input_file, output_file, rule_list_file)
        self.replacer.load_rule_list()
        self.replacer.replace_words()
        tk.messagebox.showinfo("完成提示", "替换完成。请查看输出文件: {}".format(output_file))
