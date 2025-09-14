import subprocess


def notify(title: str, message: str) -> None:
    assert '"' not in title, 'Title cannot contain double quotes'
    assert '"' not in message, 'Message cannot contain double quotes'
    script = f'display notification "{message}" with title "{title}" sound name "default"'
    subprocess.run(['/usr/bin/osascript', '-e', script], check=True)
