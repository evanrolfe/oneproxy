# Clients Page:
pyside2-uic src/frontend/views/clients/clients_page.ui > src/frontend/views/_compiled/clients/ui_clients_page.py
pyside2-uic src/frontend/views/clients/clients_table.ui > src/frontend/views/_compiled/clients/ui_clients_table.py
pyside2-uic src/frontend/views/clients/client_view.ui > src/frontend/views/_compiled/clients/ui_client_view.py

# Crawls Page:
pyside2-uic src/frontend/views/crawls/crawls_page.ui > src/frontend/views/_compiled/crawls/ui_crawls_page.py
pyside2-uic src/frontend/views/crawls/crawls_table.ui > src/frontend/views/_compiled/crawls/ui_crawls_table.py
pyside2-uic src/frontend/views/crawls/crawl_view.ui > src/frontend/views/_compiled/crawls/ui_crawl_view.py
pyside2-uic src/frontend/views/crawls/new_crawl.ui > src/frontend/views/_compiled/crawls/ui_new_crawl.py

# Network Page:
pyside2-uic src/frontend/views/network/network_page_widget.ui > src/frontend/views/_compiled/network/ui_network_page_widget.py
pyside2-uic src/frontend/views/network/network_requests_table_tabs.ui > src/frontend/views/_compiled/network/ui_network_requests_table_tabs.py
pyside2-uic src/frontend/views/network/network_requests_table.ui > src/frontend/views/_compiled/network/ui_network_requests_table.py
pyside2-uic src/frontend/views/network/network_display_filters.ui > src/frontend/views/_compiled/network/ui_network_display_filters.py
pyside2-uic src/frontend/views/network/network_capture_filters.ui > src/frontend/views/_compiled/network/ui_network_capture_filters.py

# Intercept Page:
pyside2-uic src/frontend/views/intercept/intercept_page.ui > src/frontend/views/_compiled/intercept/ui_intercept_page.py

# Requests Page:
pyside2-uic src/frontend/views/requests/request_group_view.ui > src/frontend/views/_compiled/requests/ui_request_group_view.py
pyside2-uic src/frontend/views/requests/requests_page.ui > src/frontend/views/_compiled/requests/ui_requests_page.py

# Shared:
pyside2-uic src/frontend/views/shared/request_view.ui > src/frontend/views/_compiled/shared/ui_request_view.py

# HACK: pyside2-uic does not import the QWebEngineView so we have to add this line manually:
# BE CAREFUL when changing this file as this line will easily break!
line=`sed "18q;d" src/frontend/views/_compiled/shared/ui_request_view.py`
if ! [[ $line =~ "qwebengineview" ]]; then
  echo "WARNING: src/frontend/views/_compiled/shared/ui_request_view.py does not contain qwebengineview on line 18 as expected.";
fi

sed -i '18s/.*/from PySide2.QtWebEngineWidgets import QWebEngineView/' src/frontend/views/_compiled/shared/ui_request_view.py
# /HACK

# Mainwindow:
pyside2-uic src/frontend/views/new_client_modal.ui > src/frontend/views/_compiled/ui_new_client_modal.py
pyside2-uic src/frontend/views/main_window.ui > src/frontend/views/_compiled/ui_main_window.py
