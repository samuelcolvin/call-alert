from .camera import check_camera_active
from .notification import notify
from .text_to_speech import play_text

if __name__ == '__main__':
    print(check_camera_active())
    text = 'Testing'
    notify('Call Alert', text)
    play_text(text)
