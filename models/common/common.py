from pydantic import BaseModel


class CommonResponse(BaseModel):
    code: int
    success: bool
    message: str
    data: dict | None


# 定义生成响应的函数
def response_success(data: dict = None, message: str = "success") -> CommonResponse:
    return CommonResponse(code=200, message=message, data=data, success=True)


def response_fail(message: str = "fail") -> CommonResponse:
    return CommonResponse(code=400, message=message, data=None, success=False)


def test_response_success():
    return response_success(data={"test": "test"})


def test_response_fail():
    return response_fail()


# print(test_response_success())
# print(test_response_fail())
