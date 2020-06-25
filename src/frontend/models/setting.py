import json

class Setting:
  def __init__(self, attributes):
    self.id = attributes.get('id')
    self.key = attributes.get('key')
    self.value = attributes.get('value')
