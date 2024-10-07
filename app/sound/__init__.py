import os
from dotenv import load_dotenv

load_dotenv()

boot = os.getenv("BOOT")


def sound():
    """
    サウンドシステムを環境に応じて初期化する
    """
    if boot == "raspberrypi":
        from app.sound.bibideba import Bibideba

        return Bibideba()
    elif boot == "macos":
        from app.sound.sound import Sound

        return Sound()
    else:
        from app.sound.sound_mock import SoundMock

        return SoundMock()
