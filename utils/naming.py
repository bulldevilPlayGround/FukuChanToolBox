

def add_suffix(filename, suffix):
    file_name = '.'.join(filename.split('.')[:-1])
    file_type = filename.split('.')[-1]
    return file_name + suffix + '.' + file_type

def change_file_type(filename, new_type):
    file_name = '.'.join(filename.split('.')[:-1])
    return file_name + '.' + new_type

def refine_file_name(filename):
    # 去除文件名中不能作为windows文件名的字符
    return filename.replace('/', '_').replace('\\', '_').replace(':', '_').replace('*', '_').replace('?', '_').replace('"', '_').replace('<', '_').replace('>', '_').replace('|', '_')
