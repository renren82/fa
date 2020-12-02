import os
import json

path_root = 'H:/QTDownloadRadio/'
# add [ ] replace { with ,{ then remove first ,
file_name = 'download.dat' 
file_path = path_root + file_name


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


if __name__ == '__main__':
    file = open(file_path, "rb")
    fileJson = json.load(file)

    os.chdir(path_root)
    file_list = walk_file(path_root)
    for find_file in file_list:
        # print(find_file)
        i = 0
        while i < len(fileJson):
            field = fileJson[i]["uniqueId"]
            # print(type(field))
            name = fileJson[i]["programName"]
            # print(name)
            if find_file == str(field):
                print("find " + find_file)
                os.rename(find_file, name+".mp3")
                break
            i += 1

