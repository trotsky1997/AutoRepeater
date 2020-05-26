#导入requests模块
import requests
import urllib.parse
class Xiaoniu(object):
    def __init__(self):

        self.headers={
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://niutrans.vip',
        'Referer': 'https://niutrans.vip/console/textTrans',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36'
        }

        self.url = 'https://test.niutrans.vip/NiuTransServer/testtrans'

    def translate(self, from_lan, to_lan, text):
        data = {
            'from' : from_lan,
            'to' : to_lan,
            'src_text': text
        }
        url = self.url
        url+='?from={}&to={}&src_text='.format(from_lan, to_lan)
        url+=urllib.parse.quote(data['src_text'])
        #print(url)
        result = requests.get(url=url,headers=self.headers)
        #print(result.text)
        if result != None:
            return result.json()['tgt_text']

def xiaoniuTrans(word,from_language='zh',to_language='en'):
    niu = Xiaoniu()
    return niu.translate(from_language,to_language,word)
if __name__ == '__main__':
        print(xiaoniuTrans("hello",from_language='en',to_language='zh'))