# BaiduTranslator
Reverse engineered Baidu Fanyi client written in Python

This is a native Python implementation of Baidu Fanyi's JS code. 
No 'bundling V8 JS engine into Python and run Baidu Fanyi's JS code' trickery here.

Require Python modules-
  requests
  pywin32 (optional, only for daemon mode)

Note-
  - Require Python 3
  - Baidu has rate limiter on their server, so don't go crazy.
  - Daemon mode uses Windows named pipe to communicate with another process.

TODO-
  Port this to C++ or Rust
  
References-
  https://github.com/TimLuo465/baidu-translate-api
  https://blog.csdn.net/hujingshuang/article/details/80180294
  https://blog.csdn.net/zhu6201976/article/details/98262497
  
