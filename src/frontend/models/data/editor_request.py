from orator import Model

class EditorRequest(Model):
  __table__ = 'editor_requests'

  def children(self):
    return EditorRequest.where('parent_id', '=', self.id).order_by('created_at', 'desc').get()

  def delete_resursive(self):
    for child in self.children():
      child.delete_resursive()

    self.delete()
