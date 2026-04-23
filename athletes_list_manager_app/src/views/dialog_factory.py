from abc import ABC, abstractmethod
from views.views import (
    AddAthleteDialogView,
    SearchDialogView,
    DeleteDialogView,
    SettingsDialogView,
)


class IDialogFactory(ABC):
    @abstractmethod
    def create_add_dialog(self) -> AddAthleteDialogView:
        pass

    @abstractmethod
    def create_search_dialog(self) -> SearchDialogView:
        pass

    @abstractmethod
    def create_delete_dialog(self) -> DeleteDialogView:
        pass

    @abstractmethod
    def create_settings_dialog(self, current_theme: str) -> SettingsDialogView:
        pass


class DefaultDialogFactory(IDialogFactory):
    def create_add_dialog(self) -> AddAthleteDialogView:
        return AddAthleteDialogView()

    def create_search_dialog(self) -> SearchDialogView:
        return SearchDialogView()

    def create_delete_dialog(self) -> DeleteDialogView:
        return DeleteDialogView()

    def create_settings_dialog(self, current_theme: str) -> SettingsDialogView:
        return SettingsDialogView(current_theme)
