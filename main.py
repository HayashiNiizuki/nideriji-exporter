import requests
import os
import json

BASE_URL = "https://nideriji.cn/api/"
EMAIL = "liupingcnjs@qq.com"
TOKEN = None
USER_ID = None


def login():
    global TOKEN, USER_ID
    if os.path.exists(".auth"):
        with open(".auth", "r") as f:
            login_data = json.load(f)
    else:
        payload = {
            "email": EMAIL,
            "password": input("Password: "),
        }

        res = requests.post(
            url=BASE_URL + "login/",
            data=payload,
            timeout=None,
        )

        login_data = res.json()
        with open(".auth", "w") as f:
            json.dump(login_data, f)

    TOKEN = login_data["token"]
    USER_ID = login_data["userid"]


def save_diaries():
    os.makedirs("./.data/", exist_ok=True)

    payload = {"user_config_ts": 0, "diaries_ts": 0, "remark_ts": 0, "images_ts": 0}
    headers = {"auth": "token " + TOKEN}
    res = requests.post(
        url=BASE_URL + "v2/sync/", data=payload, headers=headers, timeout=None
    )

    diaries = res.json()["diaries"]
    for diary in diaries:
        id = diary["id"]
        payload = {"diary_ids": id}
        res = requests.post(
            url=BASE_URL + "diary/all_by_ids/" + str(USER_ID) + "/",
            data=payload,
            headers=headers,
            timeout=10,
        )
        diaries = res.json().get("diaries", [])
        if diaries:
            diary = diaries[0]
            with open(
                f"./.data/" + str(diary["createdtime"]) + ".txt", "w", encoding="utf-8"
            ) as f:
                f.write(diary["content"])
                print(f"Saved diary ID: {id}")
        else:
            print(f"No diary found for ID: {id}")


if __name__ == "__main__":
    requests.Session()

    login()
    save_diaries()
