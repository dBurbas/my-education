# controllers.py
import os
from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import Qt, QSettings
from PySide6.QtWidgets import QMessageBox, QFileDialog
from core.settings import TEAM_TYPES, POSITIONS, SPORT_RANKS
from core.model import AthleteManagerModel
from core.athlete import Athlete
from views.dialog_factory import IDialogFactory
from exceptions.athlete_manager_exceptions import AthleteManagerError
from views.views import (
    MainView,
    SearchDialogView,
)


class PaginationController:
    def __init__(self, model: AthleteManagerModel, view: MainView) -> None:
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


class MainController:
    def __init__(
        self,
        model: AthleteManagerModel,
        view: MainView,
        pagination: PaginationController,
        theme_service: ThemeController,
        dialog_factory: IDialogFactory,
    ) -> None:
        self._model = model
        self._view = view
        self._pagination = pagination
        self._theme = theme_service
        self._dialogs = dialog_factory

        self._search_dialog: SearchDialogView | None = None

        self._connect_signals()
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
        except AthleteManagerError as e:
            QMessageBox.warning(self._view, "Ошибка", str(e))
            return
        self._pagination.go_to_last_page()

    def open_search_dialog(self) -> None:
        if self._search_dialog is None:
            self._search_dialog = self._dialogs.create_search_dialog()
            if self._search_dialog.search_button:
                self._search_dialog.search_button.clicked.connect(self._perform_search)

        self._search_dialog.setup_comboboxes(
            self._model.get_existing_sports(), self._model.get_existing_ranks()
        )
        self._search_dialog.show()
        self._search_dialog.raise_()

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

    def _perform_search(self, checked: bool = False) -> None:
        criteria = self._search_dialog.get_search_criteria()
        try:
            found = self._model.find_athletes(criteria)
            self._search_dialog.render_results(found)
            if not found:
                QMessageBox.information(
                    self._search_dialog, "Результат", "Ничего не найдено."
                )
        except AthleteManagerError as e:
            QMessageBox.warning(self._search_dialog, "Ошибка поиска", str(e))

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
