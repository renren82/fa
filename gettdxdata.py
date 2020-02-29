import struct
import os
import datetime
import math

path = './lday/'


def gettdxdaydata(file_path, name):
    data = []
    with open(file_path, 'rb') as f:
        while True:
            data_date = f.read(4)
            data_open = f.read(4)
            data_high = f.read(4)
            data_low = f.read(4)
            data_close = f.read(4)
            data_amount = f.read(4)
            data_vol = f.read(4)
            data_reservation = f.read(4)
            """
            每32个字节为一天数据
            每4个字节为一个字段，每个字段内低字节在前
            00 ~ 03 字节：年月日, 整型
            04 ~ 07 字节：open*100， 整型
            08 ~ 11 字节：high*100, 整型
            12 ~ 15 字节：low*100, 整型
            16 ~ 19 字节：close*100, 整型
            20 ~ 23 字节：amount（元），float型
            24 ~ 27 字节：vol(gu)，整型
            28 ~ 31 字节：（保留）
            """
            if not data_date:
                break

            data_date = struct.unpack("l", data_date)
            data_open = struct.unpack("l", data_open)
            data_high = struct.unpack("l", data_high)
            data_low = struct.unpack("l", data_low)
            data_close = struct.unpack("l", data_close)
            data_amount = struct.unpack("f", data_amount)
            data_vol = struct.unpack("l", data_vol)
            data_reservation = struct.unpack("l", data_reservation)
            date_format = datetime.datetime.strptime(str(data_date[0]), '%Y%M%d')  # 格式化日期
            data_list = date_format.strftime('%Y-%M-%d') + "," + str(data_open[0] / 100) + "," + str(
                data_high[0] / 100.0) + "," + str(data_low[0] / 100.0) + "," + str(data_close[0] / 100.0) + "," + str(
                data_vol[0]) + "\r\n"
            print(data_list)


def gettdxmdata(file_path, name):
    data = []
    with open(file_path, 'rb') as f:
        while True:
            num = f.read(2)
            minutes = f.read(2)
            data_open = f.read(4)
            data_high = f.read(4)
            data_low = f.read(4)
            data_close = f.read(4)
            data_amount = f.read(4)
            data_vol = f.read(4)
            data_reservation = f.read(4)
            """
            每32个字节，每字段内低字节在前
            00 ~ 01 字节：日期，整型，设其值为num，则日期计算方法为：
            year=floor(num/2048)+2004;
            month=floor(mod(num,2048)/100);
            day=mod(mod(num,2048),100);
            02 ~ 03 字节： 从0点开始至目前的分钟数，整型
            04 ~ 07 字节：open，float型
            08 ~ 11 字节：high，float型
            12 ~ 15 字节：low，float型
            16 ~ 19 字节：close，float型
            20 ~ 23 字节：amount，float型
            24 ~ 27 字节：vol，整型
            28 ~ 31 字节：（保留）
            """
            if not data_vol:
                break

            num = struct.unpack("H", num)
            minutes = struct.unpack("H", minutes)
            data_open = struct.unpack("f", data_open)
            data_high = struct.unpack("f", data_high)
            data_low = struct.unpack("f", data_low)
            data_close = struct.unpack("f", data_close)
            data_amount = struct.unpack("f", data_amount)
            data_vol = struct.unpack("l", data_vol)
            data_reservation = struct.unpack("l", data_reservation)

            year = math.floor(num[0] / 2048) + 2004
            month = math.floor((num[0] % 2048) / 100)
            day = ((num[0] % 2048) % 100)
            hour = math.floor(minutes[0] / 60)
            minute = minutes[0] % 60

            open_p = round(data_open[0], 2)
            high_p = round(data_high[0], 2)
            low_p = round(data_low[0], 2)
            close_p = round(data_close[0], 2)

            date_format = datetime.datetime.strptime(str(year) + str(format(month, '02d')) + str(day),
                                                     '%Y%M%d')  # 格式化日期
            data_list = date_format.strftime('%Y-%M-%d') + " " + str(format(hour, '02d')) + ":" \
                        + str(format(minute, '02d')) + "," + str(open_p) + "," + str(high_p) + "," + str(
                low_p) + "," + str(close_p) + "," + str(data_vol[0]) + "\r\n"
            print(data_list)


list_file = os.listdir(path)
for i in list_file:
    gettdxdaydata(path + i, i[:-4])
