import openpyxl
import re
import string
# Regular expression patterns
#时间戳可能没有小时，只有分钟，而且以小时或分钟开头时，可能只有一位数字
TIMESTAMP_PATTERN = r'^((?:\d{1,2}[:：\.])?\d{1,2}[:：\.]\d{2})\s*([\S\s]*)'
class videoInfoParserExcel:
    def __init__(self, file, verbose=False):
        self.verbose = verbose
        self.timestamps = []
        self.videoTexts = []
        self.sheet = self.__load_excel_file__(file)
        self.__fetch_time_list__(self.sheet)
        self.__fetch_videoText_list__(self.sheet)

    def __load_excel_file__(self, file):
        try:
            workbook = openpyxl.load_workbook(file)
            sheet = workbook.active
            if self.verbose:
                print(f"Successfully loaded {file}")
            return sheet
        except Exception as e:
            if self.verbose:
                print(f"Failed to load {file}: {e}")
            return None

    def __fetch_time_list__(self, sheet):
        listB = []
        for row in sheet.iter_rows(min_col=2, max_col=2):
            for cell in row:
                if cell.value is not None:
                    cell_value_str = str(cell.value)
                    if cell_value_str == "0" or re.match(TIMESTAMP_PATTERN, cell_value_str):
                        listB.append(cell_value_str)

        self.timestamps = []
        current_list = []
        for item in listB:
            if item == "0":
                item = "00:00"
            elif re.match(r'^\d{1}[:：\.]\d{2}$', item):
                item = "0" + item
            item = item.replace('.', ':')
            if item == "00:00" and current_list:
                self.timestamps.append(current_list)
                current_list = []
            current_list.append(item)
        if current_list:
            self.timestamps.append(current_list)

        if self.verbose:
            print(self.timestamps)

    def __fetch_videoText_list__(self, sheet):
        if not self.timestamps:
            raise ValueError("必须在时间戳解析之后才能解析文本")
        listE = []
        invalid_chars = '<>:"/\\|?*'
        for row in sheet.iter_rows(min_col=5, max_col=5):
            for cell in row:
                if cell.value is not None:
                    corresponding_d_cell = sheet.cell(row=cell.row, column=4).value
                    if corresponding_d_cell is not None and re.match(r'^[A-Za-z]$', str(corresponding_d_cell)):
                        first_line = str(cell.value).split('\n')[0]
                        first_line = ''.join(c for c in first_line if c not in invalid_chars)
                        listE.append(first_line)
        index = 0
        for sublist in self.timestamps:
            sublist_size = len(sublist)
            self.videoTexts.append(listE[index:index + sublist_size])
            index += sublist_size

        if self.verbose:
            print(self.videoTexts)
    def __debug_print_video_info__(self):
        for i in range(len(self.timestamps)):
            for j in range(len(self.timestamps[i])):
                print(f"{self.timestamps[i][j]}: {self.videoTexts[i][j]}")

#test
# debugMode = True
# input_file= '24.10.26_时间轴.xlsx'
# file = videoInfoParserExcel(verbose=debugMode, file=input_file)
# file.__debug_print_video_info__()