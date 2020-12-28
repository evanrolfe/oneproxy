import json

from PySide2.QtSql import QSqlDatabase, QSqlQuery

from models.capture_filters import CaptureFilters

DEFAULT_CAPTURE_FILTERS = {
  'hostList': [],
  'hostSetting': '',
  'pathList': [],
  'pathSetting': '',
  'extList': [],
  'extSetting': '',
  'navigationRequests': True
}

class CaptureFiltersData:
  def __init__(self):
    self.settings = []

  @classmethod
  def load(cls):
    filters = cls.load_row()

    if (filters == None):
      cls.create_default()
      filters = cls.load_row()

    return filters

  @classmethod
  def save(cls, capture_filters):
    query = QSqlQuery()
    query.prepare("UPDATE capture_filters SET filters=? WHERE id = 1")
    query.bindValue(0, capture_filters.get_filters_json())
    result = query.exec_()

    if (result == False):
      print("THERE WAS AN ERROR WITH THE SQL QUERY!")
    else:
      print("Saved filters")
      print(capture_filters.get_filters_json())

  @classmethod
  def capture_filters_from_query_result(cls, query):
    filters = json.loads(query.value('filters'))
    return CaptureFilters(filters)

  @classmethod
  def load_row(cls):
    query = QSqlQuery()
    query.prepare("SELECT * FROM capture_filters WHERE id = 1")
    query.exec_()
    query.next()

    if (query.first()):
      return cls.capture_filters_from_query_result(query)
    else:
      return None

  @classmethod
  def create_default(cls):
    query = QSqlQuery()
    query.prepare("INSERT capture_filters SET filters=? WHERE id = 1")
    query.prepare("INSERT INTO capture_filters (id, filters) VALUES (1, :filters)")
    query.bindValue(":filters", json.dumps(DEFAULT_CAPTURE_FILTERS))
    result = query.exec_()
    query.next()
