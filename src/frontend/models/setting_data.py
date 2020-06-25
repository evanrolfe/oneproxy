from PySide2.QtSql import QSqlDatabase, QSqlQuery

from models.setting import Setting

class SettingData:
  def __init__(self):
    self.settings = []

  @classmethod
  def intercept_enabled(cls):
    setting = cls.load('interceptEnabled')
    return (setting.value == '1')

  @classmethod
  def load(cls, key):
    query = QSqlQuery()
    query.prepare("SELECT * FROM settings WHERE key=:key")
    query.bindValue(":key", key)
    query.exec_()
    query.next()

    return cls.setting_from_query_result(query)

  @classmethod
  def setting_from_query_result(cls, query):
    attrs = {
      'id': query.value('id'),
      'key': query.value('key'),
      'value': query.value('value')
    }

    return Setting(attrs)
