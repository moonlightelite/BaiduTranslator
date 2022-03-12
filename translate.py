#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# Copyright (c) 2020 moonlightelite
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import sys,os
import re
import requests
import argparse
import pickle
import time
import urllib.parse
import sqlite3
import random

#python -m pip install requests[socks]

HAVE_PYWIN32 = True
proxy_mode = False
# 21CC57D3BED68561D5B35D36D4DB320:FG=1
# 2BAFEECEB9E308C84DEFCF6B2DB9EB4D:FG=1
baidu_cookie = "" #

proxies_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'translation-baidu.proxies')
cookies_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'translation-baidu.cookie')
try:
    import win32pipe, win32file, pywintypes
except:
    print("pywin32 module not available. Skipping.")
    HAVE_PYWIN32 = False

class BaiduDecoder():
    i = None
    gtk = None
    
    def __init__(self, gtk):
        self.gtk = gtk
        
    def zero_fill_right_shift(self, val, n):
        return (val >> n) if val >= 0 else ((val + 0x100000000) >> n)
        
    def n(self, r, o):
        for t in range(0, len(o) - 2, 3):
            a = o[t + 2]
            if a >= "a":
                a = ord(a) - 87
            else:
                a = int(a)
            if o[t + 1] == "+":
                a = self.zero_fill_right_shift(r, a)
            else:
                a = r << a
            if o[t] == "+":
                r = r + a & 4294967295
            else:
                r^=a
        if r > 0x7fffffff:
            r = r - 0xffffffff - 1
        return r
        
    def e(self, r):
        o = re.match("[\uD800-\uDBFF][\uDC00-\uDFFF]", r)
        if not o:
            t = len(r)
            if t > 30:
                r = "" + r[0:10] + r[int(t/2) - 5:10 + int(t/2) - 5] + r[-10:]
        else:
            e = re.split("[\uD800-\uDBFF][\uDC00-\uDFFF]", r)
            h = len(e)
            f = []
            for C in range(h):
                try:
                    if e[C]:
                        f = f + e[C].split("")
                except:
                    pass
                if C != h - 1:
                    f.append(o[C])
            g = len(f)
            if g > 30:
                r = "".join(x for x in f[0:10]) + "".join(x for x in f[Math.floor(g / 2) - 5:Math.floor(g / 2) + 5]) + \
                    "".join(x for x in f[-10:])
        u = 0
        if self.i:
            u = self.i
        else:
            if self.gtk:
                u = self.gtk
            else:
                u = ""
        d = u.split(".")
        m = s = c = 0
        try:
            m = int(d[0])
        except:
            m = 0
        try:
            s = int(d[1])
        except:
            s = 0
        S = {}
        for v in range(len(r)):
            A = ord(r[v])
            if 128 > A:
                S[c] = A
                c+=1
            else:
                if 2048 > A:
                    S[c] = A >> 6 | 192
                    c+=1
                else:
                    if (64512 & A) == 55296 and v + 1 < len(r) and (64512 & ord(r[v + 1])) == 56321:
                        v+=1
                        A = 65536 + ((1023 & A) << 10) + (1023 & ord(r[v]))
                        S[c] = A >> 18 | 240,
                        c+=1
                        S[c] = A >> 12 & 63 | 128
                        c+=1
                    else:
                        S[c] = A >> 12 | 224
                        c+=1
                        S[c] = A >> 6 & 63 | 128
                        c+=1
                    S[c] = 63 & A | 128
                    c+=1
        p = m
        F = "+-a^+6"
        D = "+-3^+b+-f"
        for b in range(len(S)):
            p += S[b]
            p = self.n(p, F)
        p = self.n(p, D)
        p ^= s
        if 0 > p:
            p = (2147483647 & p) + 2147483648
        p %= 1e6
        return str(int(p)) + "." + str(int(p) ^ m)


class TranslationException(Exception):
    def __init__(self, message):
        super().__init__(message)


class BaiduTranslate():
    url_root = "https://fanyi.baidu.com/"
    url_langdetect = "https://fanyi.baidu.com/langdetect"
    url_v2transapi = "https://fanyi.baidu.com/v2transapi"
    headers = {
        "origin": "https://fanyi.baidu.com",
        "referer": "https://fanyi.baidu.com",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
    }
    cookies = {}
    cache = {}
    conn = None

    def __init__(self, input_lang=None, output_lang="en"):
        self.input_lang = input_lang
        self.output_lang = output_lang

        self.session = requests.session()
        self.session.headers = self.headers

        self.set_proxies()
        self.set_cookies()
        self.token, self.gtk = self.get_gtk_token()
        self.setupSQLite()
        
    def set_proxies(self):
        if proxy_mode and os.path.exists(proxies_file):
            with open(proxies_file, 'r') as fd:
                self.proxies = [x.strip() for x in fd.readlines()]
        else:
            self.proxies = None
        
    def pick_proxy(self):
        p = random.choice(self.proxies)
        proxies = {
            'http': p,
            'https': p
        }
        return proxies
        
    def set_cookies(self):
        if not os.path.exists(cookies_file):
            page = self.session.get(self.url_root)
            self.cookies = page.cookies
        else:
            with open(cookies_file, 'rb') as fd:
                self.cookies = pickle.load(fd)
        if baidu_cookie:
            self.cookies.set('BAIDUID', baidu_cookie, domain=".baidu.com", path="/")
            with open(cookies_file, 'wb') as fd:
                pickle.dump(self.cookies, fd)

    def get_gtk_token(self):
        response = self.session.get(self.url_root, cookies=self.cookies)
        response = response.content.decode()
    
        token = re.findall(r"\stoken: '(.+)'", response)[0]
        gtk = re.findall(r";window.gtk = '(.+)';", response)[0]

        return token, gtk

    def detect_lang(self, input_string):
        data_langdetect = {
            "query": input_string
        }
        try:
            response = self.session.post(self.url_langdetect, data=data_langdetect)
            response_dict = response.json()
            if response_dict["error"] == 0:
                return response_dict["lan"]
        except Exception as e:
            print(e)

    def setupSQLite(self):
        self.conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'translation.db'))
        c = self.conn.cursor()

        try:
            c.execute('''CREATE TABLE translation
                 (input_text, output_text)''')
            self.conn.commit()
        except sqlite3.OperationalError:
            pass

    def translate(self, input_string, input_lang=None, output_lang=None):
        try:
            if not input_string.strip():
                return " "
            return self._translate(input_string, input_lang, output_lang)
            #return "\n".join([self._translate(x, input_lang, output_lang) for x in input_string.splitlines()])
        except Exception as e:
            print(e)
            return " "

    def _translate(self, input_string, input_lang=None, output_lang=None, retry=False):
        c = self.conn.cursor()
        if not input_lang:
            if not self.input_lang:
                input_lang = self.detect_lang(input_string)
            elif self.input_lang:
                input_lang = self.input_lang

        if not output_lang:
            output_lang = self.output_lang

        if not self.cache.get(input_lang + output_lang, None):
            self.cache[input_lang + output_lang] = {}
        if self.cache[input_lang + output_lang].get(input_string, None):
            return self.cache[input_lang + output_lang].get(input_string)
        input_text = (input_string)
        c.execute('SELECT output_text FROM translation WHERE input_text=?', (input_string,))
        output_text = c.fetchone()
        if output_text:
            return output_text[0]

        decoder = BaiduDecoder(self.gtk)
        sign = decoder.e(input_string)

        try:
            data = {
                "from": input_lang,
                "to": output_lang,
                "query": input_string, # urllib.parse.quote_plus(input_string)
                "domain": "common",
                "simple_means_flag": 3,
                "sign": sign,  
                "token": self.token,
            }
            
            if proxy_mode:
                proxy = self.pick_proxy()
            else:
                proxy = None
            response = self.session.post(self.url_v2transapi + "?from=" + input_lang + "&to=" + output_lang, data=data, cookies=self.cookies, proxies=proxy)
            
            response_dict = response.json()

            if "error" in response_dict.keys() and not retry:
                raise (TranslationException(response_dict))

            trans = "\n".join(x for x in map(lambda x: x["dst"], response_dict["trans_result"]["data"]))

            if not self.cache[input_lang + output_lang].get(input_string, None):
                self.cache[input_lang + output_lang][input_string] = trans
            if not output_text:
                c.execute('INSERT INTO translation(input_text,output_text) VALUES (?,?)', (input_string, trans))
                self.conn.commit()
            return trans
        except TranslationException as e:
            #print("Translation error. Resetting keys")
            self.token, self.gtk = self.get_gtk_token()
            return self._translate(input_string, input_lang, output_lang, retry=True)
        except Exception as e:
            print(e)


def named_pipe_server(baidu_translate):
    while True:
        print("Named_Pipe_Server starting.")
        try:
            # Create named pipe
            pipe = win32pipe.CreateNamedPipe(r'\\.\pipe\BAIDU_TRANSLATE', 
                win32pipe.PIPE_ACCESS_DUPLEX,
                win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
                win32pipe.PIPE_UNLIMITED_INSTANCES, 65536, 65536, 0, None)
            print("Named Pipe is created. Waiting for Client to connect.")
            # Enable named pipe and wait for client connection
            win32pipe.ConnectNamedPipe(pipe, None)
            print("Client is connected.")
            cont = True
            count = 0
            phase = fromLang = toLang = None
            while cont:
                # Accept std::wstring or TCHAR
                resp = win32file.ReadFile(pipe, 65536)
                encoding = None
                if resp[1][1] != 0:
                    encoding = 'utf-8'
                else:
                    encoding = 'utf-16LE' # No BOM
                msg = resp[1].decode(encoding)
                info = re.findall(r"^\[Message #\d+,to=(.*),from=(.*)\](.+)$", msg)
                toLang = info[0][0]
                fromLang = info[0][1]
                phase = urllib.parse.unquote(info[0][2])
                print(f"Phase: {phase}")
                try:
                    if phase and "×" in phase:
                        phase = phase.replace("×", "ン")
                    if phase:
                        data = baidu_translate.translate(phase, input_lang=fromLang, output_lang=toLang)
                except Exception as e:
                    raise e
                print(f"Translated: {data}")
                try:
                    data = data.encode(encoding)
                except:
                    data = "failed".encode(encoding)
                err, bytes_written=win32file.WriteFile(
                    pipe, 
                    data
                )
                count+=1
                print(f"WriteFile Return Code: {err}, Number of Bytes Written: {bytes_written}")
                if err:
                    cont = False
        except pywintypes.error as e:
            print(e)
        finally:
            print("Server exiting")
            if pipe:
                # Ensure all data read by client
                win32file.FlushFileBuffers(pipe)
                # Disconnect the named pipe
                win32pipe.DisconnectNamedPipe(pipe)
                # CLose the named pipe
                win32file.CloseHandle(pipe)
        print(f"Server ended.")


def test(baidu):
    samples = ["""2000年時，香港島人口有1,367,900人，約佔全港人口19%。人口密度每平方公里18,000人，高於整體密度（每平方公里7,000人）。
    如果單以島嶼的比較，香港島是全香港人口最多的島，也是中華人民共和國第三最多常住人口的島，僅次於海南島和廈門島（詳見中國島嶼）。""",
    """一天睡3小時、還能4天不休息，周揚青質疑小豬為了約人不睡覺，
    過往受訪片段出爐，羅志祥曾自曝體力好、健檢報告精采，讓網友瞬間理解「時間管理」能力。"""]

    print(samples[0], "\n", baidu.translate(samples[0]), "\n\n")
    print(samples[1], "\n", baidu.translate(samples[1], output_lang="jp"), "\n\n")

def run(args):
    if args.proxy:
        global proxy_mode
        proxy_mode = True
    if args.baiducookie:
        global baidu_cookie
        baidu_cookie = args.baiducookie
        
    baidu = BaiduTranslate()
    if args.test:
        test(baidu)
        sys.exit(0)
    elif args.daemon:
        if not HAVE_PYWIN32:
            print("Name pipe module not available. Exiting.")
            sys.exit(-1)
        named_pipe_server(baidu)
        sys.exit(0)
    elif args.input:
        print(baidu.translate(args.input, output_lang=args.output_language))
        sys.exit(0)
    elif args.filename:
        for line in args.filename:
            l = line.strip()
            if not l:
                continue
            print(l, "\n", baidu.translate(l, output_lang=args.output_language).strip(), "\n")
            time.sleep(1)
        sys.exit(0)
        
def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return open(arg, 'r')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Translation using Baidu Translate.')
    parser.add_argument('-i', '--input', help='Phrase to be translated', type=str)
    parser.add_argument('-o', '--output_language', help="Output language (eg. en for English, 'zh': '中文','jp': '日语','yue': '粤语','wyw': '文言文','cht': '中文繁体' etc.)", default="en")
    parser.add_argument('-t', '--test', help='Test mode', default=False, action='store_true')
    parser.add_argument('-p', '--proxy', help='Use proxy file', default=False, action='store_true')
    parser.add_argument('-d', '--daemon', help='Run as daemon', default=False, action='store_true')
    parser.add_argument('-bc', '--baiducookie', help='BAIDUID cookie (xxx...:FG=1)', type=str)
    parser.add_argument("-f", dest="filename", required=False,
                    help="File to be translated", metavar="FILE",
                    type=lambda x: is_valid_file(parser, x))
    args = parser.parse_args()

    run(args)
