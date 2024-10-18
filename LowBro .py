from PyQt5.QtWidgets import ( QApplication, QMainWindow, QFileDialog,
							QWidget, QHBoxLayout, QVBoxLayout,
							QLabel, QLineEdit, QPushButton, QProgressBar,
							 QMenu, QWidgetAction
							)
from PyQt5.QtCore import Qt, QUrl, QSize, QDir, QFileInfo, QPoint
from PyQt5.QtGui import QKeySequence, QIcon, QColor, QContextMenuEvent, QPixmap
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings, QWebEngineProfile, QWebEnginePage, QWebEngineDownloadItem

import PyQt5.QtCore as QtCore

# Other Lib
import sys 
import sqlite3 
import datetime
# Own Module
from QtRecyclerView import QRecyclerView
from Layouts import DownloadLayout


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
		self.downloading_list : list = []
		self.file_style_main = "./src/styles/style_sheet_main.qcc"
		self.file_database = "./src/database.db"
		self.default_path = "C:/Users/Welcome/Downloads/"
		self.current_path = "C:/Users/Welcome/Downloads/"
		self.default_page : str = "https://www.google.com/"
		self.default_page : QUrl = QUrl(self.default_page)
		# Others
		self.default_backgroud_color = "#282828"


		self.setWindowTitle("LowBrow")
		self.resize(900, 600)
		self.style_sheet()

		#"https://www.youtube.com/watch?v=AiD6SOOBKZI" Manasulayo song
		#"https://www.youtube.com/watch?v=IZHGcU0U_W0" Matta SOng
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

		# RecylerView
		self.download_view = QRecyclerView()
		self.download_action = QWidgetAction(None)
		self.download_widget= QWidget()
		self.download_menu = QMenu()

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
		#self.other.delete_tabel('downloads')

		self.settings_browser = self.browser.settings()
		# Status Bar
		#self.statusBar().showMessage(self.default_path)
		#self.statusBar().addWidget(self.label)

		# Main UI Setup
		self.initUI()

	def initUI(self):
		self.main_centeral_widget = QWidget()
		self.setCentralWidget(self.main_centeral_widget)

		# Setting Download View
		self.download_view.setLayoutSize(150, 60)

		# Action Shortcuts
		self.action_copy.setShortcut("ctrl+c")
		self.action_save_as.setShortcut('ctrl+s')
		self.action_new_tab.setShortcut('ctrl+t')
		self.action_new_window.setShortcut('Ctrl+n')
		self.action_quit.setShortcut('ctrl+q')

		# Action Icon
		self.action_copy.setIcon(QIcon('./src/icon/clipboard_white.svg'))
		self.action_save_as.setIcon(QIcon('./src/icon/save_white.svg'))
		#self.action_new_window.setIcon(QIcon('./src/icon/.svg'))
		#self.action_new_tab.setIcon(QIcon('./src/icon/clipboard_white.svg'))
		self.action_quit.setIcon(QIcon('./src/icon/x_white.svg'))



		self.context_menu.setStyleSheet("""
				QMenu{
					background-color: #212121;
					color: #ffffff;
					font-family: arial;
					padding : 3px;
					border-style: solid;
					border-color : #616161;
					border-width : 1px;
				}
				QMenu:hover {
				background-color : #ffffff;

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
			url = url.toString()
		
		if not url == "https://www.google.com/" or url == "www.google.com":
			if not url.startswith("www.") or not url.endswith(".com"):
				url = url.replace(" ","+")
				url = f"https://www.google.com/search?q={url}" 
		#https://www.google.com/search?q=pyqtsignal+pyside6

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

	
	def download_file(self, download : QWebEngineDownloadItem):

		# Ask Before Download On
		if self.ask_download:
			# Ask where to save file
			path, _ = QFileDialog.getSaveFileName(self, "Save as", self.current_path+download.downloadFileName())

		# Ask Before Download Off
		else:
			# Save that on default path ex : C:/Users/Welcome/Downloads/ + ex.txt
			path = self.default_path+str(download.downloadFileName())
		# Download Path is Null
		if path == "":
			return

		# Set Download File Details
		download.setDownloadFileName(QFileInfo(path).fileName())
		self.current_path = QFileInfo(path).path()+"/"
		download.setDownloadDirectory(QFileInfo(path).path())

		print(f"\n filesize = {download.totalBytes()} default_path = {self.current_path} filetype = {download.type()}\n")
		# Start Downloading File
		download.accept()
		
		# Add in Downloading List
		self.downloading_list.append(download.path())
		# Show Download Progress Signal
		download.downloadProgress.connect(self.download_progress)
		# Show Download Finished Signal
		download.finished.connect(lambda : self.download_finished(download))
		self.statusBar().showMessage(f"Downloading... {download.path()}", 2000)
		

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

	def download_finished(self, download):
		for x in range(len(self.downloading_list)):
			if self.downloading_list[x] == download.path():
				self.statusBar().showMessage(f"File: {download.path()} Downloaded Successfully ", 4000)
				print(f"File: {download.path()} Downloaded Successfully ")
				self.downloading_list.pop(x)
				break

		print(" add download ===>",self.other.add_download(download.url().toString(), download.path(), int(datetime.datetime.now().timestamp()), "Finished", 0, 0))
		
		
	def show_downloads(self):
		downloads = self.other.get_data("downloads")
		x = self.btn_download.pos().x()
		y = self.btn_download.pos().y()
		x-= 330
		y+= 30
		point = QWidget(self).mapToGlobal(QPoint(x,y))
		print(f"x = {x} y = {y} Gpos = {point}")
		
		if downloads == []:
			self.statusBar().showMessage("No Downloads", 6000)
			return
		self.download_view.clearView()

		for download in downloads:
			id = download[0]
			icon = "./src/icon/file_white.svg"
			url = download[1]
			path = download[2]
			name = QFileInfo(path).fileName()
			time = download[3]
			state = download[4]
			total_size = download[5]
			down_size = download[6]
			print(f"Id: {id} name: {name} path: {path} state = {state} url: {url} time: {time}")
			layout = DownloadLayout(self)

			#layout.file_state.clicked.connect( lambda: self.act_download(id,states,widget,path)) #open_file_location
			self.download_view.addWidget(self.download_layout(id, icon, name, path, state, total_size, down_size))
		# Show Recycler
		self.download_view.view()

		# Action Download 
		self.download_action.setDefaultWidget(self.download_view)
		self.download_menu.addAction(self.download_action)
		# Show Downloads
		self.download_menu.exec(point)

	def download_layout(self , id:int, icon_p:str, name:str, path:str, states:str, t_size, d_size):
		# Layouts
		widget = QWidget()
		hbox = QHBoxLayout()
		midbox = QVBoxLayout()
		ps_box = QHBoxLayout()

		# Inner Objects
		file_icon = QLabel()
		file_name = QLabel()
		file_path = QLabel()
		file_size = QLabel()
		file_state = QPushButton()
		file_progress = QProgressBar()

		if d_size == 0:
			total_size = f"{t_size}Mb"
		else:
			total_size = f"{d_size}Mb/{t_size}Mb"

		widget.setObjectName("main")
		widget.setStyleSheet("""
			QWidget#main:hover{
			background-color: #616161;
			}
			QLabel{
			background-color: #212121;
			color: #ffffff;
			text-align: center;
			font-family: arial;
			}
			QPushButton{
			background-color: #212121;
			color: #ffffff;
			}
			QPushButton:hover{
			background-color: #818181;
			color: #ffffff;
			}
			

			""")

		file_icon.setPixmap(QPixmap(icon_p))
		file_icon.setFixedWidth(40)
		file_name.setText(name)
		file_progress.setMaximum(100)
		file_path.setText(path)
		file_size.setText(total_size)
		print("Lays")

		match states:
			case "Finished":
				state = "./src/icon/folder_white.svg"
			case "Progress":
				state = "./src/icon/pause_white.svg"
			case "Paused":
				state = "./src/icon/play_white.svg"
			case "Canceled":
				state = "./src/icon/refresh-cw_white.svg"

		file_state.setIcon(QIcon(state))
		file_state.setIconSize(QSize(20, 20))
		file_state.setFixedHeight(32)
		file_state.setFixedWidth(32)
		file_state.clicked.connect( lambda: act_download(id,states,widget,path)) #open_file_location

		midbox.addWidget(file_name)
		print("LA")
		if states == "Progress" :
			file_progress.setValue(50)
			file_progress.setStyleSheet("QProgressBar{ text-align : center; }")
			midbox.addWidget(file_progress)
		elif states == "Paused":
			file_progress.setValue(50)
			file_progress.setStyleSheet("QProgressBar{ background-color : red ;text-align : center; }QProgressBar:chunk{ background-color : orange;}")
			midbox.addWidget(file_progress)
		ps_box.addWidget(file_path)
		ps_box.addStretch()
		ps_box.addWidget(file_size)
		midbox.addLayout(ps_box)
		hbox.addWidget(file_icon)
		hbox.addLayout(midbox)
		hbox.addWidget(file_state)
		widget.setLayout(hbox)
		#widget.setStyleSheet("background-color: #919191")
		widget.resize(450, 70)
		return widget


	
	def act_download(self, id, state, obj, path):
		match state:
			case "Progress":
				self.statusBar().showMessage(f"Download File: {path} is Paused", 4000)
			case "Paused":
				self.statusBar().showMessage(f"Download File: {path} is Resumed", 4000)
			case "Canceled":
				self.statusBar().showMessage(f"Download File: {path} is Restarted", 4000)
			case "Finished":
				self.statusBar().showMessage(f"Opening File: {path}", 4000)


	def coping_text(self):
		text : str = ""

		# Url and Text Selected is empty
		if self.req_url.toString() == "" and self.browser_page.selectedText() == "":
			text = self.browser_page.url().toString()
		elif self.req_url.toString() == "" :
			text = self.browser_page.selectedText()
		else:
			text = self.req_url.toString()
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
								state STRING DEFAULT "Progress",
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
			self.db.commit()
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
			self.db.commit()
			return "Success"
		except Exception as e:
			return str(e)


	def delete_data(self,tabel_name: str,id) -> str:
		try:
			self.cursor.execute("DELETE FROM {} WHERE id = {}".format(tabel_name, id))
			self.db.commit()
			return "Success"
		except Exception as e:
			return str(e)

	def delete_tabel(self, tabel_name:str) -> str:
		try :
			self.cursor.execute("DROP TABLE IF EXISTS {} ".format(tabel_name))
			self.db.commit()
			return "Success"
		except Exception as e :
			return str(e)

if __name__ == "__main__":
	app = QApplication([])

	window = MainWindow()
	window.show()

	sys.exit(app.exec_())



