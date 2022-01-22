import asyncio
import pkgutil

import yaml
from graia.ariadne.app import Ariadne
from graia.ariadne.model import MiraiSession
from graia.broadcast import Broadcast
from graia.saya import Saya
from graia.saya.builtins.broadcast import BroadcastBehaviour

with open("config.yml", "r", encoding="UTF-8") as f:
    connect_info = yaml.safe_load(f)

loop = asyncio.new_event_loop()
bcc = Broadcast(loop=loop)
app = Ariadne(broadcast=bcc, connect_info=MiraiSession(**connect_info))
saya = Saya(bcc)
saya.install_behaviours(BroadcastBehaviour(bcc))

with saya.module_context():
    for module_info in pkgutil.iter_modules(["modules"]):
        if module_info.name.startswith("_"):
            continue
        saya.require("modules." + module_info.name)

app.launch_blocking()
