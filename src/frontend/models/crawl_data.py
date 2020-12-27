import time

from PySide2.QtSql import QSqlDatabase, QSqlQuery

from models.crawl import Crawl

class CrawlData:
    def __init__(self):
      self.crawls = []

    def load_crawls(self):
      self.crawls = []
      query = QSqlQuery("SELECT * FROM crawls ORDER BY id DESC")
      query.exec_()

      while query.next():
        crawl = self.crawl_from_query_result(query)
        self.crawls.append(crawl)

    def load_crawl(self, crawl_id):
      query = QSqlQuery()
      query.prepare("SELECT * FROM crawls WHERE id=:id")
      query.bindValue(":id", crawl_id)
      query.exec_()
      query.next()

      return self.crawl_from_query_result(query)

    def crawl_from_query_result(self, query):
      attrs = {
        'id': query.value('id'),
        'client_id': query.value('client_id'),
        'config': query.value('config'),
        'status': query.value('status'),
        'created_at': query.value('created_at'),
        'started_at': query.value('started_at'),
        'finished_at': query.value('finished_at')
      }

      return Crawl(attrs)

    @classmethod
    def save(cls, crawl):
      created_at = int(round(time.time() * 1000))

      query = QSqlQuery()
      query.prepare("INSERT INTO crawls (client_id, config, status, created_at) VALUES (:client_id, :config, :status, :created_at)")
      query.bindValue(":client_id", crawl.client_id)
      query.bindValue(":config", crawl.config)
      query.bindValue(":status", crawl.status)
      query.bindValue(":created_at", created_at)
      result = query.exec_()
      query.next()

      if (result == False):
        print("THERE WAS AN ERROR WITH THE SQL QUERY!")
      else:
        crawl.id = query.lastInsertId()
        crawl.created_at = created_at
        print(f"Crawl created with id: {crawl.id}")

      return result
