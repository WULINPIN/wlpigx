import time

import threadpool


def say_hello(string, verbose):
    print('Hello,{0},{1}'.format(string, verbose))
    time.sleep(2)


name_list = ['A', 'B', 'C', 'D']
#多参数传递
name_dict = [(None, {'string': 'Alice', 'verbose': 'haha'}), (None, {'string': 'Alice', 'verbose': 'haha'}),
             (None, {'string': 'Alice', 'verbose': 'haha'})]
name_lists = [(['1', '2', '3'], None), (['A', 'B', 'C'], None)]

start = time.time()
for i in range(len(name_list)):
    say_hello(name_list[i], 'verbose')
end = time.time()

print('Without Threadpool The total time is {0}'.format(end - start))
pool_start = time.time()
pool = threadpool.ThreadPool(4)
requests = threadpool.makeRequests(say_hello, name_dict)
# 当函数有多个参数的情况，函数调用时第一个解包list，第二个解包dict
[pool.putRequest(req) for req in requests]
pool.wait()
pool_end = time.time()

print('With Threadpool The total time is {0}'.format(pool_end - pool_start))
