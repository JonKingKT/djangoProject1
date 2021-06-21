import time
from django.core import signing
import hashlib
from django.core.cache import cache

HEADER = {'typ': 'JWP', 'alg': 'default'}
KEY = 'LIU_YAN'
SALT = 'www.antuen.com'
TIME_OUT =24 * 30 * 60  # 1 天
# TIME_OUT =10

def __encrypt(obj):
    """加密"""
    value = signing.dumps(obj, key=KEY, salt=SALT)
    value = signing.b64_encode(value.encode()).decode()
    return value


def __decrypt(src):
    """解密"""
    src = signing.b64_decode(src.encode()).decode()
    raw = signing.loads(src, key=KEY, salt=SALT)
    print(type(raw))
    return raw


def create_user_token(userphone):
    """生成token信息"""
    # 1. 加密头信息
    header = __encrypt(HEADER)
    # 2. 构造Payload
    payload = {"userphone": userphone, "iat": time.time()}
    payload = __encrypt(payload)
    # 3. 生成签名
    md5 = hashlib.md5()
    md5.update(("%s.%s" % (header, payload)).encode())
    signature = md5.hexdigest()
    token = "%s.%s.%s" % (header, payload, signature)
    # 存储到缓存中
    cache.set(userphone, token, TIME_OUT)
    return token

def create_doctor_token(doctorphone):
    """生成token信息"""
    # 1. 加密头信息
    header = __encrypt(HEADER)
    # 2. 构造Payload
    payload = {"doctorphone": doctorphone, "iat": time.time()}
    payload = __encrypt(payload)
    # 3. 生成签名
    md5 = hashlib.md5()
    md5.update(("%s.%s" % (header, payload)).encode())
    signature = md5.hexdigest()
    token = "%s.%s.%s" % (header, payload, signature)
    # 存储到缓存中
    cache.set(doctorphone, token, TIME_OUT)
    return token


def __get_payload(token):
    payload = str(token).split('.')[1]
    payload = __decrypt(payload)
    return payload


# 通过token获取用户
def get_userphone(token):
    payload = __get_payload(token)
    return payload['userphone']
    pass

# 通过token获取商家
def get_doctorphone(token):
    payload = __get_payload(token)
    return payload['doctorphone']
    pass


def check_user_token(token):
    userphone = get_userphone(token)
    last_token = cache.get(userphone)
    if last_token:
        return last_token == token
    return False

def check_doctor_token(token):
    doctorphone = get_doctorphone(token)
    last_token = cache.get(doctorphone)
    if last_token:
        return last_token == token
    return False