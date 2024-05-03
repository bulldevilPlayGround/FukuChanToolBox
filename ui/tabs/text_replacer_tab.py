import tkinter as tk
from ui.tabs.abstract_tab import tkTabFrame
import ui.items.file_items as file_items
from text.replacer import TextReplacer

class tkTextReplacerTab(tkTabFrame):
    def create_widgets(self):
        self.replacer = TextReplacer()
        self.inputFileSelectItem = file_items.fileSelectItem(self, "输入文件: ", "浏览")
        self.outPutFileSelectItem = file_items.fileNameSelectItem(self, "输出文件: ", "浏览")
        self.ruleListFileSelectItem = file_items.fileSelectItem(self, "规则列表文件: ", "浏览")

        self.run_button = tk.Button(self, text="运行替换", command=self.run_replacer)
        #使用grid布局，把run_button放在最下面,右对齐
        self.run_button.grid(row=file_items.fileAbstractItem.current_row+1, column=1, padx=5, pady=5, sticky='e')

    def run_replacer(self):
        input_file = self.inputFileSelectItem.entry.get("1.0", tk.END).splitlines()[0]
        output_file = self.outPutFileSelectItem.entry.get("1.0", tk.END).splitlines()[0]
        rule_list_file = self.ruleListFileSelectItem.entry.get("1.0", tk.END).splitlines()[0]

        self.replacer.update_files(input_file, output_file, rule_list_file)
        self.replacer.load_rule_list()
        self.replacer.replace_words()
        tk.messagebox.showinfo("完成提示", "替换完成。请查看输出文件: {}".format(output_file))
