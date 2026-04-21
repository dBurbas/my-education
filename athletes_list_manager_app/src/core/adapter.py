from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex


class AthleteQtModel(QAbstractTableModel):
    def __init__(self, athletes_list: list, headers: list):
        super().__init__()
        self._data = athletes_list
        self._headers = headers

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._headers)

    def data(self, index: QModelIndex, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None

        if role == Qt.ItemDataRole.DisplayRole:
            athlete = self._data[index.row()]
            col = index.column()

            if col == 0:
                return athlete.fio
            elif col == 1:
                return athlete.team
            elif col == 2:
                return athlete.position
            elif col == 3:
                return str(athlete.titles)
            elif col == 4:
                return athlete.sport
            elif col == 5:
                return athlete.rank
        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if (
            role == Qt.ItemDataRole.DisplayRole
            and orientation == Qt.Orientation.Horizontal
        ):
            return self._headers[section]
        return None
