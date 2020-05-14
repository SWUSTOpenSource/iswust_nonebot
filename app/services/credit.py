from typing import Optional

from nonebot import get_bot

from app.libs.aio import run_sync_func
from app.libs.scheduler import add_job
from app.models.user import User
from app.utils.bot_common import qq2event
from app.utils.parse.credit_progress import get_credit_progress


class CreditService:
    @classmethod
    async def get_progress(cls, qq: int) -> Optional[str]:
        # 先查 user 出来，再查 Course 表
        user = await User.check(qq)
        if not user:
            return "NOT_BIND"
        await add_job(cls.update_progress, args=[qq])
        return "WAIT"

    @classmethod
    async def update_progress(cls, qq: int):
        user: User = await User.get(str(qq))
        if not user:
            return
        from auth_swust import request as login_request

        cookies = await User.get_cookies(qq)
        sess = login_request.Session(cookies)
        res = await run_sync_func(get_credit_progress, sess)
        _bot = get_bot()
        if res:
            await _bot.send(qq2event(qq), _format(res))
            return
        await _bot.send(qq2event(qq), "查询绩点出错，请稍后再试")


def _format(credits: dict):
    msg = ""
    for name, credit in credits.items():
        msg = msg + f"{name}: {credit}\n"
    return msg.strip()