from typing import Optional

from nonebot import CommandSession, on_command

from app.services.user import UserService

__plugin_name__ = "取消绑定教务处(命令：unbind)"
__plugin_usage__ = r"""取消绑定教务处
使用方法：向我发送以下指令。
    unbind
    取消绑定
    解绑
    """


@on_command("unbind", aliases=("解绑", "取消绑定", "取消绑定教务处"))
async def unbind(session: CommandSession):
    sender_qq: Optional[str] = session.event.get("user_id")
    if sender_qq:
        r = await UserService.unbind(sender_qq)
        if r:
            resp = r.json()
            session.finish(resp["msg"])
