# Clients Page:
pyside2-uic src/frontend/ui/clients/clients_page.ui > src/frontend/ui_compiled/clients/ui_clients_page.py
pyside2-uic src/frontend/ui/clients/clients_table.ui > src/frontend/ui_compiled/clients/ui_clients_table.py
pyside2-uic src/frontend/ui/clients/client_view.ui > src/frontend/ui_compiled/clients/ui_client_view.py

# Network Page:
pyside2-uic src/frontend/ui/network/network_page_widget.ui > src/frontend/ui_compiled/network/ui_network_page_widget.py
pyside2-uic src/frontend/ui/network/network_requests_table.ui > src/frontend/ui_compiled/network/ui_network_requests_table.py
pyside2-uic src/frontend/ui/network/network_display_filters.ui > src/frontend/ui_compiled/network/ui_network_display_filters.py
pyside2-uic src/frontend/ui/network/network_capture_filters.ui > src/frontend/ui_compiled/network/ui_network_capture_filters.py

# Intercept Page:
pyside2-uic src/frontend/ui/intercept/intercept_page.ui > src/frontend/ui_compiled/intercept/ui_intercept_page.py

# Requests Page:
pyside2-uic src/frontend/ui/requests/requests_page.ui > src/frontend/ui_compiled/requests/ui_requests_page.py

# Shared:
pyside2-uic src/frontend/ui/shared/request_view.ui > src/frontend/ui_compiled/shared/ui_request_view.py

# HACK: pyside2-uic does not import the QWebEngineView so we have to add this line manually:
# BE CAREFUL when changing this file as this line will easily break!
line=`sed "18q;d" src/frontend/ui_compiled/shared/ui_request_view.py`
if ! [[ $line =~ "qwebengineview" ]]; then
  echo "WARNING: src/frontend/ui_compiled/shared/ui_request_view.py does not contain qwebengineview on line 18 as expected.";
fi

sed -i '18s/.*/from PySide2.QtWebEngineWidgets import QWebEngineView/' src/frontend/ui_compiled/shared/ui_request_view.py
# /HACK

# Mainwindow:
pyside2-uic src/frontend/ui/new_client_modal.ui > src/frontend/ui_compiled/ui_new_client_modal.py
pyside2-uic src/frontend/ui/main_window.ui > src/frontend/ui_compiled/ui_main_window.py
