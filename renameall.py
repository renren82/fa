import os

if __name__ == '__main__':
    dir_path = 'E:/yanyan/论语/download'
    list_file = os.listdir(dir_path)
    os.chdir(dir_path)
    for file_name in list_file:
        print(file_name)
        os.rename(file_name, file_name + ".mp3")
