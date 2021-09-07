from moviepy.editor import *

path_root = "E:/yanyan/y英语/Unlock 2e RW 2/"
path_out = "E:/yanyan/y英语/Unlock 2e RW 2_mp3/"

list_file = os.listdir(path_root)
os.chdir(path_root)
for file_name in list_file:
    # 要转换的mp4文件
    video = VideoFileClip(path_root + file_name)
    audio = video.audio
    audio.write_audiofile(path_out + file_name[:-4] + '.mp3')
