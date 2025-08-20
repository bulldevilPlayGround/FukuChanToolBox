from text.videoInfoParserWord import videoInfoParserWord

#test
debugMode = True
input_file= '25.7.5_时间线.docx'
file = videoInfoParserWord(verbose=debugMode, file=input_file)
# file.printTheFile()
print(len(file.videoTexts))
print(len(file.timestamps))
# file.doc_dict_to_excel(file.doc_dict, 'result.xlsx')