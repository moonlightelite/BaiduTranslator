# BaiduTranslator
Reverse engineered Baidu Fanyi client written in Python

![Alt text](example.gif?raw=true "Title")

This is a native Python implementation of Baidu Fanyi's JS code. 

No 'bundling V8 JS engine into Python and run Baidu Fanyi's JS code' trickery here.

Why Baidu Fanyi? Their Chinese-Japanese/English translation is substantially better than Google Translate. For English, Baidu Fanyi is worse.

Also, there could be copyright concerns if you simply copy/paste Baidu's JS code into your program. This RE implementation is done for interoperability reason, so you probably won't infringe on Baidu's copyright.

Require Python modules-
  - requests
  - pywin32 (optional, only for daemon mode)
  
Installation-
  - Install Python 3
  - Install PIP
  - Install requests and pywin32 with PIP

Usage:
```
$ ./translate.py -h
usage: translate.py [-h] [-i INPUT] [-o OUTPUT_LANGUAGE] [-t] [-p] [-d] [-bc BAIDUCOOKIE] [-f FILE]

Translation using Baidu Translate.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Phrase to be translated
  -o OUTPUT_LANGUAGE, --output_language OUTPUT_LANGUAGE
                        Output language (eg. en for English, 'zh': '中文','jp': '日语','yue': '粤语','wyw': '文言文','cht': '中文繁体'
                        etc.)
  -t, --test            Test mode
  -p, --proxy           Use proxy file
  -d, --daemon          Run as daemon
  -bc BAIDUCOOKIE, --baiducookie BAIDUCOOKIE
                        BAIDUID cookie (xxx...:FG=1)
  -f FILE               File to be translated
```

Example-
```
$ ./translate.py -i 'Hundreds of demonstrators, a few of them armed, gathered in Lansing and many did not wear masks or socially distance.' -o zh
数百名示威者聚集在兰辛，其中一些人携带武器，许多人没有戴口罩，也没有与社会保持距离。
```

Note-
  - Require Python 3
  - Baidu has changed its cookie validation scheme. Now a new BAIDUID cookie is activated for translation only after 24 hours. This means that if you run the script for the first time, you have to wait 24 hours before the server would accept the new BAIDUID cookie. If you already have a valid cookie (eg. from a web  browser), you can enter it with --baiducookie.
  - Baidu has rate limiter on their server, so you might want to use multi-proxies mode --proxies if you need to go faster
  - Daemon mode uses Windows named pipe to communicate with another process.

TODO-
  - Port this to C++ or Rust
  
References-
  - https://fanyi.baidu.com/
  - https://github.com/TimLuo465/baidu-translate-api
  - https://blog.csdn.net/hujingshuang/article/details/80180294
  - https://blog.csdn.net/zhu6201976/article/details/98262497
  
