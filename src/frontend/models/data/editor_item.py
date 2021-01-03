from orator import Model

class EditorItem(Model):
  __table__ = 'editor_items'

  def children(self):
    return EditorItem.where('parent_id', '=', self.id).get()

  def delete_resursive(self):
    for child in self.children():
      child.delete_resursive()

    self.delete()