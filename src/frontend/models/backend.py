import json
import time

from PySide2.QtCore import QProcess, Slot, QByteArray
from PySide2.QtWidgets import QMessageBox

from models.request import Request

LIST_AVAILABLE_CLIENTS_COMMAND = b'{"command": "listAvailableClientTypes"}'

class Backend:
  # Singleton method stuff:
  __instance = None
  @staticmethod
  def get_instance():
    # Static access method.
    if Backend.__instance == None:
        Backend()
    return Backend.__instance

  def __init__(self, app_path):
    self.app_path = app_path
    self.callbacks = {
      'newRequest': [],
      'updatedRequest': [],
      'clientsAvailable': [],
      'clientsChanged': [],
      'requestIntercepted': [],
      'responseIntercepted': []
    }
    self.start()

    # Virtually private constructor.
    if Backend.__instance != None:
        raise Exception("This class is a singleton!")
    else:
        Backend.__instance = self
  # /Singleton method stuff

  def start(self):
    print("Starting the proxy...")
    self.backend = QProcess()
    self.backend.start(f'{self.app_path}/build/oneproxy-backend --basePath={self.app_path}/')
    self.backend.readyReadStandardOutput.connect(self.std_out_received)
    self.backend.readyReadStandardError.connect(self.std_err_received)
    # REMOVE THIS!!!
    # TODO: Make this wait for a "backendStarted" message
    time.sleep(2)

  def kill(self):
    print("Stopping the backend...")
    self.backend.terminate()
    self.backend.waitForFinished(-1)

  def std_out_received(self):
    output = self.backend.readAllStandardOutput()
    lines = str(output, encoding='utf-8').split("\n")

    for line in lines:
      if (line[0:6] == '[JSON]'):
        self.process_json(line[6:].strip())
      else:
        print(line)

  def send_command(self, command):
    print(command)
    command_bytes = QByteArray(command + b'\n')
    self.backend.write(command_bytes)

  def std_err_received(self):
    line = self.backend.readAllStandardError()
    line = str(line, encoding='utf-8')
    self._show_error_box(line)

  def _show_error_box(self, message):
    message_box = QMessageBox()
    message_box.setWindowTitle('Error')
    message_box.setText(message)
    message_box.exec_()

    print(message)

  def register_callback(self, message_type, callback):
    self.callbacks[message_type].append(callback)

  def process_json(self, line):
    try:
      obj = json.loads(line)

      if (obj['type'] == 'newRequest'):
        for callback in self.callbacks['newRequest']:
          request = Request(obj['request'])
          callback(request)

      elif (obj['type'] == 'updatedRequest'):
        print(obj)
        for callback in self.callbacks['updatedRequest']:
          request = Request(obj['request'])
          callback(request)

      elif (obj['type'] == 'clientsAvailable'):
        for callback in self.callbacks['clientsAvailable']:
          callback(obj['clients'])

      elif (obj['type'] == 'clientsChanged'):
        for callback in self.callbacks['clientsChanged']:
          callback()

      elif (obj['type'] == 'requestIntercepted'):
        for callback in self.callbacks['requestIntercepted']:
          callback(obj['request'])

      elif (obj['type'] == 'responseIntercepted'):
        for callback in self.callbacks['responseIntercepted']:
          callback(obj['request'])

    except json.decoder.JSONDecodeError:
      print("[BackendHandler] could not parse json: ")
      print(line)

  #-----------------------------------------------------------------------------
  # Commands:
  #-----------------------------------------------------------------------------
  def get_available_clients(self):
    self.send_command(LIST_AVAILABLE_CLIENTS_COMMAND)

  def open_client(self, client_id):
    command = b'{"command": "openClient", "id": ' + bytes(str(client_id), 'utf8') + b'}'
    self.send_command(command)

  def forward_request(self, request):
    request_json = json.dumps(request)
    command = b'{"command": "forward", "request": ' + bytes(request_json, 'utf8') + b'}'
    self.send_command(command)

  def forward_intercept_request(self, request):
    request_json = json.dumps(request)
    command = b'{"command": "forwardAndIntercept", "request": ' + bytes(request_json, 'utf8') + b'}'
    self.send_command(command)

  def change_setting(self, key, value):
    if (isinstance(value, bool)):
      value = str(value).lower()

    elif (isinstance(value, int)):
      value = str(value)

    else:
      # Otherwise add quotes:
      value = f'"value"'

    key = bytes(key, 'utf8')
    value = bytes(value, 'utf8')
    command = b'{"command": "changeSetting", "key": "' + key + b'", "value": ' + value + b'}'
    self.send_command(command)

