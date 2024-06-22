import jwt
import datetime

# JWT 配置
SECRET_KEY = "my_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300


def timestamp_to_date(timestamp):
    """
    将时间戳转换为日期字符串。

    参数:
    - timestamp: int or float，表示时间戳的整数或浮点数。

    返回:
    - str，格式化的日期字符串。
    """
    # 时间戳转为datetime对象
    date_obj = datetime.datetime.fromtimestamp(timestamp)

    # 格式化日期字符串，例如："2023-04-01 12:34:56"
    formatted_date = date_obj.strftime("%Y-%m-%d %H:%M:%S")

    # 转换为datetime对象
    date_obj = datetime.datetime.strptime(formatted_date, "%Y-%m-%d %H:%M:%S")
    return date_obj


def create_access_token(data: dict, expires_delta: datetime.timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> bool:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        if datetime.datetime.utcnow() < timestamp_to_date(payload.get("exp")):
            return True
        if not payload.get("username"):
            return False
        return False
    except jwt.ExpiredSignatureError:
        return False


def test_create_access_token():
    data = {"username": "test_user"}
    token = create_access_token(data)
    print(token)


def test_verify_token():
    token = create_access_token({"username": "test_user"})
    print(verify_token(token))

