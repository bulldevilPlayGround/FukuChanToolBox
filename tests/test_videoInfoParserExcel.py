from text.videoInfoParserExcel import videoInfoParserExcel

#test
debugMode = True
input_file= '12月10日时间轴.xlsx'
file = videoInfoParserExcel(verbose=debugMode, file=input_file)
print(f"len of self.videoInfo: {len(file.videoInfo)}")
file.__debug_print_video_info__()
