import time
from concurrent.futures import ThreadPoolExecutor,as_completed


def outPut(name, gender, age):
    print('My name is {0}, {1}, {2} years old!'.format(name, gender, age))
    time.sleep(2)


def outPut1(name):
    print('My name is {0}'.format(name))
    time.sleep(3)


def main():
    names = ['zhangsan', 'lisi', 'wangwu', 'aaa', 'bbb', 'cccd', 'eeee']
    # name_list = [()]
    start = time.time()
    gender = 'female'
    age = 12
    with ThreadPoolExecutor(10) as executor:
        for name in names:
            executor.submit(outPut, name, gender, age)
    end = time.time()
    print("Submit function total time is {0}".format(end - start))


if __name__ == '__main__':
    main()
