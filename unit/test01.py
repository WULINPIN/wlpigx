import requests

url = 'http://www.zhongfu.net'
res = requests.get(url)
# print(res.content)
print(type(res.text))
# str
# print(res.headers)
for (key, value) in res.headers.items():
    print('{0}: {1}'.format(key, value))

print(res.headers['Content-Type'])
