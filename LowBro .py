from PyQt5.QtWidgets import ( QApplication, QMainWindow, QFileDialog,
							QWidget, QHBoxLayout, QVBoxLayout,
							QLabel, QLineEdit, QPushButton, QMenu
							)
from PyQt5.QtCore import Qt, QUrl, QSize, QDir, QFileInfo
from PyQt5.QtGui import QKeySequence, QIcon, QColor, QContextMenuEvent
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings, QWebEngineProfile, QWebEnginePage, QWebEngineDownloadItem

import PyQt5.QtCore as QtCore

# Other Lib
import sys 
import sqlite3 
import datetime


"""    Todo:
			1.show downloads
			2.show history
			3.show menu
			4.show bookmark 
			5.web background color
			6.set home page
			7.settings
			8.tabview
			9.advanced search


"""

class MainWindow(QMainWindow):


	""" Know about : 
				backgroundColor
				icon -> QIcon
				iconUrl -> qUrl
				loading
				isLoading()->bool
				requestedUrl
				selectedText
				createWindow() for new tab
				download(qurl, filename) 
				title -> str >>> 
				history -> QHistory >>>
				reload()  >>>
				stop()  >>>
				loadFinished() >>>
				loadProgress() >>>
				loadStarted()  >>>




				"""



	def __init__(self):
		super().__init__()


		# Default Variables
		# Browser 
		self.ask_download = True
		self.downlaoding_list : list = []
		self.file_style_main = "./src/styles/style_sheet_main.qcc"
		self.file_database = "./src/database.db"
		self.default_path = "C:/Users/Welcome/Downloads/"
		self.current_path = "C:/Users/Welcome/Downloads/"
		self.default_page : str = "https://feathericons.com/?query="
		self.default_page : QUrl = QUrl(self.default_page)
		# Others
		self.default_backgroud_color = "#282828"


		self.setWindowTitle("LowBrow")
		self.resize(900, 600)
		self.style_sheet()

		#"https://www.youtube.com/watch?v=AiD6SOOBKZI"
		#"https://www.youtube.com/watch?v=IZHGcU0U_W0"
		#"https://feathericons.com/?query="
		#"file:///G:/Python/Files/PyQt5/test/temp/roadmap_python.mp4"
		#"www.google.com"
		#"file:///G:/Python/Files/PyQt5/test/temp/web/New%20Tab.htm"

		# Label

		# PushButton
		self.btn_go = QPushButton()
		self.btn_back = QPushButton()
		self.btn_forward = QPushButton()
		self.browser_icon = QPushButton()
		self.btn_download = QPushButton()
		self.btn_refresh = QPushButton()
		self.btn_bookmark = QPushButton()
		self.btn_home = QPushButton()
		self.btn_menu = QPushButton()
		self.btn_settings = QPushButton()

		self.spacer_home_to_edit = QPushButton()
		self.spacer_book_to_download = QPushButton()

		# Clipboard 
		self.clipboard = QApplication.clipboard()

		# Menus
		self.context_menu = QMenu()
		# Actions
		self.action_copy = self.context_menu.addAction("Copy")
		self.action_save_as = self.context_menu.addAction("Save as")
		self.action_new_window = self.context_menu.addAction("Open new Window")
		self.action_new_tab = self.context_menu.addAction("Open New Tab")
		self.action_quit = self.context_menu.addAction("Quit")

		self.edit_url = QLineEdit()

		self.hbox_top = QHBoxLayout()
		self.vbox = QVBoxLayout()

		self.browser = Browser()
		
		self.settings_browser = QWebEngineSettings.globalSettings()
		self.browser_profile = QWebEngineProfile(f"storage-{1}", self.browser)
		self.browser_page = QWebEnginePage(self.browser_profile, self.browser)
		self.browser.setPage(self.browser_page)
		self.other = Other(self)
		self.history = self.other.get_data("history")

		# Status Bar
		self.statusBar().showMessage(self.default_path)
		#self.statusBar().addWidget(self.label)

		# Main UI Setup
		self.initUI()

	def initUI(self):
		self.main_centeral_widget = QWidget()
		self.setCentralWidget(self.main_centeral_widget)

		# Action Shortcuts
		self.action_copy.setShortcut("ctrl+c")
		self.action_save_as.setShortcut('ctrl+s')
		self.action_new_tab.setShortcut('ctrl+t')
		self.action_new_window.setShortcut('Ctrl+n')
		self.action_quit.setShortcut('ctrl+q')

		self.context_menu.setStyleSheet("""
				QMenu{
					background-color: #212121;
					color: #ffffff;
					font-family: arial;
					padding : 3px;
					}
				QMenu:chunk {
				background-color : #515151;

				}
				""")
		
		#print(self.settings_browser.getAttribute())
		# Disable Spacer
		self.spacer_home_to_edit.setDisabled(True)
		self.spacer_book_to_download.setDisabled(True)
		
		#self.edit_url.setMaximumHeight( 60)
		self.edit_url.setMinimumHeight( 30)
		self.edit_url.setMinimumWidth(600)
		self.edit_url.setMaximumWidth(900)

		# Set 
		self.btn_back.setMinimumHeight(30)
		self.btn_back.setMaximumWidth( 30)
		self.btn_forward.setMinimumHeight(30)
		self.btn_forward.setMaximumWidth( 30)
		self.btn_go.setMinimumHeight(30)
		self.btn_go.setMaximumWidth( 30)
		self.btn_refresh.setMinimumHeight(30)
		self.btn_refresh.setMaximumWidth(30)
		self.btn_bookmark.setMinimumHeight(30)
		self.btn_bookmark.setMaximumWidth(30)
		self.btn_download.setMinimumHeight(30)
		self.btn_download.setMaximumWidth(30)
		self.btn_menu.setMinimumHeight(30)
		self.btn_menu.setMaximumWidth(30)

		self.browser_icon.setMinimumHeight( 30)
		self.browser_icon.setMaximumWidth( 30)

		self.btn_go.setShortcut(QKeySequence( Qt.Key_Enter))

		# Set Icons
		self.btn_back.setIcon(QIcon("./src/icon/chevron-left_white.svg"))
		self.btn_forward.setIcon(QIcon("./src/icon/chevron-right_white.svg"))
		self.btn_go.setIcon(QIcon("./src/icon/search_white.svg"))
		self.btn_refresh.setIcon(QIcon("./src/icon/refresh-cw_white.svg"))
		self.btn_bookmark.setIcon(QIcon("./src/icon/bookmark.whitesvg.svg"))
		self.btn_menu.setIcon(QIcon("./src/icon/menu_white.svg"))
		self.btn_home.setIcon(QIcon("./src/icon/home_white.svg"))
		self.btn_settings.setIcon(QIcon("./src/icon/settings_white.svg"))
		self.btn_download.setIcon(QIcon("./src/icon/download_white.svg"))
		self.browser_icon.setIcon(QIcon("./src/icon/globe_white.svg"))

		# Set Icon Size 
		self.browser_icon.setIconSize(QSize(20, 20))
		self.btn_back.setIconSize(QSize(25, 25))
		self.btn_forward.setIconSize(QSize(25, 25))
		self.btn_go.setIconSize(QSize(20, 20))
		self.btn_home.setIconSize(QSize(25, 25))
		self.btn_bookmark.setIconSize(QSize(20, 20))
		self.btn_download.setIconSize(QSize(20, 20))
		self.btn_refresh.setIconSize(QSize(20, 20))
		self.btn_menu.setIconSize(QSize(20, 20))

		self.settings_browser.setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
		self.settings_browser.setAttribute(QWebEngineSettings.PluginsEnabled, True)

		# Button Clicked Signal 
		self.btn_go.clicked.connect(lambda: self.load_url(self.edit_url.text()))
		self.edit_url.returnPressed.connect(lambda: self.load_url(self.edit_url.text()))
		self.btn_back.clicked.connect(self.browser.back)
		self.btn_forward.clicked.connect(self.browser.forward)
		self.btn_refresh.clicked.connect(self.url_refresh_stop_stop)
		self.btn_bookmark.clicked.connect(self.add_bookmark)
		self.btn_menu.clicked.connect(self.show_menu)
		self.btn_download.clicked.connect(self.show_downloads)
		# Action Clicked Signal
		self.action_quit.triggered.connect(sys.exit)
		self.action_copy.triggered.connect(self.coping_text)
		self.action_new_window.triggered.connect(self.new_window)

		self.browser.context_menu = self.context_menu

		self.browser.urlChanged.connect(self.url_changed)
		self.browser.loadStarted.connect(self.url_loading)
		self.browser.loadFinished.connect(self.url_loaded)
		self.browser_page.linkHovered.connect(self.link_selected)

		# Request Signal Handler
		self.browser_page.fullScreenRequested.connect(self.full_screen_req)
		self.browser_profile.downloadRequested.connect(self.download_file)


		#self.hbox_top.setAlignment(Qt.AlignTop)
		self.hbox_top.addWidget(self.btn_back)
		self.hbox_top.addWidget(self.btn_forward)
		self.hbox_top.addWidget(self.btn_refresh)
		self.hbox_top.addWidget(self.spacer_home_to_edit)
		self.hbox_top.addWidget(self.browser_icon)
		self.hbox_top.addWidget(self.edit_url)
		self.hbox_top.addWidget(self.btn_bookmark)
		self.hbox_top.addWidget(self.spacer_book_to_download)
		self.hbox_top.addWidget(self.btn_download)
		self.hbox_top.addWidget(self.btn_menu)

		self.vbox.addLayout(self.hbox_top)
		self.vbox.addWidget(self.browser)
		self.main_centeral_widget.setLayout(self.vbox)

		self.load_url()

	def main_icon(self, url: QUrl = QUrl("www.google.com")):
		print("\n{url}  Icon Url >>>>",self.browser_page.iconUrl())

	def update_window(self):
		self.setWindowTitle(self.browser_page.title())
		self.setWindowIcon(self.browser_page.icon())
		print("WIndow icon >>>>>",self.browser_page.iconUrl())

	def url_changed(self):
		url = self.browser.url().toString()
		print(f" Url <<<< {url} \n >>>>")
		self.edit_url.setText(url)
		time = datetime.datetime.now()
		#print("current time:", time)
		self.other.add_history("history",url , time.timestamp())

	def load_url(self,url : str =""):
		if url == "":
			url = self.default_page
		q_url = QUrl(url)
		if not q_url.scheme():
			q_url.setScheme("https")
			#url = "https://"+url

		print(q_url.toString())
		self.browser.setUrl(q_url)

	def url_loading(self):
		print("loading....")
		self.loading = True
		self.btn_refresh.setIcon(QIcon("./src/icon/cancel_x_white.svg"))

	def url_loaded(self):
		print("loaded")
		self.loading = False
		self.btn_refresh.setIcon(QIcon("./src/icon/refresh-cw_white.svg"))
		self.update_window()

		print(f"\n Title >>>> {self.browser_page.title()} \n")
		
		print(f"Url Loaded {self.browser_page.icon()}")
		self.browser_icon.setIcon(self.browser_page.icon())
		print("###### back Color -----> ",self.browser_page.backgroundColor())
		self.browser_page.setBackgroundColor(QColor(self.default_backgroud_color))

	def url_refresh_stop_stop(self):
		if self.loading:
			self.browser.stop()
		else:
			self.browser.reload()
			#print("\n ----Refersh---- \n")

	def add_bookmark(self):
		value = self.other.add_data("bookmark",self.browser.url().toString())
		if value == "Success":
			print("add_bookmark >>>> added")
		elif value.startswith("UNIQUE constraint failed:"):
			print("add_bookmark >>>> Bookmark is already exits")
		else:
			print("add_bookmark >>>> ", value)

	def show_menu(self):
		self.req_url = self.browser_page.requestedUrl()
		book = self.other.get_data("bookmark")
		print(f"get {self.req_url} bookmark >>>>> ", book)

	
	def download_file(self, downlaod : QWebEngineDownloadItem):

		# Ask Before Download On
		if self.ask_download:
			# Ask where to save file
			path, _ = QFileDialog.getSaveFileName(self, "Save as", self.current_path+downlaod.downloadFileName())

		# Ask Before Download Off
		else:
			# Save that on default path ex : C:/Users/Welcome/Downloads/ + ex.txt
			path = self.default_path+str(downlaod.downloadFileName())
		# Download Path is Null
		if path == "":
			return

		# Set Download File Details
		downlaod.setDownloadFileName(QFileInfo(path).fileName())
		self.current_path = QFileInfo(path).path()+"/"
		downlaod.setDownloadDirectory(QFileInfo(path).path())

		print(f"\n filesize = {downlaod.totalBytes()} default_path = {self.current_path} filetype = {downlaod.type()}\n")
		# Start Downloading File
		downlaod.accept()
		
		# Add in Downloading List
		self.downlaoding_list.append(downlaod.path())
		# Show Download Progress Signal
		downlaod.downloadProgress.connect(self.download_progress)
		# Show Download Finished Signal
		downlaod.finished.connect(lambda : self.download_finished(downlaod))
		self.statusBar().showMessage(f"Downloading... {downlaod.path()}", 2000)
		

	def download_progress(self, recv_byte, total_byte):
		
		recv_byte = (recv_byte/1024)/1024
		total_byte= int((total_byte/1024)/1024)
		#if recv_byte == recv_byte
		print(f"\n Download Progress {recv_byte} Mb/{total_byte} Mb")
		"""# bytes to Mb
		if int(total_byte/1024) > 1024:
			print("is Mb") 
		else:
			print("is Kb")
			recv_byte = int(recv_byte/1024)
			total_byte= int(total_byte/1024) """

	def download_finished(self, downlaod):
		for x in range(len(self.downlaoding_list)):
			if self.downlaoding_list[x] == downlaod.path():
				self.statusBar().showMessage(f"File: {downlaod.path()} Downloaded Successfully ", 4000)
				print(f"File: {downlaod.path()} Downloaded Successfully ")
				self.downlaoding_list.pop(x)
				break

		print(" add download ===>",self.other.add_download(downlaod.url().toString(), downlaod.path(), int(datetime.datetime.now().timestamp()), "started", 0, 0))
		
		
	def show_downloads(self):
		downloads = self.other.get_data("downloads")

		for downlaod in downloads:
			print(downlaod)

	def coping_text(self):
		text = self.req_url.toString()
		# Text Selected 

		if text == "":
			text = self.browser_page.selectedText()
		# by default Url
		self.clipboard.setText(text, mode= self.clipboard.Clipboard)

		# Show Message(str:text, time:ms)
		self.statusBar().showMessage(f"{text} is Copied", 2000)
		#pyperclip.copy(text)

	def link_selected(self, url):
		print(f"Link Selected ---> _{url}_")
		self.req_url = QUrl(url)
        
	def new_window(self):
		new = MainWindow()
		print(f"request ===> {self.req_url}")
		if not str(self.req_url) == "PyQt5.QtCore.QUrl('')":
			new.browser.setUrl(self.req_url)
		else:
			new.browser.setUrl(self.browser_page.requestedUrl())
		new.show()

	@QtCore.pyqtSlot("QWebEngineFullScreenRequest")
	def full_screen_req(self, request):
		request.accept()
		if request.toggleOn():
			print("toggle On")
			self.browser.setParent(None)
			self.browser.showFullScreen()
		else:
			print("toggle Off") 
			#self.setCentralWidget(self.browser)
			self.vbox.addWidget(self.browser)
			self.main_centeral_widget.setLayout(self.vbox)
			self.browser.showNormal()
		

	def style_sheet(self):
		try:
			with open(self.file_style_main, 'r') as f:
				self.setStyleSheet(f.read())
				f.close()
		except FileNotFoundError as e:
			print(e)

class Browser(QWebEngineView):
	def __init__(self):
		super().__init__()
		self.setStyleSheet("""

			background-color: #212121;

			""")

	# Left Mouse Clicked Event
	def contextMenuEvent(self, event):
		self.context_menu.exec(event.globalPos())


class Other():

	def __init__(self,main:MainWindow):
		super().__init__()
		# Default Variable
		self.db = sqlite3.connect(main.file_database)
		self.cursor = self.db.cursor()

		# Create History Table  
		self.cursor.execute(""" CREATE TABLE IF NOT EXISTS history (
								id INTEGER PRIMARY KEY AUTOINCREMENT, 
								url STRING NOT NULL, 
								time_ids TIMESTAMP NOT NULL)
		""")

		# Create Bookmark Table  
		self.cursor.execute(""" CREATE TABLE IF NOT EXISTS bookmark (
								id INTEGER PRIMARY KEY AUTOINCREMENT,
								url STRING NOT NULL UNIQUE
								) """)
		# Create Downloads Table 
		self.cursor.execute(""" CREATE TABLE IF NOT EXISTS downloads (
								id INTEGER PRIMARY KEY AUTOINCREMENT, 
								url STRING NOT NULL, 
								path STRING NOT NULL UNIQUE,
								time TIMESTAMP NOT NULL,
								state STRING DEFAULT "progress",
								t_size int DEFAULT 0,
								c_size int DEFAULT 0 )
		""")


		#self.cursor.execute(""" DROP TABLE  history""")
		#self.db.commit()


	def add_history(self, tabel_name, url : str , time ) -> str :
		try:
			self.cursor.execute(""" INSERT INTO {} (url, time_ids) VALUES ("{}", {}) """.format(tabel_name, url, time))
			self.db.commit()
			return "Success"
		except Exception as e:
			return str(e)

	def add_download(self, url: str, path: str, time, state: str, total_size:int, current_size: int) -> str:
		try:
			self.cursor.execute(""" INSERT INTO downloads (url, path, state, time, t_size, c_size) 
								VALUES ("{}", "{}", "{}", {}, {}, {})""".format(url, path, state, time, total_size, current_size))
			return "Success"
		except Exception as e:
			return str(e)


	def add_data(self, tabel_name, url : str  ) -> str :
		try:
			self.cursor.execute(""" INSERT INTO {} (url) VALUES ("{}") """.format(tabel_name, url))
			self.db.commit()
			return "Success"
		except Exception as e:
			return str(e)

	def get_data(self, tabel_name:str , time: str = "") -> list or str :
		try:
			if time == "":
				self.cursor.execute(""" SELECT * FROM {} """.format(tabel_name))
			else:
				self.cursor.execute(""" SELECT * FROM {} WHERE time = {} """.format(tabel_name, time))
			return self.cursor.fetchall()
		except Exception as e:
			return str(e)

	def update_data(self, tabel_name: str, id: int, url : str) -> str:
		try:
			self.cursor.execute(""" UPDATE {} SET url = {} WHERE id = {} ;""".format(tabel_name, url, id))
		except Exception as e:
			return str(e)


	def delete_data(self,tabel_name: str,id) -> str:
		try:
			self.cursor.execute("DELETE FROM {} WHERE id = {}".format(tabel_name, id))
			return "Success"
		except Exception as e:
			return str(e)

if __name__ == "__main__":
	app = QApplication([])

	window = MainWindow()
	window.show()

	sys.exit(app.exec_())



