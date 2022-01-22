import secrets

from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Image
from graia.ariadne.message.parser.twilight import (
    FullMatch,
    RegexMatch,
    Twilight,
    UnionMatch,
)
from graia.ariadne.model import Group
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

channel = Channel.current()


@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage],
        inline_dispatchers=[
            Twilight(
                match={
                    "header": UnionMatch("https://github.com/", "github.com/"),
                    "owner": RegexMatch(r"[a-zA-Z0-9][a-zA-Z0-9\-]*"),
                    "slash": FullMatch("/"),
                    "repo": RegexMatch(r"([a-zA-Z0-9_\-\.]+)$"),
                }
            )
        ],
    )
)
async def github_repo(
    app: Ariadne,
    group: Group,
    repo: RegexMatch,
    owner: RegexMatch,
):
    await app.sendGroupMessage(
        group,
        MessageChain.create(
            Image(
                url=(
                    "https://opengraph.githubassets.com/"
                    f"{secrets.token_urlsafe(16)}/{str(owner.result)}/{str(repo.result)}"
                )
            )
        ),
    )
