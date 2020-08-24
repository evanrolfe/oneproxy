import json

from PySide2.QtSql import QSqlDatabase, QSqlQuery

from models.capture_filters import CaptureFilters

class CaptureFiltersData:
  def __init__(self):
    self.settings = []

  @classmethod
  def load(cls):
    query = QSqlQuery()
    query.prepare("SELECT * FROM capture_filters WHERE id = 1")
    query.exec_()
    query.next()

    return cls.capture_filters_from_query_result(query)

  @classmethod
  def capture_filters_from_query_result(cls, query):
    filters = json.loads(query.value('filters'))
    return CaptureFilters(filters)
