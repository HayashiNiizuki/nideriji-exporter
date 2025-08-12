import requests
import json

BASE_URL = "https://nideriji.cn/api/"

if __name__ == "__main__":
    requests.Session()

    payload = {
        "email": "",
        "password": "",
    }

    res = requests.post(
        url=BASE_URL + "login/",
        data=payload,
        timeout=None,
    )

    login_data = res.json()

    payload = {"user_config_ts": 0, "diaries_ts": 0, "remark_ts": 0, "images_ts": 0}
    headers = {"auth": "token " + login_data["token"]}
    res = requests.post(
        url=BASE_URL + "v2/sync/", data=payload, headers=headers,timeout=None
    )

    print(res.json())
