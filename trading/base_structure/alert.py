from common.audio.wav import play_wav
from common.helper import loop_for_seconds
from project_helper.config_module import myconfig


def alert_exception(seconds=3):
    val = ((myconfig.project_root / 'others' / 'alarm.wav').resolve())
    loop_for_seconds(lambda: play_wav(str(val)), seconds)
