from rqalpha import update_bundle

from common.helper import dt_from_time
from common.sched_with_datetime import SchedulerWithDt
from stock_data_updater.data_updater_logger import updatelog
from stock_data_updater.day_data_updater import DayBarUpdater


def run_in_background():
    shed = SchedulerWithDt()

    def heart_beat():
        updatelog.info('Schedule is running...')
        shed.enter(3, 1, heart_beat)

    shed.enter(0, 1, heart_beat)

    shed.enterabs_dt(dt_from_time(17, 40, 10), 1, DayBarUpdater.update_all)
    shed.enterabs_dt(dt_from_time(21, 38, 30), 1, DayBarUpdater.update_all)
    shed.run()


def main():

    # run_in_background()
    update_bundle()


if __name__ == '__main__':
    main()
