# controller.py
from PySide6.QtGui import QGuiApplication, QPalette
from PySide6.QtCore import Qt, QSettings
from PySide6.QtWidgets import QMessageBox
from core.settings import TEAM_TYPES, POSITIONS, SPORT_RANKS
from core.model import AthleteManagerModel, Athlete
from exceptions.athlete_manager_exceptions import AthleteManagerError
from views.views import (
    MainView,
    AddAthleteDialogView,
    SearchDialogView,
    DeleteDialogView,
    SettingsDialogView,
)


class MainController:
    def __init__(self, model: AthleteManagerModel, view: MainView):
        self.model = model
        self.main_view = view
        self.current_theme = "System"
        self.settings = QSettings("BSUIR", "SportMan")
        self.search_dialog = None
        self.search_current_page = 0
        self.search_results = []
        self.current_theme = self.settings.value("appearance/theme", "System")
        self.apply_theme(self.current_theme)

        self.current_page = 0
        self.items_per_page = 10

        self.main_view.ui.records_on_page_comboBox.currentTextChanged.connect(
            self.on_per_page_changed
        )
        self.main_view.ui.action_add.triggered.connect(self.open_add_dialog)
        self.main_view.ui.action_search.triggered.connect(self.open_search_dialog)
        self.main_view.ui.action_delete.triggered.connect(self.open_delete_dialog)
        self.main_view.ui.action_settings.triggered.connect(self.open_settings_dialog)
        self.main_view.ui.add_button.clicked.connect(self.open_add_dialog)
        self.main_view.ui.search_button.clicked.connect(self.open_search_dialog)
        self.main_view.ui.delete_button.clicked.connect(self.open_delete_dialog)
        self.main_view.ui.settings_button.clicked.connect(self.open_settings_dialog)
        # Кнопки пагинации
        self.main_view.ui.next_pagination_button.clicked.connect(self.turn_page_forward)
        self.main_view.ui.prev_pagination_button.clicked.connect(self.turn_page_back)
        self.main_view.ui.last_page_button.clicked.connect(self.turn_to_end_page)
        self.main_view.ui.first_page_button.clicked.connect(self.turn_to_first_page)

        self.refresh_main_table()

    def on_per_page_changed(self, value: str):

        self.items_per_page = int(value)

        self.current_page = 0

        self.refresh_main_table()

    def refresh_main_table(self):
        """Обновляет данные в таблице и состояние кнопок пагинации"""
        total_pages = self.model.get_total_pages_num(self.items_per_page)

        if self.current_page >= total_pages:
            self.current_page = max(0, total_pages - 1)

        page_data = self.model.get_page(self.current_page, self.items_per_page)

        self.main_view.render_table(page_data)

        total_pages = self.model.get_total_pages_num(self.items_per_page)
        total_items = self.model.get_total_athletes_count()
        self.main_view.update_pagination_labels(
            self.current_page, total_pages, total_items
        )

        self.main_view.ui.second_page_button.setEnabled(total_pages > 1)
        self.main_view.ui.last_page_button.setEnabled(total_pages > 1)
        self.main_view.ui.prev_pagination_button.setEnabled(self.current_page > 0)
        self.main_view.ui.next_pagination_button.setEnabled(
            self.current_page < total_pages - 1
        )

    def turn_page_forward(self):
        total_pages = self.model.get_total_pages_num(self.items_per_page)
        if self.current_page < total_pages - 1:
            self.current_page += 1
            self.refresh_main_table()

    def turn_page_back(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.refresh_main_table()

    def turn_to_first_page(self):
        if self.current_page != 0:
            self.current_page = 0
            self.refresh_main_table()

    def turn_to_end_page(self):
        total_pages = self.model.get_total_pages_num(self.items_per_page)
        if self.current_page < total_pages - 1:
            self.current_page = total_pages - 1
            self.refresh_main_table()

    def open_add_dialog(self):
        dialog = AddAthleteDialogView()

        dialog.setup_comboboxes(
            sports=self.model.get_existing_sports(),
            ranks=SPORT_RANKS,
            teams=TEAM_TYPES,
            positions=POSITIONS,
        )

        if dialog.exec():
            raw_data = dialog.get_athlete_data()
            new_athlete = Athlete(**raw_data)
            self.model.add_athlete(new_athlete)

            self.current_page = self.model.get_total_pages_num(self.items_per_page) - 1
            self.refresh_main_table()

    def open_search_dialog(self):
        if self.search_dialog is None:
            self.search_dialog = SearchDialogView()

            if self.search_dialog.search_button:
                self.search_dialog.search_button.clicked.connect(self.perform_search)

        self.search_dialog.setup_comboboxes(
            self.model.get_existing_sports(), SPORT_RANKS
        )

        self.search_dialog.show()
        self.search_dialog.raise_()  # Выводит окно поверх остальных

    def perform_search(self, dialog: SearchDialogView):
        criteria = self.search_dialog.get_search_criteria()

        try:
            found_athletes = self.model.find_athletes(criteria)

            self.search_dialog.render_results(found_athletes)

            if not found_athletes:
                from PySide6.QtWidgets import QMessageBox

                QMessageBox.information(
                    self.search_dialog, "Результат", "Ничего не найдено."
                )

        except Exception as e:
            print(f"Ошибка поиска: {e}")

    def open_delete_dialog(self):
        delete_dialog = DeleteDialogView()
        delete_dialog.setup_comboboxes(self.model.get_existing_sports(), SPORT_RANKS)

        if delete_dialog.exec():
            criteria = delete_dialog.get_search_criteria()
            try:
                self.perform_deletion(criteria)

            except AthleteManagerError as e:
                QMessageBox.warning(self.main_view, "Ошибка", f"Ошибка удаления: {e}")

    def perform_deletion(self, criteria: dict):
        athletes_to_delete = self.model.find_athletes(criteria)
        delete_count = len(athletes_to_delete)
        total_count = self.model.get_total_athletes_count()

        if delete_count == 0:
            QMessageBox.information(
                self.main_view,
                "Результат",
                "По вашим критериям не найдено ни одного спортсмена.",
            )
            return

        if delete_count == total_count:
            reply = QMessageBox.warning(
                self.main_view,
                "Критическое действие!",
                "Вы собираетесь удалить ВСЕХ спортсменов из базы!\nЭто действие нельзя отменить. Вы абсолютно уверены?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )

            if reply == QMessageBox.StandardButton.No:
                return

        elif delete_count > 0:
            reply = QMessageBox.question(
                self.main_view,
                "Подтверждение",
                f"Будет удалено записей: {delete_count}. Продолжить?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )
            if reply == QMessageBox.StandardButton.No:
                return

        self.model.remove_athletes(criteria)

        self.refresh_main_table()
        QMessageBox.information(
            self.main_view, "Успех", f"Успешно удалено записей: {delete_count}"
        )

    def open_settings_dialog(self):
        settings_dialog = SettingsDialogView(self.current_theme)
        if settings_dialog.exec():
            selected_theme = settings_dialog.get_selected_theme()
            if selected_theme != self.current_theme:
                self.current_theme = selected_theme
                self.apply_theme(self.current_theme)
                self.settings.setValue("appearance/theme", self.current_theme)

    def apply_theme(self, theme_name: str):
        if theme_name == "dark":
            QGuiApplication.styleHints().setColorScheme(Qt.ColorScheme.Dark)
        elif theme_name == "light":
            QGuiApplication.styleHints().setColorScheme(Qt.ColorScheme.Light)
        elif theme_name == "auto":
            QGuiApplication.styleHints().setColorScheme(Qt.ColorScheme.Unknown)
