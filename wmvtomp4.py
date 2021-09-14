from ffmpy3 import FFmpeg

input_file = "E:/yanyan/y英语/unlock3/unlock3_unit3_L1.wmv"
output_file = input_file[:-4] + ".mp4"

ff = FFmpeg(inputs={input_file: None}, outputs={output_file: None})
ff.cmd
ff.run()
