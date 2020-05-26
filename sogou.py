
import re
import json
import time
import hashlib
import requests
import argparse

# 版本号
__version__ = '1.0.0'

headers = {
    'content-type': "application/x-www-form-urlencoded",
    'accept': "application/json"
    }

# 搜狗申请的pid和key
PID = 'd2dcca8dea30c3dc0570788c204f5b8a'
Key = '475af5d76c46584ec5d35493b92f255b'

# d2dcca8dea30c3dc0570788c204f5b8a', '475af5d76c46584ec5d35493b92f255b


def parse():
    """
    解析命令行参数
    :return: parser
    """
    parser = argparse.ArgumentParser(description='the usage of Sougou-Dict command line')
    parser.add_argument('-v', '--version', action='store_true', help="show current version")
    parser.add_argument('word', nargs='*', help='word or phrase you want to translate ')
    return parser


def main():
    """
    设置可选参数和位置参数
    :return: None
    """
    parser = parse()
    args = vars(parser.parse_args())

    if args['version']:
        print(__version__)
        return

    if args['word']:
        translate(' '.join(args['word']))
        return

    parser.print_help()


def translate(word,*args, **kwargs):
    """
    调用搜狗api查询结果，并打印在终端
    :param word: query word
    :return: result
    """
    url = "http://fanyi.sogou.com:80/reventondc/api/sogouTranslate"
    salt = str(int(time.time()))
    q = word

    md5_sign = PID + q + salt + Key
    sign = hashlib.md5(md5_sign.encode('utf-8')).hexdigest()

    # 检测输入中是否含有中文，只要有中文，一律默认翻译成英文
    # 中文字符编码范围： \u4e00 - \u9fa5
    # 文档有写可以auto自动识别，不知为何会一直报错，暂时先使用这种笨办法
    zh = re.compile(u'[\u4e00-\u9fa5]')
    match = zh.search(q)
    if match:
        type_from = 'zh-CHS'
        type_to = 'en'
    else:
        type_from = 'en'
        type_to = 'zh-CHS'

    payload = "from={}&to={}&pid={}&q={}&sign={}&salt={}".format(type_from, type_to, PID, q, sign, salt)
    response = requests.post(url, data=payload.encode('utf8'), headers=headers)
    response.encoding = 'utf-8'
    output = json.loads(response.text)
    # print(output)
    if output['errorCode'] == '0':

        # print('\n基本释义:\n\t>>> {}:'.format(output['query']), output['translation'], "<<<")
        return output['translation']
    else:
        print('Unexpected error occured！errorCode:{}'.format(output['errorCode']))


if __name__ == "__main__":
    main()