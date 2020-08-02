from PySide2.QtCore import QAbstractTableModel, QModelIndex, Qt, QObject, Slot, Signal

from operator import itemgetter, attrgetter

from models.backend import Backend

class RequestsTableModel(QAbstractTableModel):
  def __init__(self,request_data, parent = None):
    QAbstractTableModel.__init__(self, parent)
    self.headers = ['ID', 'Source', 'Method', 'Host', 'Path', 'Status', 'Modified']
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

      row_values = [
        request.id,
        request.client_id,
        request.method,
        request.host,
        request.path,
        request.response_status,
        request.modified()
      ]

      return row_values[index.column()]


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
      self.request_data.requests = sorted(self.request_data.requests, key=lambda r: [r.host, r.id], reverse=reverse)
    elif (column == 4):
      self.request_data.requests = sorted(self.request_data.requests, key=lambda r: [r.path, r.id], reverse=reverse)
    elif (column == 5):
      self.request_data.requests = sorted(self.request_data.requests, key=self.response_status_sort_key, reverse=reverse)

    self.dataChanged.emit(QModelIndex(), QModelIndex())

  def response_status_sort_key(self, request):
    if (request.response_status == ''):
      status = 0
    else:
      status = int(request.response_status)

    return [status, request.id]
