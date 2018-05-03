import time
import base64
import hmac


def generate_token(key, expire=3600):
    """
    生成token
    :param key: str (用户给定的key，需要用户保存以便之后验证token,每次产生token时的key 都可以是同一个key)
    :param expire: int(最大有效时间，单位为s)
    :return: state: str(生成的token)
    """
    ts_str = str(time.time() + expire)
    ts_byte = ts_str.encode("utf-8")
    sha1_str = hmac.new(key.encode("utf-8"), ts_byte, 'sha1').hexdigest()
    token = ts_str + ':' + sha1_str
    b64_token = base64.urlsafe_b64encode(token.encode("utf-8"))
    return b64_token.decode("utf-8")


def certify_token(key, token):
    """
    验证token是否可用
    :param key: 关键字
    :param token: token
    :return: Boolean
    """
    token_str = base64.urlsafe_b64decode(token).decode('utf-8')
    token_list = token_str.split(':')
    if len(token_list) != 2:
        return False
    ts_str = token_list[0]
    if float(ts_str) < time.time():
        # token expired
        return False
    known_sha1_str = token_list[1]
    sha1 = hmac.new(key.encode("utf-8"), ts_str.encode('utf-8'), 'sha1')
    calc_sha1_str = sha1.hexdigest()
    if calc_sha1_str != known_sha1_str:
        # token certification failed
        return False
        # token certification success
    return True
