import requests

url='http://docs.python-requests.org/en/master/'
proxies={
'http':'http://20.10.33.247:8080',
'https':'https://20.10.33.247:8080'
}
r = requests.get(url,proxies=proxies)
print(r.status_code)