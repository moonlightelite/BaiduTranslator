# BaiduTranslator
Reverse engineered Baidu Fanyi client written in Python

This is a native Python implementation of Baidu Fanyi's JS code. 
No 'bundling V8 JS engine into Python and run Baidu Fanyi's JS code' trickery here.

Require Python modules-
  - requests
  - pywin32 (optional, only for daemon mode)

Usage:
```
$ ./translate.py -h
usage: translate.py [-h] [-i INPUT] [-o OUTPUT_LANGUAGE] [-t] [-d]

Translation using Baidu Translate.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Phrase to be translated
  -o OUTPUT_LANGUAGE, --output_language OUTPUT_LANGUAGE
                        Output language (eg. en for English, jp for Japanese,
                        zh for Chinese etc.)
  -t, --test            Test mode
  -d, --daemon          Run as daemon
```

Example-
```
$ ./translate.py -i 'Hundreds of demonstrators, a few of them armed, gathered in Lansing and many did not wear masks or socially distance.' -o zh
数百名示威者聚集在兰辛，其中一些人携带武器，许多人没有戴口罩，也没有与社会保持距离。
```

Note-
  - Require Python 3
  - Baidu has rate limiter on their server, so don't go crazy.
  - Daemon mode uses Windows named pipe to communicate with another process.

TODO-
  - Port this to C++ or Rust
  
References-
  - https://fanyi.baidu.com/
  - https://github.com/TimLuo465/baidu-translate-api
  - https://blog.csdn.net/hujingshuang/article/details/80180294
  - https://blog.csdn.net/zhu6201976/article/details/98262497
  
