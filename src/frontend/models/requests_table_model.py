from PySide2.QtCore import QAbstractTableModel, QModelIndex, Qt, QObject, Slot, Signal

from operator import itemgetter, attrgetter

from models.backend import Backend

class RequestsTableModel(QAbstractTableModel):
  def __init__(self,request_data, parent = None):
    QAbstractTableModel.__init__(self, parent)
    self.headers = ['ID', 'Source', 'Method', 'URL']
    self.request_data = request_data

    # Register callback with the backend:
    self.backend = Backend.get_instance()
    self.backend.register_callback('newRequest', self.add_request)

  def add_request(self, request):
    rowIndex = 0
    self.beginInsertRows(QModelIndex(), rowIndex, rowIndex)
    self.request_data.requests.insert(0, request)
    self.endInsertRows()

  def roleNames(self):
    roles = {}
    for i, header in enumerate(self.headers):
      roles[Qt.UserRole + i + 1] = header.encode()
    return roles

  def headerData(self, section, orientation, role = Qt.DisplayRole):
    if role == Qt.DisplayRole and orientation == Qt.Horizontal:
      return self.headers[section]

    return None

  def columnCount(self, parent):
    return len(self.headers)

  def rowCount(self, index):
    return len(self.request_data.requests)

  def data(self, index, role):
    if role == Qt.DisplayRole:
      if not index.isValid():
        return None

      if index.row() > len(self.request_data.requests):
        return None

      request = self.request_data.requests[index.row()]

      if (index.column() == 0):
        return request.id
      elif (index.column() == 1):
        return request.client_id
      elif (index.column() == 2):
        return request.method
      elif (index.column() == 3):
        return request.url

  @Slot(result="QVariantList")
  def roleNameArray(self):
    return self.headers

  def sort(self, column, order):
    self.sortOrder = order
    self.sortColumn = column

    if (order == Qt.AscendingOrder):
      print(f"Sorting column {column} ASC")
    elif (order == Qt.DescendingOrder):
      print(f"Sorting column {column} DESC")

    reverse = (order == Qt.DescendingOrder)

    if (column == 0):
      self.request_data.requests = sorted(self.request_data.requests, key=lambda r: r.id, reverse=reverse)
    elif (column == 1):
      self.request_data.requests = sorted(self.request_data.requests, key=lambda r: r.client_id, reverse=reverse)
    elif (column == 2):
      self.request_data.requests = sorted(self.request_data.requests, key=lambda r: [r.method, r.id], reverse=reverse)
    elif (column == 3):
      self.request_data.requests = sorted(self.request_data.requests, key=lambda r: [r.url, r.id], reverse=reverse)

    self.dataChanged.emit(QModelIndex(), QModelIndex())
