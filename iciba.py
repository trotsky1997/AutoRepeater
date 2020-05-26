import urllib.request
import urllib.parse
import json

def iciba(text,from_language='zh',to_language='en'):


        url = 'http://fy.iciba.com/ajax.php?a=fy'

        data = {
        'f':from_language,
        't':to_language,
        'w':text
        }

        data = urllib.parse.urlencode(data).encode('utf - 8')
        wy = urllib.request.urlopen(url,data)
        html = wy.read().decode('utf - 8')
        ta = json.loads(html)
        return ta['content']['out']
                        
