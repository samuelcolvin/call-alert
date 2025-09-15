import subprocess


def notify(title: str, message: str, link: str | None = None) -> None:
    args = ['terminal-notifier', '-message', message, '-title', title]
    if link:
        args += ['-open', link]
    subprocess.run(args, check=True)
