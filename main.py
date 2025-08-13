import requests
import os
import json
from datetime import datetime

from args import args
from log import LOG

BASE_URL = "https://nideriji.cn/api/"
EMAIL = None
TOKEN = None
USER_ID = None


def login():
    global TOKEN, USER_ID
    if os.path.exists(".auth"):
        with open(".auth", "r") as f:
            login_data = json.load(f)
        LOG.info("Loaded existing authentication data.")
    else:
        payload = {
            "email": input("Email: "),
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
        LOG.info("Saved new authentication data.")

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
        try:
            _id = diary["id"]
            payload = {"diary_ids": _id}
            res = requests.post(
                url=BASE_URL + "diary/all_by_ids/" + str(USER_ID) + "/",
                data=payload,
                headers=headers,
                timeout=10,
            )
            diaries = res.json().get("diaries", [])
            if diaries:
                diary = diaries[0]
                dt_str = datetime.fromtimestamp(diary["createdtime"]).strftime(
                    "%Y-%m-%d"
                )
                title = diary["title"]
                with open(
                    f"./.data/{dt_str}-{_id}-{title}.txt", "w", encoding="utf-8"
                ) as f:
                    f.write(diary["title"] + "\n\n")
                    f.write(diary["content"])
                    LOG.info(f"Saved diary ID: {_id}")
            else:
                LOG.info(f"No diary found for ID: {_id}")
        except Exception as e:
            LOG.error(f"Error saving diary ID {_id}: {e}")
            continue


if __name__ == "__main__":
    requests.Session()

    login()
    LOG.info(f"Logged in as user ID: {USER_ID}")

    if args.save_diaries:
        save_diaries()
