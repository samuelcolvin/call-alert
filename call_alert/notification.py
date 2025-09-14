import subprocess


def notify(title: str, message: str) -> None:
    title = title.replace('"', '\\"')
    message = message.replace('"', '\\"')
    script = f'display notification "{message}" with title "{title}" sound name "default"'
    subprocess.run(['/usr/bin/osascript', '-e', script], check=True)
