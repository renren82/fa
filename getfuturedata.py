from urllib import request
import json


def get_data(id):
    url_60m = 'http://stock2.finance.sina.com.cn/futures/api/json.php/IndexService.getInnerFuturesMiniKLine5m?symbol='
    url = url_60m + id
    req = request.Request(url)
    rsp = request.urlopen(req)
    res = rsp.read()
    print(res)
    res_json = json.loads(res)

    bar_list = []

    res_json.reverse()
    print(res_json)
    for line in res_json:
        bar = {}
        bar['date'] = line[0]
        bar['open'] = float(line[1])
        bar['high'] = float(line[2])
        bar['low'] = float(line[3])
        bar['close'] = float(line[4])
        bar['vol'] = int(line[5])
        bar_list.append(bar)

    print(bar_list)


if __name__ == '__main__':
    get_data('M0')
