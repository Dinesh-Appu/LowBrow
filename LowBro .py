from PyQt5.QtWidgets import ( QApplication, QMainWindow, QFileDialog,
							QWidget, QHBoxLayout, QVBoxLayout,
							QLabel, QLineEdit, QPushButton
							)
from PyQt5.QtCore import Qt, QUrl, QSize, QDir, QFileInfo 
from PyQt5.QtGui import QKeySequence, QIcon, QColor
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings, QWebEngineProfile, QWebEngineDownloadItem

import PyQt5.QtCore as QtCore

# Other Lib
import sys 
import sqlite3 
import datetime


"""    Todo:
			1.file download
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
		self.ask_download = True
		self.file_style_main = "./src/styles/style_sheet_main.qcc"
		self.file_database = "./src/database.db"
		self.default_path = "C:/Users/Welcome/Downloads/"
		self.current_path = "C:/Users/Welcome/Downloads/"
		self.default_page : str = "https://feathericons.com/?query=arrow"
		self.default_backgroud_color = "#282828"


		self.setWindowTitle("LowBrow")
		self.resize(900, 600)
		self.style_sheet()

		#"https://www.youtube.com/watch?v=AiD6SOOBKZI"
		#"https://www.youtube.com/watch?v=IZHGcU0U_W0"
		#"file:///G:/Python/Files/PyQt5/test/temp/roadmap_python.mp4"
		#"www.google.com"
		#"file:///G:/Python/Files/PyQt5/test/temp/web/New%20Tab.htm"

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

		self.edit_url = QLineEdit()

		self.hbox_top = QHBoxLayout()
		self.vbox = QVBoxLayout()

		self.browser = QWebEngineView()

		self.settings_browser = QWebEngineSettings.globalSettings()
		self.other = Other(self)
		self.history = self.other.get_data("history")
		# Main UI Setup
		self.initUI()


	def initUI(self):
		self.main_centeral_widget = QWidget()
		self.setCentralWidget(self.main_centeral_widget)

		
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
		self.btn_download.clicked.connect(self.new_window)

		self.browser.urlChanged.connect(self.url_changed)
		self.browser.loadStarted.connect(self.url_loading)
		self.browser.loadFinished.connect(self.url_loaded)
		#self.browser.createWindow.connect(self.new_tab)

		self.browser.page().fullScreenRequested.connect(self.full_screen_req)
		QWebEngineProfile.defaultProfile().downloadRequested.connect(self.download_file)


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

	def main_icon(self):
		print("\nIcon Url >>>>",self.browser.page().iconUrl())

	def update_window(self):
		self.setWindowTitle(self.browser.page().title())
		self.setWindowIcon(self.browser.page().icon())
		print("WIndow icon >>>>>",self.browser.page().iconUrl())

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
		self.loading = True
		self.btn_refresh.setIcon(QIcon("./src/icon/cancel_x_white.svg"))

	def url_loaded(self):
		self.loading = False
		self.btn_refresh.setIcon(QIcon("./src/icon/refresh-cw_white.svg"))
		self.update_window()

		print(f"\n Title >>>> {self.browser.page().title()} \n")
		
		print(f"Url Loaded {self.browser.page().icon()}")
		self.browser_icon.setIcon(self.browser.page().icon())
		print("###### back Color -----> ",self.browser.page().backgroundColor())
		self.browser.page().setBackgroundColor(QColor(self.default_backgroud_color))

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
		book = self.other.get_data("bookmark")
		print("get bookmark >>>>> ", book)

	
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
		if path == None:
			return

		# Set Download File Details
		downlaod.setDownloadFileName(QFileInfo(path).fileName())
		self.current_path = QFileInfo(path).path()+"/"
		downlaod.setDownloadDirectory(QFileInfo(path).path())

		print(f"\n filesize = {downlaod.totalBytes()} default_path = {self.current_path} filetype = {downlaod.type()}\n")
		# Start Downloading File
		downlaod.accept()
		# Show Download Progress Signal
		downlaod.downloadProgress.connect(self.downlaod_progress)
        

	def downlaod_progress(self, recv_byte, total_byte):
		
		print(f"n Download Progress {int(recv_byte/1024)} Kb/{int(total_byte/1024)} Kb")
		"""# bytes to Mb
		if int(total_byte/1024) > 1024:
			print("is Mb") 
			recv_byte = int((recv_byte/1024)/1024)
			total_byte= int((total_byte/1024)/1024)
		else:
			print("is Kb")
			recv_byte = int(recv_byte/1024)
			total_byte= int(total_byte/1024) """
		

        
	def new_window(self):
		new = MainWindow()
		new.browser.setUrl(self.browser.url())
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


class Other():

	def __init__(self,main:MainWindow):
		super().__init__()
		


		self.db = sqlite3.connect(main.file_database)

		self.cursor = self.db.cursor()

		self.cursor.execute(""" CREATE TABLE IF NOT EXISTS history (
								id INTEGER PRIMARY KEY AUTOINCREMENT, 
								url STRING NOT NULL, 
								time_ids TIMESTAMP NOT NULL)
		""")

		self.cursor.execute(""" CREATE TABLE IF NOT EXISTS bookmark (
								id INTEGER PRIMARY KEY AUTOINCREMENT,
								url STRING NOT NULL UNIQUE
								) """)


		#self.cursor.execute(""" DROP TABLE  history""")
		#self.db.commit()


	def add_history(self, tabel_name, url : str , time ) -> str :
		try:
			self.cursor.execute(""" INSERT INTO {} (url, time_ids) VALUES ("{}", {}) """.format(tabel_name, url, time))
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



