class CaptureFilters:
  def __init__(self, attributes):
    self.host_list = attributes.get('hostList')
    self.host_setting = attributes.get('hostSetting')

    self.path_list = attributes.get('pathList')
    self.path_setting = attributes.get('pathSetting')

    self.ext_list = attributes.get('extList')
    self.ext_setting = attributes.get('extSetting')

    self.navigation_requests = attributes.get('navigationRequests')
