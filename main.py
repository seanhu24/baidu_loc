import csv
import config
import requests
import json


def get_location(addr, city):
    ak = config.ak
    url = 'http://api.map.baidu.com/geocoder/v2/?address=%s&city=%s&output=json&ak=%s' % (
        addr, city, ak)
    resp = requests.get(url)
    result = dict(json.loads(resp.text))
    return result


def read_csv(filename):
    with open(filename, 'r', encoding='GBK') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            yield dict(row)


def write_csv(filename, content):
    with open(filename, 'w', encoding='GBK', newline='') as csvfile:
        headers = [k for k in content[0]]
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        writer.writerows(content)


if __name__ == '__main__':
    banks = read_csv('bankinfo.csv')
    res = []
    for bank in banks:
        ret = get_location(bank.get('地址'), bank.get('机构所在地区名称'))
        # print(ret)
        res.append({'机构名称': bank.get('机构名称'),
                    '地址': bank.get('地址'),
                    '经度值': ret.get('result').get('location').get('lng'),
                    '纬度值': ret.get('result').get('location').get('lat'),
                    '地址理解程度': ret.get('result').get('comprehension')})

    write_csv('地址信息.csv', res)
