from pocketbase import PocketBase
import jwt
from exchange.utility import log_message, log_error_message, settings
import time
import traceback

pb = PocketBase("http://127.0.0.1:8090")


def auth():
    try:
        DB_ID = settings.DB_ID
        DB_PASSWORD = settings.DB_PASSWORD
        # 새 버전 PocketBase API 사용
        pb.collection("_superusers").auth_with_password(DB_ID, DB_PASSWORD)
    except Exception as e:
        try:
            # 이전 버전 API 시도
            pb.admins.auth_with_password(DB_ID, DB_PASSWORD)
        except Exception as e2:
            print(f"PocketBase 연결 실패: {e2}")
            # PocketBase 연결 실패시 무시하고 계속 진행
            pass


def reauth():
    try:
        token = pb.auth_store.base_token
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        expire_time = decoded_token["exp"]
        current_time = int(time.time())
        if current_time > expire_time:
            auth()
    except:
        print("PocketBase 재인증 실패")
        pass


def create(collection, data):
    try:
        reauth()
        pb.collection(collection).create(data)
    except:
        print("PocketBase create 실패")
        pass


def delete(collection, id):
    try:
        reauth()
        pb.collection(collection).delete(id)
    except:
        raise Exception("DB delete error")


def get_full_list(collection, batch_size=200, query_params=None):
    try:
        reauth()
        return pb.collection(collection).get_full_list(
            batch=batch_size, query_params=query_params
        )
    except:
        raise Exception("DB get_full_list error")


try:
    auth()
except:
    log_error_message(traceback.format_exc(), "DB auth error")
