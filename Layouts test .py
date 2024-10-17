import sys
from PyQt5.QtWidgets import ( 
			QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
			QLabel, QPushButton, QProgressBar)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize


class MainWindow(QMainWindow):

	def __init__(self):
		super().__init__()

		self.resize(500, 500)
		self.setStyleSheet(open("./src/styles/style_sheet_main.qcc", 'r').read())

		self.label = QLabel("PyQt5 Custom RecyclerView .py")
		self.main_box = QVBoxLayout()

		self.names : list(str) = ['Dinesh', 'Appu', 'Sathya', "Aalife", "Kishor", "Siva", "Vasanth", "Vasantha", "Karthi", "Mani"] 
		self.initUI()


	def initUI(self):
		central_widget = QWidget()
		self.setCentralWidget(central_widget)

		for i in range(1,4):
			self.download_layout( i ,"./src/icon/file_white.svg", "file_white.svg", "G:/Github/projects/LowBrow/src/icon/", "Progress")

		central_widget.setLayout(self.main_box)

	def download_layout(self, id:int, icon_p:str, name:str, path:str, states:str): # 
			
		widget = QWidget(self)
		hbox = QHBoxLayout()
		center = QVBoxLayout()
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

		file_icon = QLabel()
		file_name = QLabel()
		file_path = QLabel()
		file_state = QPushButton()
		file_progress = QProgressBar()

		file_icon.setPixmap(QPixmap(icon_p))
		file_icon.setFixedWidth(40)
		file_name.setText(name)
		file_progress.setMaximum(100)
		file_path.setText(path)

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
		file_state.setIconSize(QSize(29, 29))
		file_state.setFixedHeight(32)
		file_state.setFixedWidth(32)
		file_state.clicked.connect( lambda: self.open_file(id,states,widget))

		center.addWidget(file_name)
		if states == "Progress" :
			file_progress.setValue(50)
			file_progress.setStyleSheet("QProgressBar{ text-align : center; }")
			center.addWidget(file_progress)
		elif states == "Paused":
			file_progress.setValue(50)
			file_progress.setStyleSheet("QProgressBar{ background-color : red ;text-align : center; }QProgressBar:chunk{ background-color : orange;}")
			center.addWidget(file_progress)
		center.addWidget(file_path)
		hbox.addWidget(file_icon)
		hbox.addLayout(center)
		hbox.addWidget(file_state)
		widget.setLayout(hbox)
		#widget.setStyleSheet("background-color: #919191")
		widget.resize(450, 70)
		self.main_box.addWidget(widget)

	def open_file(self, id, state, main):
		print(f" Id = {id} State = {state}")
		print(main)


if __name__ == '__main__':
	app = QApplication([])

	window = MainWindow()
	window.show()

	sys.exit(app.exec_())

