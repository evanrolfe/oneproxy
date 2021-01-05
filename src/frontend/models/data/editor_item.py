from orator import Model
from models.data.editor_request import EditorRequest

class EditorItem(Model):
  __table__ = 'editor_items'

  def children(self):
    return EditorItem.where('parent_id', '=', self.id).order_by('item_type', 'asc').get()

  def delete_everything(self):
    self.delete_resursive()
    self.item().delete()

  def delete_resursive(self):
    for child in self.children():
      child.delete_resursive()

    self.delete()

  def item(self):
    if self.item_type == 'request':
      return EditorRequest.where('id', '=', self.item_id).first()

  def save(self, *args, **kwargs):
    item_id = getattr(self, 'item_id', None)

    if self.item_type == 'request' and item_id == None:
      request = EditorRequest()
      request.save()
      print(f'Created request id {request.id}')
      self.item_id = request.id

    super(EditorItem, self).save(*args, **kwargs)
