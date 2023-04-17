from PyQt5.QtWidgets import QApplication
import sys
import MainWindow as mw

if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = mw.MainWindow()
    sys.exit(App.exec_())
