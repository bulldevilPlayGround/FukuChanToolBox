import docx2txt
import openpyxl
import re
# Regular expression patterns
EMPTY_LINE_PATTERN = r'^$'
SECTION_PATTERN_TITLE = r'^[\s\t]*\d+[\s\t]*$'
TIMESTAMP_PATTERN = r'^((?:\d+[:：\.])?\d{2}[:：\.]\d{2})\s*([\S\s]*)'  #时间戳可能没有小时，只有分钟
TAIL_PATTERN = r'^-(?:\d+[:：\.])?\d{2}[:：\.]\d{2}$'
"""
doc_dict format:
{
  "1": [
    {
      "time": "00:00",
      "text": "line1"
    },
    {
      "time": "04:23",
      "text": "line"
    },
    ...
  ],
  ...
}
timestamps
{
    "1": [time1, time2, time3 ....],
    "2": [time1, time2, time3 ....],
    ...
}
"""
def debugLog(flag, *args):
    if flag:
        print(*args)

class wordToExcel:
    def __init__(self, file, verbose=False):
        self.verbose = verbose
        self.doc_dict = {}
        self.timestamps = []
        self.videoTexts = []
        self.__load_word_doc__(file)
        self.__parse_title_from_lines__()
        self.__structure_doc__()

    def __load_word_doc__(self, file):
        text = docx2txt.process(file)
        #去除text里的制表符和空行
        text = re.sub(r'[\t\r]', '', text)
        text = re.sub(r'\n+', '\n', text)
        self.lines = text.split('\n')

    def __parse_title_from_lines__(self):
        #如果第三行是时间戳正文，那么第一行是标题
        if re.match(TIMESTAMP_PATTERN, self.lines[2]):
            self.title = self.lines[0]
        else:
            self.title = ''

    def __structure_doc__(self):
        sec_str = ""
        i = 0 if self.title == '' else 1
        while i < len(self.lines):
            debugLog(self.verbose, f"IN: line {i}: {self.lines[i]}")
            #找到章节的标题，开始第一个循环
            if re.match(SECTION_PATTERN_TITLE, self.lines[i]):
                sec_str = self.lines[i]
                self.doc_dict[sec_str] = sec_list = []
                debugLog(self.verbose, f"sec_str in line {i}: {self.lines[i]}")
                i += 1
                 #跳到下一行，遍历当前章节，结束条件是没有到达最后，以及下一行不是章节标题
                while i < len(self.lines):
                    debugLog(self.verbose, f"Sub IN: line {i}: {self.lines[i]}")
                    #按照标准的'timestamp text'格式，找到时间戳，加入到sec_list
                    line_data = re.search(TIMESTAMP_PATTERN, self.lines[i])
                    if line_data:
                        debugLog(self.verbose, f"append normal line {i}")
                        sec_list.append({
                            'time' : re.sub(r'[:：.]', ':', line_data.group(1)),
                            'text': line_data.group(2)
                        })
                    #text是多行，会导致改行只有文字，追加多行文字到list末尾的text里
                    elif self.lines[i] != '' and not re.match(TAIL_PATTERN, self.lines[i]):
                        if not sec_list : raise ValueError(f"文件格式错误，缺少必要的时间戳")
                        debugLog(self.verbose, f"append multi-line {i} to last line in list")
                        sec_list[-1]['text'] += '\n'+self.lines[i]
                        i += 1
                    #如果是尾行，可能有“-timestamp”单独成行，追加到list末尾的时间戳里
                    elif re.match(TAIL_PATTERN, self.lines[i]):
                        if not sec_list : raise ValueError(f"文件格式错误，缺少必要的时间戳")
                        debugLog(self.verbose, f"line {i} is tail, break here ")
                        #sec_list的最后一个元素的timestamp要拼接上这一行
                        sec_list[-1]['time'] += self.lines[i].replace('.', ':')
                    #break if reach the end of section
                    if i+1 < len(self.lines) and re.match(SECTION_PATTERN_TITLE, self.lines[i+1]):
                        debugLog(self.verbose, f"line {i+1} is next sec, break here ")
                        i += 1
                        break;
                    i += 1
            else:
                i += 1
            debugLog(self.verbose, f"File converted to dict")

        self.__fetch_time_list__(self.doc_dict)
        self.__fetch_videoText_list__(self.doc_dict)
        if self.verbose: self.print_doc_dict(self.doc_dict)

    def __fetch_time_list__(self, doc_dict):
        self.timestamps = []
        for _, sec_list in doc_dict.items():
            # sec['time']是一个(HH):MM:SS格式的时间戳，
            # 但是有些特殊情况它可能是(HH):MM:SS-(HH):MM:SS格式
            # 所以在这里如果sec['time']里包含“-”只需要插入“-”之前的部分
            self.timestamps.append([sec['time'].split('-')[0] for sec in sec_list])
        debugLog(self.verbose, f"{len(self.timestamps)} timestamps: {self.timestamps}")

    def __fetch_videoText_list__(self, doc_dict):
        self.videoTexts = []
        for _, sec_list in doc_dict.items():
            self.videoTexts.append([sec['text'] for sec in sec_list])
        debugLog(self.verbose, f"{len(self.videoTexts)} videoTexts: {self.videoTexts}")

    def doc_dict_to_excel(self, doc_dict, output_file='result.xlsx'):
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        # Write headers
        sheet['A1'] = 'Chapter Title'
        sheet['B1'] = 'Index'
        sheet['C1'] = 'Timestamp'
        sheet['D1'] = 'Text'
        # Write data
        row = 2
        for chapter_title, chapter_data in doc_dict.items():
            # Merge cells for chapter title
            sheet[f'A{row}'] = chapter_title
            sheet.merge_cells(f'A{row}:A{row + len(chapter_data) - 1}')
            index = 1
            for data in chapter_data:
                sheet[f'B{row}'] = index
                sheet[f'C{row}'] = data['time']
                sheet[f'D{row}'] = data['text']
                row += 1
                index += 1
        # Save the workbook
        workbook.save(output_file)

    def print_doc_dict(self, doc_dict):
        for sec_str, sec_list in doc_dict.items():
            debugLog(self.verbose, f"-----------------")
            debugLog(self.verbose, f"Section {sec_str}:")
            debugLog(self.verbose, f"-----------------")
            for line in sec_list:
                debugLog(self.verbose, f"{line['time']} {line['text']}")

    def printTheFile(self):
        i = 0
        while i < len(self.lines):
            print(f"{i}: {self.lines[i]}")
            i += 1

# file = '24.4.12.docx'
# file = '2.24.docx'
# debugMode = True
# file = '24.3.7黑衣服.docx'
# file = wordToExcel(verbose=debugMode, file=file)
# # debugLog(file.verbose, f"title is {file.title}")
# # debugLog(file.verbose, "-----------------")
# file.printTheFile()
# debugLog(file.verbose, "-----------------")
# file.doc_dict_to_excel(file.doc_dict, 'result.xlsx')
