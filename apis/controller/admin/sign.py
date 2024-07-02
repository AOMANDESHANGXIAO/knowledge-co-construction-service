from models.table_def import Admin
from models.common.common import CommonResponse, response_success, response_fail
from models.admin.adminer import AdminerSignInParams, AdminerSignInResponse, AdminerSignUpParams
from db.session import SessionLocal
from utils.psd_handler import hash_password, verify_password
from utils.jwt_handler import create_access_token, verify_token


def admin_sign_in(params: AdminerSignInParams) -> CommonResponse:
    session = SessionLocal()

    try:
        db_admin = session.query(Admin).filter(Admin.username == params.username).first()

        if db_admin is None:
            return response_fail("账号不存在")

        if not verify_password(params.password, db_admin.password):
            return response_fail("密码错误")

        response_data = AdminerSignInResponse(
            nickname=db_admin.nickname,
            id=db_admin.id,
            token=create_access_token({"username": db_admin.username})
        ).__dict__

        return response_success(data=response_data, message="欢迎回来")
    except Exception as e:
        return response_fail(message=str(e))
    finally:
        session.close()


def admin_sign_up(params: AdminerSignUpParams) -> CommonResponse:
    session = SessionLocal()
    try:
        db_admin = session.query(Admin).filter(Admin.username == params.username).first()

        if db_admin is not None:
            return response_fail("账号已存在")

        db_admin = Admin(
            username=params.username,
            password=hash_password(params.password),
            nickname=params.nickname
        )

        session.add(db_admin)
        session.commit()

        return response_success(message="成功添加管理员")
    except Exception as e:
        return response_fail(message=str(e))
    finally:
        session.close()
