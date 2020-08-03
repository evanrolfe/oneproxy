from PySide2.QtSql import QSqlDatabase, QSqlQuery

from models.request import Request

class RequestData:
    def __init__(self):
      self.requests = []

    def update_request(self, new_request):
      for i, request in enumerate(self.requests):
        if request.id == new_request.id:
          self.requests[i] = new_request

    def get_index_of(self, request):
      for i, r in enumerate(self.requests):
        if r.id == request.id:
          return i

    def load_requests(self):
      query = QSqlQuery("SELECT * FROM requests ORDER BY id DESC")

      while query.next():
        request = self.request_from_query_result(query)
        self.requests.append(request)

    def load_request(self, request_id):
      query = QSqlQuery()
      query.prepare("SELECT * FROM requests WHERE id=:id")
      query.bindValue(":id", request_id)
      query.exec_()
      query.next()

      return self.request_from_query_result(query)

    def request_from_query_result(self, query):
      attrs = {
        'id': query.value('id'),
        'client_id': query.value('client_id'),
        'method': query.value('method'),
        'host': query.value('host'),
        'path': query.value('path'),
        'encrypted': query.value('encrypted'),
        'http_version': query.value('http_version'),
        'request_headers': query.value('request_headers'),
        'request_payload': query.value('request_payload'),

        'request_modified': query.value('request_modified'),
        'modified_method': query.value('modified_method'),
        'modified_url': query.value('modified_url'),
        'modified_host': query.value('modified_host'),
        'modified_http_version': query.value('modified_http_version'),
        'modified_path': query.value('modified_path'),
        'modified_ext': query.value('modified_ext'),
        'modified_request_headers': query.value('modified_request_headers'),
        'modified_request_payload': query.value('modified_request_payload'),

        'response_headers': query.value('response_headers'),
        'response_status': query.value('response_status'),
        'response_status_message': query.value('response_status_message'),
        'response_http_version': query.value('response_http_version'),
        'response_body': query.value('response_body'),
        'response_body_rendered': query.value('response_body_rendered'),

        'response_modified': query.value('response_modified'),
        'modified_response_status': query.value('modified_response_status'),
        'modified_response_status_message': query.value('modified_response_status_message'),
        'modified_response_http_version': query.value('modified_response_http_version'),
        'modified_response_headers': query.value('modified_response_headers'),
        'modified_response_body': query.value('modified_response_body'),
        'modified_response_body_length': query.value('modified_response_body_length'),
      }

      return Request(attrs)
