import os
import re
import hashlib

from typing import Optional, List, Tuple

from app.aio import requests

from log import IS_LOGGER

isUrl = re.compile(r"^https?:\/\/")


def bot_hash(message: str) -> str:
    message = str(message)
    key = os.environ.get("ENCRYPT_KEY") or "qq_bot_is_so_niu_bi"
    key = key.encode()
    inner = hashlib.md5()
    inner.update(message.encode())
    outer = hashlib.md5()
    outer.update(inner.hexdigest().encode() + key)
    return outer.hexdigest()


async def dwz(url: str) -> Optional[str]:
    if not isUrl.match(url):
        IS_LOGGER.error("请输入正常的 url")
        raise ValueError("请输入正常的 url")

    dwz_url = "http://sa.sogou.com/gettiny?={}"

    data = {"url": url}
    r: requests.AsyncResponse = await requests.get(dwz_url, params=data)
    res = await r.text

    return res


def check_args(**kwargs) -> Tuple[bool, Optional[List[str]]]:
    msg_list = []
    for k, v in kwargs.items():
        if v is None:
            msg = f"Missing arg: {k}"
            msg_list.append(msg)
    if msg_list:
        return False, msg_list
    return True, None