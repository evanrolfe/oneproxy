import json

class Client:
  def __init__(self, attributes):
    self.id = attributes['id']
    self.title = attributes['title']
    self.cookies = attributes['cookies']
    self.pages = attributes['pages']
    self.type = attributes['type']
    self.proxy_port = attributes['proxy_port']
    self.browser_port = attributes['browser_port']
    self.open = attributes['open']
    self.created_at = attributes['created_at']
    self.launched_at = attributes['launched_at']

  def open_text(self):
    if (self.open == 1):
      return 'Open'
    else:
      return 'Closed'
