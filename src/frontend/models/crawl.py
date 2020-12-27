import json

class Crawl:
  def __init__(self, attributes):
    self.id = attributes.get('id')
    self.client_id = attributes.get('client_id')
    self.config = attributes.get('config')
    self.status = attributes.get('status')
    self.created_at = attributes.get('created_at')
    self.started_at = attributes.get('started_at')
    self.finished_at = attributes.get('finished_at')

  def config_obj(self):
    return self.config
