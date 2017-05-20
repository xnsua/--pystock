from common.helper import loop_for_seconds, play_wav
from config_module import myconfig


def alert_exception(seconds=3):
    val = ((myconfig.project_root / 'others' / 'alarm.wav').resolve())
    loop_for_seconds(lambda: play_wav(str(val)), seconds)
