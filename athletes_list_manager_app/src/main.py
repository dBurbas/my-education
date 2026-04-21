# main.py
import sys

from PySide6.QtWidgets import QApplication

from core.model import AthleteManagerModel
from views.views import MainView
from controllers import MainController


def main():

    app = QApplication(sys.argv)

    model = AthleteManagerModel()

    view = MainView()

    controller = MainController(model, view)

    view.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
