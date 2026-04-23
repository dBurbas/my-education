# main.py
import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QSettings

from core.loader import SAXLoader
from core.saver import DOMSaver
from core.model import AthleteManagerModel
from views.views import MainView
from views.dialog_factory import DefaultDialogFactory

from controllers import (
    MainController,
    ThemeController,
    PaginationController,
    SearchController,
)


def main() -> None:
    app = QApplication(sys.argv)

    model = AthleteManagerModel(saver=DOMSaver(), loader=SAXLoader())

    view = MainView()

    settings = QSettings("BSUIR", "SportMan")
    theme_service = ThemeController(settings)
    pagination = PaginationController(model, view)

    dialog_factory = DefaultDialogFactory()
    search = SearchController(model, dialog_factory)
    controller = MainController(
        model=model,
        view=view,
        pagination=pagination,
        theme_service=theme_service,
        search_controller=search,
        dialog_factory=dialog_factory,
    )

    view.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
