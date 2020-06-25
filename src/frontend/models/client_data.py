from PySide2.QtSql import QSqlDatabase, QSqlQuery

from models.client import Client

class ClientData:
    def __init__(self):
      self.clients = []

    def load_clients(self):
      self.clients = []
      query = QSqlQuery("SELECT * FROM clients ORDER BY id DESC")
      query.exec_()

      while query.next():
        client = self.client_from_query_result(query)
        self.clients.append(client)

    def load_client(self, client_id):
      query = QSqlQuery()
      query.prepare("SELECT * FROM clients WHERE id=:id")
      query.bindValue(":id", client_id)
      query.exec_()
      query.next()

      return self.client_from_query_result(query)

    def client_from_query_result(self, query):
      attrs = {
        'id': query.value('id'),
        'type': query.value('type'),
        'title': query.value('title'),
        'cookies': query.value('cookies'),
        'pages': query.value('pages'),
        'proxy_port': query.value('proxy_port'),
        'browser_port': query.value('browser_port'),
        'open': query.value('open'),
        'launched_at': query.value('launched_at'),
        'created_at': query.value('created_at')
      }

      return Client(attrs)
