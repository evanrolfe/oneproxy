import json

class Crawl:
  def __init__(self, attributes):
    self.id = attributes['id']
    self.client_id = attributes['client_id']
    self.config = attributes['config']
    self.status = attributes['status']
    self.created_at = attributes['created_at']
    self.started_at = attributes['started_at']
    self.finished_at = attributes['finished_at']

  def config_obj(self):
    return self.config
