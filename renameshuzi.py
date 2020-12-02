import os
import json

path_root = 'D:/aaa/'


# 遍历文件夹
def walk_file(dir_path):
    for root, dirs, files in os.walk(dir_path):

        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list

        # 遍历文件
        # for f in files:
        #     print(os.path.join(root, f))

        # 遍历所有的文件夹
        # for d in dirs:
        #     print(os.path.join(root, d))
        #
        return files


os.chdir(path_root)

file_list = walk_file(path_root)
for find_file in file_list:
    # print(find_file)
    start = find_file.find('第')
    end = find_file.find('回')
    if find_file.find("一百") != -1:
        if find_file.find("九十一") != -1:
            new_name = find_file[0:(start+1)] + "191" + find_file[end:]
            os.rename(find_file, new_name)
        elif find_file.find("九十二") != -1:
            new_name = find_file[0:(start+1)] + "192" + find_file[end:]
            os.rename(find_file, new_name)
        elif find_file.find("九十三") != -1:
            new_name = find_file[0:(start+1)] + "193" + find_file[end:]
            os.rename(find_file, new_name)
        elif find_file.find("九十四") != -1:
            new_name = find_file[0:(start+1)] + "194" + find_file[end:]
            os.rename(find_file, new_name)
        elif find_file.find("九十五") != -1:
            new_name = find_file[0:(start+1)] + "195" + find_file[end:]
            os.rename(find_file, new_name)
        elif find_file.find("九十六") != -1:
            new_name = find_file[0:(start+1)] + "196" + find_file[end:]
            os.rename(find_file, new_name)
        elif find_file.find("九十七") != -1:
            new_name = find_file[0:(start + 1)] + "197" + find_file[end:]
            os.rename(find_file, new_name)
        elif find_file.find("九十八") != -1:
            new_name = find_file[0:(start+1)] + "198" + find_file[end:]
            os.rename(find_file, new_name)
        elif find_file.find("九十九") != -1:
            new_name = find_file[0:(start+1)] + "199" + find_file[end:]
            os.rename(find_file, new_name)