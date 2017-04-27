from pathlib import Path

from PyQt5.QtCore import QObject, QRunnable, pyqtSignal


class WorkerSignals(QObject):
    result = pyqtSignal(int)


# region Description
class Tasks(QObject):
    def __init__(self):
        super(Tasks, self).__init__()

    @staticmethod
    def process_result(task):
        print('Receiving', task)


# endregion


class Worker(QRunnable):
    def __init__(self, task, callback):
        super().__init__()

        self.task = task
        self.signals = WorkerSignals()
        self.signals.result.connect(callback)

    def run(self):
        print('Sending', self.task)
        self.signals.result.emit(self.task)


if __name__ == "__main__":

    import sys

    Path('../a/b').mkdir(parents=True, exist_ok=True)
    print(sys.path)

    # app = QApplication(sys.argv)
    # main = Tasks()
    # worker = Worker(1, main.process_result)
    # # worker.signals.result.connect(main.process_result)
    #
    # QThreadPool.globalInstance().start(worker)
    # QThreadPool.globalInstance().waitForDone()
    # sys.exit(app.exec_())
