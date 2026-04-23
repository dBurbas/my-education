from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex
from typing import TYPE_CHECKING
from dataclasses import fields
from core.athlete import Athlete

if TYPE_CHECKING:
    from core.athlete import Athlete

FIELD_NAMES = [f.name for f in fields(Athlete)]


class AthleteQtModel(QAbstractTableModel):
    def __init__(self, athletes_list: list["Athlete"], headers: list):
        super().__init__()
        self._data = athletes_list
        self._headers = headers

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._headers)

    def data(self, index: QModelIndex, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or role != Qt.ItemDataRole.DisplayRole:
            return None

        athlete = self._data[index.row()]
        attr = FIELD_NAMES[index.column()]
        return str(getattr(athlete, attr))

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if (
            role == Qt.ItemDataRole.DisplayRole
            and orientation == Qt.Orientation.Horizontal
        ):
            return self._headers[section]
        return None
