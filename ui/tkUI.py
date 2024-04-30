import tkinter as tk
from tkinter import ttk
from text.replacer import TextReplacer
import ui.items as items

class tkTabFrame(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(fill='both', expand=True)
        self.create_widgets()

    def create_widgets(self):
        pass

class tkTextReplacerTab(tkTabFrame):
    def create_widgets(self):
        self.replacer = TextReplacer()
        self.inputFileSelectItem = items.fileSelectItem(self, "输入文件: ", "浏览")
        self.outPutFileSelectItem = items.fileNameSelectItem(self, "输出文件: ", "浏览")
        self.ruleListFileSelectItem = items.fileSelectItem(self, "规则列表文件: ", "浏览")

        self.run_button = tk.Button(self, text="运行替换", command=self.run_replacer)
        #使用grid布局，把run_button放在最下面,右对齐
        self.run_button.grid(row=items.fileAbstractItem.current_row+1, column=1, padx=5, pady=5, sticky='e')

    def run_replacer(self):
        input_file = self.inputFileSelectItem.entry.get("1.0", tk.END).splitlines()[0]
        output_file = self.outPutFileSelectItem.entry.get("1.0", tk.END).splitlines()[0]
        rule_list_file = self.ruleListFileSelectItem.entry.get("1.0", tk.END).splitlines()[0]

        self.replacer.update_files(input_file, output_file, rule_list_file)
        self.replacer.load_rule_list()
        self.replacer.replace_words()
        tk.messagebox.showinfo("完成提示", "替换完成。请查看输出文件: {}".format(output_file))

class tkUIInstance(tk.Tk):
    def __init__(self, title):
        super().__init__()
        self.title(title);
        # 创建选项卡控件
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True)
        # 创建文字处理选项卡
        self.textReplacerTab = tkTextReplacerTab(self.notebook)
