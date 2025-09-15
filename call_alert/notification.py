import subprocess
from typing import Literal


def notify(
    title: str, message: str, *, link: str | None = None, sound: Literal['default', 'error'] | None = None
) -> None:
    args = ['terminal-notifier', '-message', message, '-title', title]
    if link:
        args += ['-open', link]
    if sound:
        args += ['-sound', sound]
    subprocess.run(args, check=True)
