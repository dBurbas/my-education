# controllers.py
import os
from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import Qt, QSettings
from PySide6.QtWidgets import QMessageBox, QFileDialog, QWidget
from core.settings import TEAM_TYPES, POSITIONS, SPORT_RANKS
from core.model import AthleteManagerModel
from core.athlete import Athlete
from views.dialog_factory import IDialogFactory
from exceptions.athlete_manager_exceptions import AthleteManagerError
from math import ceil
from views.views import MainView, SearchDialogView, PaginatableView


class PaginationController:
    def __init__(self, model, view: PaginatableView) -> None:
        self._model = model
        self._view = view
        self.current_page: int = 0
        self.items_per_page: int = 10
        self._connect_signals()

    def _connect_signals(self) -> None:
        ui = self._view.ui
        ui.next_pagination_button.clicked.connect(self.turn_forward)
        ui.prev_pagination_button.clicked.connect(self.turn_back)
        ui.last_page_button.clicked.connect(self.turn_to_last)
        ui.first_page_button.clicked.connect(self.turn_to_first)
        ui.records_on_page_comboBox.currentTextChanged.connect(self.on_per_page_changed)
        ui.current_page_button.setDisabled(True)
        ui.records_on_page_comboBox.setCurrentText(str(self.items_per_page))

    def refresh(self) -> None:
        total_pages = self._model.get_total_pages_num(self.items_per_page)

        if self.current_page >= total_pages:
            self.current_page = max(0, total_pages - 1)

        page_data = self._model.get_page(self.current_page, self.items_per_page)
        self._view.render_table(page_data)

        total_items = self._model.get_total_athletes_count()
        self._view.update_pagination_labels(self.current_page, total_pages, total_items)
        self._view.update_pagination_buttons(self.current_page, total_pages)

    def go_to_last_page(self) -> None:
        """Перейти на последнюю страницу — используется после добавления записи."""
        self.current_page = max(
            0, self._model.get_total_pages_num(self.items_per_page) - 1
        )
        self.refresh()

    def on_per_page_changed(self, value: str) -> None:
        self.items_per_page = int(value)
        self.current_page = 0
        self.refresh()

    def turn_forward(self):
        total_pages = self._model.get_total_pages_num(self.items_per_page)
        if self.current_page < total_pages - 1:
            self.current_page += 1
            self.refresh()

    def turn_back(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.refresh()

    def turn_to_first(self):
        if self.current_page != 0:
            self.current_page = 0
            self.refresh()

    def turn_to_last(self):
        total_pages = self._model.get_total_pages_num(self.items_per_page)
        if self.current_page < total_pages - 1:
            self.current_page = total_pages - 1
            self.refresh()


class ThemeController:
    _THEME_KEY = "appearance/theme"
    _DEFAULT = "auto"

    _SCHEME_MAP = {
        "dark": Qt.ColorScheme.Dark,
        "light": Qt.ColorScheme.Light,
    }

    def __init__(self, settings: QSettings) -> None:
        self._settings = settings

    def apply(self, theme_name: str) -> None:
        scheme = self._SCHEME_MAP.get(theme_name, Qt.ColorScheme.Unknown)
        QGuiApplication.styleHints().setColorScheme(scheme)

    def load_saved(self) -> str:
        return self._settings.value(self._THEME_KEY, self._DEFAULT)

    def save(self, theme_name: str) -> None:
        self._settings.setValue(self._THEME_KEY, theme_name)


class StaticPagedData:
    """Обёртка над статическим списком для пагинации результатов поиска."""

    def __init__(self) -> None:
        self._athletes: list[Athlete] = []

    def update(self, athletes: list[Athlete]) -> None:
        self._athletes = athletes

    def get_page(self, page_num: int, items_per_page: int) -> list[Athlete]:
        start = page_num * items_per_page
        return self._athletes[start : start + items_per_page]

    def get_total_pages_num(self, items_per_page: int) -> int:
        return max(1, ceil(len(self._athletes) / items_per_page))

    def get_total_athletes_count(self) -> int:
        return len(self._athletes)


class SearchController:
    def __init__(
        self, model: AthleteManagerModel, dialog_factory: IDialogFactory
    ) -> None:
        self._model = model
        self._dialogs = dialog_factory
        self._search_dialog: SearchDialogView | None = None
        self._search_data_source = StaticPagedData()
        self._search_pagination: PaginationController | None = None

    def open(self) -> None:
        if self._search_dialog is None:
            self._search_dialog = self._dialogs.create_search_dialog()
            self._search_pagination = PaginationController(
                model=self._search_data_source,
                view=self._search_dialog,
            )
            if self._search_dialog.search_button:
                self._search_dialog.search_button.clicked.connect(self._perform_search)

        self._search_dialog.setup_comboboxes(
            self._model.get_existing_sports(), self._model.get_existing_ranks()
        )
        self._search_pagination.refresh()
        self._search_dialog.show()
        self._search_dialog.raise_()

    def _perform_search(self, checked: bool = False) -> None:
        criteria = self._search_dialog.get_search_criteria()
        try:
            found = self._model.find_athletes(criteria)
            self._search_data_source.update(found)
            self._search_pagination.refresh()
            if not found:
                QMessageBox.information(
                    self._search_dialog, "Результат", "Ничего не найдено."
                )
        except AthleteManagerError as e:
            QMessageBox.warning(self._search_dialog, "Ошибка поиска", str(e))


class MainController:
    def __init__(
        self,
        model: AthleteManagerModel,
        view: MainView,
        pagination: PaginationController,
        theme_service: ThemeController,
        search_controller: SearchController,
        dialog_factory: IDialogFactory,
    ) -> None:
        self._model = model
        self._view = view
        self._pagination = pagination
        self._theme = theme_service
        self._search = search_controller
        self._dialogs = dialog_factory
        self._connect_signals()
        self.is_modified = False
        self._theme.apply(self._theme.load_saved())
        self._pagination.refresh()

    def _connect_signals(self) -> None:
        ui = self._view.ui
        ui.action_save.triggered.connect(self.save)
        ui.save_button.clicked.connect(self.save)
        ui.action_load.triggered.connect(self.load)
        ui.load_button.clicked.connect(self.load)
        ui.action_add.triggered.connect(self.open_add_dialog)
        ui.action_search.triggered.connect(self.open_search_dialog)
        ui.action_delete.triggered.connect(self.open_delete_dialog)
        ui.action_settings.triggered.connect(self.open_settings_dialog)
        ui.add_button.clicked.connect(self.open_add_dialog)
        ui.search_button.clicked.connect(self.open_search_dialog)
        ui.delete_button.clicked.connect(self.open_delete_dialog)
        ui.settings_button.clicked.connect(self.open_settings_dialog)
        self._view.exit_requested.connect(self._handle_close)

    def _handle_close(self, event):
        if self.is_modified:
            msg = QMessageBox(self._view)
            msg.setIcon(QMessageBox.Icon.Question)
            msg.setWindowTitle("Сохранить изменения?")
            msg.setText("Документ был изменён. Сохранить перед закрытием?")
            msg.setStandardButtons(
                QMessageBox.StandardButton.Save
                | QMessageBox.StandardButton.Discard
                | QMessageBox.StandardButton.Cancel
            )
            msg.setDefaultButton(QMessageBox.StandardButton.Save)

            msg.button(QMessageBox.StandardButton.Save).setText("Сохранить")
            msg.button(QMessageBox.StandardButton.Discard).setText("Не сохранять")
            msg.button(QMessageBox.StandardButton.Cancel).setText("Отмена")
            reply = msg.exec()

            if reply == QMessageBox.StandardButton.Save:
                self.save()
                event.accept()
            elif reply == QMessageBox.StandardButton.Discard:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

    def save(self):
        filepath, _ = QFileDialog.getSaveFileName(
            self._view, "Сохранить файл", "data/save_files/", "XML Files (*.xml)"
        )
        if not filepath:
            return
        try:
            self._model.save_to_file(filepath)
            filename = os.path.basename(filepath) if filepath else ""
            self._view.ui.file_name_label.setText(f"Файл: {filename}")
            self.is_modified = False
        except AthleteManagerError as e:
            QMessageBox.critical(self._view, "Ошибка сохранения", str(e))
            return

    def load(self):
        filepath, _ = QFileDialog.getOpenFileName(
            self._view, "Открыть файл", "data/save_files/", "XML Files (*.xml)"
        )
        if not filepath:
            return
        try:
            self._model.load_from_file(filepath)
            filename = os.path.basename(filepath) if filepath else ""
            self._view.ui.file_name_label.setText(f"Файл: {filename}")
            self.is_modified = False
        except AthleteManagerError as e:
            QMessageBox.critical(self._view, "Ошибка загрузки", str(e))
            return
        self._pagination.refresh()

    def open_add_dialog(self) -> None:
        dialog = self._dialogs.create_add_dialog()
        dialog.setup_comboboxes(
            sports=self._model.get_existing_sports(),
            ranks=SPORT_RANKS,
            teams=TEAM_TYPES,
            positions=POSITIONS,
        )
        if not dialog.exec():
            return
        raw_data = dialog.get_athlete_data()
        try:
            self._model.add_athlete(Athlete(**raw_data))
            self.is_modified = True
        except AthleteManagerError as e:
            QMessageBox.warning(self._view, "Ошибка", str(e))
            return
        self._pagination.go_to_last_page()

    def open_search_dialog(self) -> None:
        self._search.open()

    def open_delete_dialog(self) -> None:
        dialog = self._dialogs.create_delete_dialog()
        dialog.setup_comboboxes(
            self._model.get_existing_sports(), self._model.get_existing_ranks()
        )
        if not dialog.exec():
            return
        criteria = dialog.get_search_criteria()
        try:
            self._perform_deletion(criteria)
            self.is_modified = True
        except AthleteManagerError as e:
            QMessageBox.warning(self._view, "Ошибка удаления", str(e))

    def open_settings_dialog(self) -> None:
        current_theme = self._theme.load_saved()
        dialog = self._dialogs.create_settings_dialog(current_theme)
        if not dialog.exec():
            return
        selected_theme = dialog.get_selected_theme()
        if selected_theme != current_theme:
            self._theme.apply(selected_theme)
            self._theme.save(selected_theme)
            for child in self._view.findChildren(QWidget):
                child.style().unpolish(child)
                child.style().polish(child)
                child.update()

    def _perform_deletion(self, criteria: dict) -> None:
        athletes_to_delete = self._model.find_athletes(criteria)
        delete_count = len(athletes_to_delete)
        total_count = self._model.get_total_athletes_count()

        if delete_count == 0:
            QMessageBox.information(
                self._view,
                "Результат",
                "По вашим критериям не найдено ни одного спортсмена.",
            )
            return

        if delete_count == total_count:
            reply = QMessageBox.warning(
                self._view,
                "Критическое действие!",
                "Вы собираетесь удалить ВСЕХ спортсменов из базы!\n"
                "Это действие нельзя отменить. Вы абсолютно уверены?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )
        else:
            reply = QMessageBox.question(
                self._view,
                "Подтверждение",
                f"Будет удалено записей: {delete_count}. Продолжить?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )

        if reply == QMessageBox.StandardButton.No:
            return

        self._model.remove_athletes(criteria)
        self._pagination.refresh()
        QMessageBox.information(
            self._view, "Успех", f"Успешно удалено записей: {delete_count}"
        )
