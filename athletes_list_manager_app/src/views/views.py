from PySide6.QtWidgets import QDialog, QMainWindow, QDialogButtonBox, QHeaderView
from views.ui_add_window import Ui_AddDialog
from views.ui_main_window import Ui_MainWindow
from views.ui_search_window import Ui_SearchDialog
from views.ui_delete_window import Ui_DeleteDialog
from views.ui_settings_window import Ui_Settings
from core.settings import TABLE_HEADERS, RECORD_NUMS_PER_PAGE
from core.adapter import AthleteQtModel


class AddAthleteDialogView(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_AddDialog()
        self.ui.setupUi(self)
        apply_btn = self.ui.add_buttonBox.button(QDialogButtonBox.StandardButton.Apply)

        if apply_btn:
            apply_btn.clicked.connect(self.accept)
        self.ui.add_buttonBox.rejected.connect(self.reject)

    def setup_comboboxes(self, sports: list, ranks: list, teams: list, positions: list):
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
        apply_btn = self.ui.buttonBox.button(QDialogButtonBox.StandardButton.Apply)

        if apply_btn:
            apply_btn.clicked.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)

    def setup_comboboxes(self, sports: list, ranks: list):
        self.ui.sport_comboBox.clear()
        self.ui.sport_comboBox.addItem("Любой")
        self.ui.sport_comboBox.addItems(sports)

        self.ui.category_comboBox.clear()
        self.ui.category_comboBox.addItem("Любой")
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
        if sport != "Любой":
            criteria["sport"] = sport

        rank = self.ui.category_comboBox.currentText()
        if rank != "Любой":
            criteria["rank"] = rank

        min_titles = self.ui.min_spinBox.value()
        max_titles = self.ui.max_spinBox.value()

        if min_titles > 0 or max_titles > 0:
            criteria["min_titles"] = min_titles
            criteria["max_titles"] = max_titles

        return criteria


class SearchDialogView(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_SearchDialog()
        self.ui.setupUi(self)
        self.search_button = self.ui.buttonBox.button(
            QDialogButtonBox.StandardButton.Apply
        )
        self.ui.buttonBox.rejected.connect(self.reject)

    def setup_comboboxes(self, sports: list, ranks: list):
        self.ui.sport_comboBox.clear()
        self.ui.sport_comboBox.addItem("Любой")
        self.ui.sport_comboBox.addItems(sports)

        self.ui.category_comboBox.clear()
        self.ui.category_comboBox.addItem("Любой")
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
        if sport != "Любой":
            criteria["sport"] = sport

        rank = self.ui.category_comboBox.currentText()
        if rank != "Любой":
            criteria["rank"] = rank

        min_titles = self.ui.min_spinBox.value()
        max_titles = self.ui.max_spinBox.value()

        if min_titles > 0 or max_titles > 0:
            criteria["min_titles"] = min_titles
            criteria["max_titles"] = max_titles

        return criteria

    def render_results(self, athletes: list):

        qt_model = AthleteQtModel(athletes, TABLE_HEADERS)
        self.ui.tableView.setModel(qt_model)


class SettingsDialogView(QDialog):
    def __init__(self, current_theme: str):
        super().__init__()
        self.ui = Ui_Settings()
        self.ui.setupUi(self)
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


class MainView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.records_on_page_comboBox.addItems(
            str(num) for num in RECORD_NUMS_PER_PAGE
        )

        self.ui.tableView.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.ui.tableView.verticalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

    def render_table(self, athletes_page: list):
        qt_model = AthleteQtModel(athletes_page, TABLE_HEADERS)

        self.ui.tableView.setModel(qt_model)

    def update_pagination_labels(
        self, current_page: int, total_pages: int, total_items: int
    ):
        self.ui.current_page_label.setText(
            f"Страница {current_page + 1} из {total_pages}"
        )
        self.ui.table_name_label.setText(f"Всего записей: {total_items}")
