import sys
from typing import Optional
from PyQt5.QtWidgets import ( QWidget, QHBoxLayout, QVBoxLayout, QScrollArea)

class QRecyclerView(QScrollArea):
	"""
	
	  1. setLayoutSize(Width, Height, Spacing) to set the insert Layout width & height and spacing between layouts
	  2. addWidget( Widget, StyleSheet)
	  3. view() to Load all layout and view that

	"""

	def __init__(self, parant=None):
		super().__init__()
		self.parant = parant

		self.layoutWidth:int
		self.layoutHeight:int
		self.contentSize:int = 0
		self.spacing:int

		self.mainLayout = QVBoxLayout() # For Reactable Layout Width
		self.mainWidget = QWidget() # For custom style and size 
		self.vbox = QVBoxLayout() # For Add Layouts

		self.style:str

	def addWidget(self, widget:QWidget) -> None:
		widget.setFixedHeight(self.layoutHeight)
		widget.setMinimumWidth(self.layoutWidth)
		self.style = widget.styleSheet()
		self.vbox.addWidget(widget)
		self.contentSize += 1

	def setLayoutSize(self, width:int , height:int, spacing : Optional[int] = 0) -> None:
		self.layoutWidth = (width-15)
		self.layoutHeight = height
		self.spacing = spacing
		self.vbox.setContentsMargins(0,0,0,0)
		#self.mainWidget
		self.vbox.setSpacing(self.spacing)

	def view(self) -> None:
		self.mainWidget.setFixedHeight((self.layoutHeight + self.spacing )* self.contentSize)
		self.setMinimumWidth(self.layoutWidth+20)
		self.mainWidget.setLayout(self.vbox)
		self.mainWidget.setStyleSheet("background-color : #212121")#self.style)
		#self.mainLayout.addWidget(self.mainWidget)
		self.setWidget(self.mainWidget)
		#self.resize(self.parant.size())




