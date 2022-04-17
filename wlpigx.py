# -*- coding: UTF-8 -*-
import argparse
import json
import os
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'}


# global proxise
# proxise = {'http': 'http://20.10.33.247:8080',
#            'https': 'https://20.10.33.247:8080'}


def addHead():
    pass


def responseHeadFormat(responseHead):
    for (key, value) in responseHead.items():
        print('{0}: {1}'.format(key, value))


# read host list from file;
def obtainHost(filePath):
    with open(filePath) as f:
        line = f.readlines()
        for index in range(len(line)):
            line[index] = line[index].strip("\n")
        f.close()
        return line


def parseParameter():
    # Use a breakpoint in the code line below to debug your script.
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--thread', type=int, help='Set the thread (default: 20)', dest='thread', default=20)
    # parser.add_argument('-d', '--delay', type=int, help='Seconds between requests to the same host (defaut: 2)',
    #                     dest='delay', default=5000)
    parser.add_argument('-c', '--statuscode', type=int, help='The response status code, if not set print ALL',
                        dest='scode', default=0)
    parser.add_argument('-m', '--method', type=str, help='Set the request method', dest='method', default='GET')
    parser.add_argument('-to', '--timeout', type=int, help='Set the HTTP timeout (default: 5)', dest='timeout',
                        default=5)
    parser.add_argument('-ct', '--contentType', type=str, help='Set the response Content-Type', dest='contentype',
                        default='text/html')
    parser.add_argument('-w', '--workplace', type=str, help='Set the output file where save result,default (./output)',
                        dest='workplace',
                        default='./output')
    parser.add_argument('-f', '--filter', type=str, help='Filter the response content', dest='filter')
    parser.add_argument('-H', '--header', type=str, help='Add http header', dest='header')
    parser.add_argument('-p', '--path', type=str, help='URL path', dest='path', default='')
    parser.add_argument('--proxy', type=str, help='Set proxy', dest='proxy', )
    parser.add_argument('--data', help='Post data', dest='data', default=None)
    args = parser.parse_args()

    global thread
    thread = args.thread
    global scode
    scode = args.scode
    global method
    method = args.method
    global timeout
    timeout = args.timeout
    global contentype
    contentype = args.contentype
    global workplace
    workplace = args.workplace
    global filter
    filter = args.filter
    global header
    header = json.loads(args.header)
    global path
    path = args.path
    global data
    data = args.data
    global proxies
    proxy = args.proxy
    if proxy:
        try:
            proxies = {'http': 'http://' + proxy, 'https': 'https://' + proxy}
        except Exception as e:
            pass
    else:
        proxies = None


host_lists = obtainHost('./hosts')
global INDEX
INDEX = 0


def printAll(url):
    try:
        response = requests.get(url, headers=headers, timeout=timeout, proxies=proxies)
        title = re.findall(r"<title.*?>(.+?)</title>", response.text, re.S)
        title = ''.join(title).strip()
        print('{1}, \033[1;32m({0})\033[0m Content-Length: {2},Title: [{3}]'.format(response.status_code, url,
                                                                                    response.headers['Content-Length'],
                                                                                    title))
        # INDEX += 1
        # Oh my god, it's worst!
    except Exception as e:
        print(url + '\033[1;31m (Timeout) \033[0m')


def handleHttp(host, header, method, contentype, scode, path, filter, timeout, workplace, data=None, proxy=None):
    if header:
        headers.update(header)
        # this will replace old header
        url = "".join(host) + path
        if method == 'GET':
            if scode == 0:
                printAll(url)
            # request method satisfy
            # response = requests.get(url, headers=headers, timeout=timeout, proxies=proxise)
            else:
                response = requests.get(url, headers=headers, timeout=timeout, proxies=proxy)
                contentL = response.headers['Content-Length']
                title = re.findall(r"<title.*?>(.*?)</title>", response.text, re.S)
                title = ''.join(title).strip()
                if contentype and contentype in response.headers['Content-Type']:
                    # response content-type satisfy
                    if response.status_code == scode:
                        # response statuscode satisfy
                        content = response.text + str(response.headers)
                        if response.text.find(filter):
                            # 如何保存等待解决
                            print("{0} \033[1;33m[命中] HIT!\033[0m ".format(url))
                            with open(workplace, 'a') as f:
                                f.write(url + ' ' + contentL + ' [' + title + ']' + '\n')
                                f.close()


        elif method == 'POST':
            if scode == 0:
                printAll(url)
            # response = requests.post(url, data='test', headers=headers, timeout=timeout, proxies=proxise)
            response = requests.post(url, data=data, headers=headers, timeout=timeout, proxies=proxy)
            contentL = response.headers['Content-Length']
            title = re.findall(r"<title.*?>(.*?)</title>", response.text, re.S)
            if contentype and contentype in response.headers['Content-Type']:
                # response content-type satisfy
                if response.status_code == scode:
                    # response statuscode satisfy
                    content = response.text + str(response.headers)
                    if content.find(filter):
                        # 如何保存等待以后解决
                        print("{0} \033[1;33m[命中] HIT!\033[0m".format(url))
                        with open(workplace, 'a') as f:
                            f.write(url + ' ' + contentL + ' [' + title + ']' + '\n')
                            f.close()


def main():
    parseParameter()
    if os.path.exists(workplace):
        os.remove(workplace)
    # First is delete last result
    obj_list = []
    with ThreadPoolExecutor(thread) as executor:
        for host in host_lists:
            obj = executor.submit(handleHttp, host, header, method, contentype, scode, path, filter, timeout, workplace,
                                  data, proxies)
            obj_list.append(obj)
        for task in as_completed(obj_list):
            pass


if __name__ == '__main__':
    main()
