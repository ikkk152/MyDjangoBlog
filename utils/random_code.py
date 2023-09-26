import random


def get_random_code() -> str:
    """
    随机生成六位验证码
    :return: code
    """
    return str(random.random())[-6:]


if __name__ == '__main__':
    print(get_random_code())
