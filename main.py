try:
    import translators as ts
    import PySimpleGUI as sg
    import win32clipboard
    from iciba import iciba
    from BaiduTranslate import baidu,baidudeep
    from multiprocessing.dummy import Pool as ThreadPool
    import win32con
    from sogou import translate as sogou
    from xiaoniu import xiaoniuTrans
    # Create some widgets


    def cbget():
        win32clipboard.OpenClipboard()
        data = win32clipboard.GetClipboardData(win32con.CF_TEXT)
        win32clipboard.CloseClipboard()
        return data.decode("gbk")

    def cbset(data):
        try:
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32con.CF_TEXT,data.encode('gbk'))
            win32clipboard.CloseClipboard()
        except:
            return -1

    vendors = ["raw", "google", "tencent", "alibaba",
            "youdao", "baidu", "bing", "iciba", "sougou","xiaoniu","baidu2"] #"deepl", 
    # vendors = ["raw","deepl","sougou"]
    engines = {
        "google": ts.google,
        "tencent": ts.tencent,
        "alibaba": ts.alibaba,
        "deepl": ts.deepl,
        "youdao": ts.youdao,
        "baidu": baidu,
        "bing": ts.bing,
        "iciba": iciba,
        "sougou": sogou,
        "baidu2":baidudeep,
        "xiaoniu":xiaoniuTrans,
    }

    layout = [[sg.Text("{}".format(t)+"\t"), sg.Multiline(key=t,), sg.Button("Paste\t")
            if t == "raw" else sg.Button("Copy\t")] for t in vendors]


    copy2vendor ={i:j for i,j in zip(['Copy\t' + str(i) for i in ['',]+list(range(0,len(vendors) - 2))],vendors[1:])}
    # Create the Window



    def proc(vendor):
        global val
        engine = engines[vendor]
        try:
            result = engine(engine(val,from_language='zh',to_language='en'),from_language='en',to_language='zh')
        except:
            result = 'Failed.'
        return vendor,result

    window = sg.Window('Python自动降重脚本', layout)
    if __name__=="__main__":
        while True:
            event, values = window.read()
            if event == 'Paste\t':
                val = cbget()
                window['raw'].Update(val)
                pool = ThreadPool()
                results = pool.map(proc, vendors[1:])
                pool.close()
                pool.join()
                del pool
                for i in results:
                    window[i[0]].Update(i[1])
            if event != 'Paste\t':
                cbset(window[copy2vendor[event]].Get())
            if event in (None,):
                break
        window.close()

except:
    pass