from moviepy.editor import *

path_root = "E:/yanyan/y英语/Unlock3/"
path_out = path_root

list_file = os.listdir(path_root)
os.chdir(path_root)
for file_name in list_file:
    if file_name[-4:] == ".mp4":
        # 要转换的mp4文件
        video = VideoFileClip(path_root + file_name)
        audio = video.audio
        audio.write_audiofile(path_out + file_name[:-4] + '.mp3', bitrate="320k")
