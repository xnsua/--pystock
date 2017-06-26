from common.audio.wav import play_wav
from common.helper import dt_now
from project_helper.config_module import myconfig


def alert_exception(seconds=3):
    val = ((myconfig.project_root / 'others' / 'alarm.wav').resolve())
    start_dt = dt_now()
    while (dt_now() - start_dt).total_seconds() < seconds:
        play_wav(str(val))
