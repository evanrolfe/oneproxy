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
