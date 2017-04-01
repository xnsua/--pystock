import functools
import sys

from PyQt5.QtWidgets import QWidget, QPushButton, \
    QApplication, QHBoxLayout, \
    QLineEdit, QFormLayout


def generateFormLayout(layoutname, buyorsellstr):
    formlayout = QFormLayout()
    formlayout.setObjectName(layoutname)
    stockcodeedit = QLineEdit()
    stocknumedit = QLineEdit()
    stockpriceedit = QLineEdit()
    formlayout.addRow('StockCode: ', stockcodeedit)
    formlayout.addRow('StockPrice: ', stockpriceedit)
    formlayout.addRow('StockNum: ', stocknumedit)
    buybutton = QPushButton(buyorsellstr)
    formlayout.addWidget(buybutton)
    return formlayout


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.form_layouts = ['buy1', 'buy2', 'sell1', 'sell2']
        self.initUI()
        self.setAllButtonFunction()
        self.showMainWindow()

    def initUI(self):
        vlayout = QHBoxLayout(self)
        for v in self.form_layouts:
            vlayout.addLayout(generateFormLayout(v, v))

    def showMainWindow(self):
        self.setGeometry(800, 300, 250, 150)
        self.setWindowTitle('Test buy or sell stock')
        self.show()

    def setAllButtonFunction(self):
        layout = self.layout()  # type: QHBoxLayout
        for v in layout.findChildren(QFormLayout):
            layoutchilds = [v.itemAt(i).widget() for i in range(v.count())]

            def set_btn_function(lochild):
                code = lochild[1]  # type: QLineEdit
                price = lochild[3]
                num = lochild[5]
                codetxt = code.text()
                pricetxt = price.text()
                numtxt = num.text()
                print(code)
                print('hello')

            pushbutton = layoutchilds[6]  # type: QPushButton
            func = functools.partial(set_btn_function, layoutchilds)
            pushbutton.clicked.connect(func)


if __name__ == '__main__':
    import time

    time.sleep(1)
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
