import re
import requests        # 导入requests包

proxies = {'http':'http://192.168.0.197:7890'}
strhtml = requests.get('http://141.164.39.132:5005/',timeout=20)
# strhtml.encoding='utf-8'# Get方式获取网页数据
print(re.findall(r"<title.*?>(.+?)</title>", strhtml.text,re.S))
# print(strhtml.text)