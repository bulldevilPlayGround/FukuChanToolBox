import tkinter as tk
from tkinter import messagebox
import os
from ui.tabs.abstract_tab import tkTabFrame
import ui.items.file_items as file_items
from text.replacer import TextReplacer
from utils.logger import Logger, LogLevel

class tkTextReplacerTab(tkTabFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.logger = Logger()

    def create_widgets(self):
        self.replacer = TextReplacer()
        self.inputFileSelectItem = file_items.fileListSelectItem(self, "输入文件📂: ", "浏览🔍")
        self.ruleListFileSelectItem = file_items.fileSelectItem(self, "规则列表文件📂: ", "浏览🔍", "C:\云蔓\05_中间稿\云蔓 文稿 替换.xlsx")

        self.run_button = tk.Button(self, text="运行替换😺", command=self.run_replacer)
        #使用grid布局，把run_button放在最下面,右对齐
        self.run_button.grid(row=file_items.fileAbstractItem.current_row+1, column=1, padx=5, pady=5, sticky='e')

    def run_replacer(self):
        # 获取所有输入文件路径（可能有多行）
        input_files = [line for line in self.inputFileSelectItem.entry.get("1.0", tk.END).splitlines() if line.strip()]
        if not input_files:
            messagebox.showerror("错误提示", "请至少选择一个输入文件🆖")
            return

        rule_list_file = self.ruleListFileSelectItem.entry.get("1.0", tk.END).splitlines()[0]
        if not rule_list_file:
            messagebox.showerror("错误提示", "请选择规则列表文件🆖")
            return

        # 记录成功和失败的文件
        success_files = []
        failed_files = []

        # 加载规则列表（只需加载一次）
        try:
            # 处理每个输入文件
            for input_file in input_files:
                try:
                    # 自动生成输出文件名：在原文件名后添加"_替换"后缀
                    file_name, file_ext = os.path.splitext(input_file)
                    output_file = f"{file_name}_替换{file_ext}"

                    # 更新文件路径并处理
                    self.replacer.update_files(input_file, output_file, rule_list_file)

                    # 只在第一个文件时加载规则列表
                    if input_file == input_files[0]:
                        self.replacer.load_rule_list()

                    # 执行替换
                    self.replacer.replace_words()
                    success_files.append(input_file)
                except Exception as e:
                    failed_files.append((input_file, str(e)))
                    self.logger.log(LogLevel.ERROR, f"处理文件 {input_file} 失败：{str(e)}")

            # 显示处理结果
            if success_files and not failed_files:
                messagebox.showinfo("完成提示", f"全部替换完成🆗。😼已成功处理{len(success_files)}个文件。")
            elif success_files and failed_files:
                error_msg = "\n".join([f"{os.path.basename(f)}: {e}" for f, e in failed_files[:3]])
                if len(failed_files) > 3:
                    error_msg += f"\n...等{len(failed_files)}个文件失败"
                messagebox.showwarning("部分完成", f"部分替换完成⚠️。\n成功：{len(success_files)}个文件\n失败：{len(failed_files)}个文件\n\n失败文件示例：\n{error_msg}")
            else:
                error_msg = "\n".join([f"{os.path.basename(f)}: {e}" for f, e in failed_files[:3]])
                if len(failed_files) > 3:
                    error_msg += f"\n...等{len(failed_files)}个文件失败"
                messagebox.showerror("错误提示", f"全部替换失败🆖。\n失败文件示例：\n{error_msg}")
        except Exception as e:
            messagebox.showerror("错误提示", f"替换过程发生错误🆖, 😹错误信息: {str(e)}")
