from PySide6.QtWidgets import (
    QDialog,
    QMainWindow,
    QDialogButtonBox,
    QHeaderView,
    QWidget,
    QMessageBox,
)
from PySide6.QtCore import Signal
from views.ui_add_window import Ui_AddDialog
from views.ui_main_window import Ui_MainWindow
from views.ui_search_window import Ui_SearchDialog
from views.ui_delete_window import Ui_DeleteDialog
from views.ui_settings_window import Ui_Settings
from core.settings import TABLE_HEADERS, RECORD_NUMS_PER_PAGE, DEFAULT_COMBO_ITEM
from core.adapter import AthleteQtModel


class AddAthleteDialogView(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_AddDialog()
        self.ui.setupUi(self)
        self.setWindowTitle("SportMAN – Добавление записи о спортсменах")
        apply_btn = self.ui.add_buttonBox.button(QDialogButtonBox.StandardButton.Apply)
        self.ui.add_buttonBox.button(QDialogButtonBox.StandardButton.Apply).setText(
            "Добавить"
        )
        self.ui.add_buttonBox.rejected.connect(self.reject)
        self.ui.add_buttonBox.button(QDialogButtonBox.StandardButton.Cancel).setText(
            "Отмена"
        )
        if apply_btn:
            apply_btn.clicked.connect(self._on_apply_clicked)
        self.ui.add_buttonBox.rejected.connect(self.reject)

        self.ui.last_name_lineEdit.textChanged.connect(
            lambda: self._clear_error(self.ui.last_name_lineEdit)
        )
        self.ui.first_name_lineEdit.textChanged.connect(
            lambda: self._clear_error(self.ui.first_name_lineEdit)
        )
        self.ui.sport_comboBox.currentTextChanged.connect(
            lambda: self._clear_error(self.ui.sport_comboBox)
        )

    def _on_apply_clicked(self, checked: bool = False) -> None:
        last_name = self.ui.last_name_lineEdit.text().strip()
        first_name = self.ui.first_name_lineEdit.text().strip()
        sport = self.ui.sport_comboBox.currentText().strip()
        valid = True
        if not last_name:
            self._set_error(self.ui.last_name_lineEdit)
            valid = False
        if not first_name:
            self._set_error(self.ui.first_name_lineEdit)
            valid = False

        if not sport:
            self._set_error(self.ui.sport_comboBox)
            valid = False
        if not valid:
            return

        self.accept()

    @staticmethod
    def _set_error(widget: QWidget) -> None:
        widget.setStyleSheet("border: 1px solid red;")
        widget.setFocus()

    @staticmethod
    def _clear_error(widget: QWidget) -> None:
        widget.setStyleSheet("")

    def setup_comboboxes(
        self, sports: list, ranks: list, teams: list, positions: list
    ) -> None:
        self.ui.sport_comboBox.clear()
        self.ui.sport_comboBox.addItems(sports)

        self.ui.category_comboBox.clear()
        self.ui.category_comboBox.addItems(ranks)

        self.ui.team_comboBox.clear()
        self.ui.team_comboBox.addItems(teams)

        self.ui.position_comboBox.clear()
        self.ui.position_comboBox.addItems(positions)

    def get_athlete_data(self) -> dict:
        name_parts = [
            self.ui.last_name_lineEdit.text().strip(),
            self.ui.first_name_lineEdit.text().strip(),
            self.ui.patronymic_lineEdit.text().strip(),
        ]
        full_name = " ".join([p for p in name_parts if p])

        return {
            "fio": full_name,
            "sport": self.ui.sport_comboBox.currentText(),
            "rank": self.ui.category_comboBox.currentText(),
            "titles": self.ui.title_spinBox.value(),
            "team": self.ui.team_comboBox.currentText(),
            "position": self.ui.position_comboBox.currentText().strip(),
        }


class DeleteDialogView(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_DeleteDialog()
        self.ui.setupUi(self)
        self.setWindowTitle("SportMAN – Удаление записей о спортсменах")
        apply_btn = self.ui.buttonBox.button(QDialogButtonBox.StandardButton.Apply)

        if apply_btn:
            apply_btn.clicked.connect(self._on_apply_clicked)
        self.ui.buttonBox.rejected.connect(self.reject)
        self.ui.buttonBox.button(QDialogButtonBox.StandardButton.Apply).setText(
            "Удалить"
        )
        self.ui.buttonBox.rejected.connect(self.reject)
        self.ui.buttonBox.button(QDialogButtonBox.StandardButton.Cancel).setText(
            "Отмена"
        )

        self.ui.min_spinBox.valueChanged.connect(
            lambda: self._clear_error(self.ui.min_spinBox)
        )
        self.ui.max_spinBox.valueChanged.connect(
            lambda: self._clear_error(self.ui.max_spinBox)
        )

    def setup_comboboxes(self, sports: list, ranks: list):
        self.ui.sport_comboBox.clear()
        self.ui.sport_comboBox.addItem(DEFAULT_COMBO_ITEM)
        self.ui.sport_comboBox.addItems(sports)

        self.ui.category_comboBox.clear()
        self.ui.category_comboBox.addItem(DEFAULT_COMBO_ITEM)
        self.ui.category_comboBox.addItems(ranks)

    def get_search_criteria(self) -> dict:
        criteria = {}

        name_parts = [
            self.ui.last_name_lineEdit.text().strip(),
            self.ui.first_name_lineEdit.text().strip(),
            self.ui.patronymic_lineEdit.text().strip(),
        ]
        full_name = " ".join([p for p in name_parts if p])
        if full_name:
            criteria["fio"] = full_name

        sport = self.ui.sport_comboBox.currentText()
        if sport != DEFAULT_COMBO_ITEM:
            criteria["sport"] = sport

        rank = self.ui.category_comboBox.currentText()
        if rank != DEFAULT_COMBO_ITEM:
            criteria["rank"] = rank

        min_titles = self.ui.min_spinBox.value()
        max_titles = self.ui.max_spinBox.value()

        if min_titles > 0 or max_titles > 0:
            criteria["min_titles"] = min_titles
            criteria["max_titles"] = max_titles

        return criteria

    @staticmethod
    def _set_error(widget: QWidget) -> None:
        widget.setStyleSheet("border: 1px solid red;")
        widget.setFocus()

    @staticmethod
    def _clear_error(widget: QWidget) -> None:
        widget.setStyleSheet("")

    def _on_apply_clicked(self, checked: bool = False) -> None:
        min_title = int(self.ui.min_spinBox.value())
        max_title = int(self.ui.max_spinBox.value())
        valid = True
        if min_title > max_title:
            self._set_error(self.ui.min_spinBox)
            self._set_error(self.ui.max_spinBox)
            valid = False

        if not valid:
            return

        self.accept()


class PaginatableView:
    def render_table(self, data):
        raise NotImplementedError

    def update_pagination_labels(self, cur, total, count):
        raise NotImplementedError

    def update_pagination_buttons(self, cur, total):
        raise NotImplementedError


class SearchDialogView(QDialog, PaginatableView):
    def __init__(self):
        super().__init__()
        self.ui = Ui_SearchDialog()
        self.ui.setupUi(self)
        self.setWindowTitle("SportMAN – Поиск спортсменов")
        self.search_button = self.ui.buttonBox.button(
            QDialogButtonBox.StandardButton.Apply
        )

        if self.search_button:
            self.search_button.clicked.connect(self._on_apply_clicked)
        self.ui.records_on_page_comboBox.addItems(
            str(num) for num in RECORD_NUMS_PER_PAGE
        )

        self.ui.tableView.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.ui.tableView.verticalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.ui.buttonBox.button(QDialogButtonBox.StandardButton.Apply).setText("Поиск")
        self.ui.buttonBox.rejected.connect(self.reject)
        self.ui.buttonBox.button(QDialogButtonBox.StandardButton.Cancel).setText(
            "Отмена"
        )
        self.ui.min_spinBox.valueChanged.connect(
            lambda: self._clear_error(self.ui.min_spinBox)
        )
        self.ui.max_spinBox.valueChanged.connect(
            lambda: self._clear_error(self.ui.max_spinBox)
        )

    def setup_comboboxes(self, sports: list, ranks: list):
        self.ui.sport_comboBox.clear()
        self.ui.sport_comboBox.addItem(DEFAULT_COMBO_ITEM)
        self.ui.sport_comboBox.addItems(sports)

        self.ui.category_comboBox.clear()
        self.ui.category_comboBox.addItem(DEFAULT_COMBO_ITEM)
        self.ui.category_comboBox.addItems(ranks)

    def get_search_criteria(self) -> dict:
        criteria = {}

        name_parts = [
            self.ui.last_name_lineEdit.text().strip(),
            self.ui.first_name_lineEdit.text().strip(),
            self.ui.patronymic_lineEdit.text().strip(),
        ]
        full_name = " ".join([p for p in name_parts if p])
        if full_name:
            criteria["fio"] = full_name

        sport = self.ui.sport_comboBox.currentText()
        if sport != DEFAULT_COMBO_ITEM:
            criteria["sport"] = sport

        rank = self.ui.category_comboBox.currentText()
        if rank != DEFAULT_COMBO_ITEM:
            criteria["rank"] = rank

        min_titles = self.ui.min_spinBox.value()
        max_titles = self.ui.max_spinBox.value()

        if min_titles > 0 or max_titles > 0:
            criteria["min_titles"] = min_titles
            criteria["max_titles"] = max_titles

        return criteria

    def render_table(self, athletes_page: list):
        qt_model = AthleteQtModel(athletes_page, TABLE_HEADERS)
        self.ui.tableView.setModel(qt_model)

    def update_pagination_labels(
        self, current_page: int, total_pages: int, total_items: int
    ) -> None:
        self.ui.current_page_label.setText(
            f"Страница {current_page + 1} из {total_pages}"
        )
        self.ui.table_name_label.setText(f"Всего записей: {total_items}")

    def update_pagination_buttons(self, current_page: int, total_pages: int) -> None:
        """Обновляет состояние кнопок навигации по страницам."""
        is_not_first = current_page > 0
        is_not_last = current_page < (total_pages - 1)
        self.ui.current_page_button.setText(str(current_page + 1))
        self.ui.first_page_button.setEnabled(is_not_first)
        self.ui.prev_pagination_button.setEnabled(is_not_first)
        self.ui.last_page_button.setEnabled(is_not_last)
        self.ui.next_pagination_button.setEnabled(is_not_last)

    @staticmethod
    def _set_error(widget: QWidget) -> None:
        widget.setStyleSheet("border: 1px solid red;")
        widget.setFocus()

    @staticmethod
    def _clear_error(widget: QWidget) -> None:
        widget.setStyleSheet("")

    def _on_apply_clicked(self, checked: bool = False) -> None:
        min_title = int(self.ui.min_spinBox.value())
        max_title = int(self.ui.max_spinBox.value())
        valid = True
        if min_title > max_title:
            self._set_error(self.ui.min_spinBox)
            self._set_error(self.ui.max_spinBox)
            valid = False

        if not valid:
            return


class SettingsDialogView(QDialog):
    def __init__(self, current_theme: str):
        super().__init__()
        self.ui = Ui_Settings()
        self.ui.setupUi(self)
        self.setWindowTitle("SportMAN – Настройки")
        apply_btn = self.ui.buttonBox.button(QDialogButtonBox.StandardButton.Apply)

        if apply_btn:
            apply_btn.clicked.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)
        if current_theme == "light":
            self.ui.light_theme_radioButton.setChecked(True)
        elif current_theme == "dark":
            self.ui.dark_theme_radioButton.setChecked(True)
        else:
            self.ui.system_theme_radioButton.setChecked(True)

    def get_selected_theme(self) -> str:
        if self.ui.light_theme_radioButton.isChecked():
            return "light"
        elif self.ui.dark_theme_radioButton.isChecked():
            return "dark"
        return "auto"


class MainView(QMainWindow, PaginatableView):
    exit_requested = Signal(object)

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("SportMAN – Приложение списка спортсменов")
        self.ui.records_on_page_comboBox.addItems(
            str(num) for num in RECORD_NUMS_PER_PAGE
        )
        self.close_requested = Signal(object)
        self.ui.tableView.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.ui.tableView.verticalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

    def closeEvent(self, event):
        self.exit_requested.emit(event)

    def render_table(self, athletes_page: list):
        qt_model = AthleteQtModel(athletes_page, TABLE_HEADERS)
        self.ui.tableView.setModel(qt_model)

    def update_pagination_labels(
        self, current_page: int, total_pages: int, total_items: int
    ) -> None:
        self.ui.current_page_label.setText(
            f"Страница {current_page + 1} из {total_pages}"
        )
        self.ui.table_name_label.setText(f"Всего записей: {total_items}")

    def update_pagination_buttons(self, current_page: int, total_pages: int) -> None:
        """Обновляет состояние кнопок навигации по страницам."""
        is_not_first = current_page > 0
        is_not_last = current_page < (total_pages - 1)
        self.ui.current_page_button.setText(str(current_page + 1))
        self.ui.first_page_button.setEnabled(is_not_first)
        self.ui.prev_pagination_button.setEnabled(is_not_first)
        self.ui.last_page_button.setEnabled(is_not_last)
        self.ui.next_pagination_button.setEnabled(is_not_last)
