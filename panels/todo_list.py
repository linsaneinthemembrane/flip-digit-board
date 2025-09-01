from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QListWidget, QPushButton, QListWidgetItem

class ToDoList(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # ...
        self.list_widget = QListWidget(self)
        self.input = QLineEdit(self)
        self.add_button = QPushButton("Add")
        self.delete_button = QPushButton("Delete Selected")
        # ... layout, etc ...
        self.add_button.clicked.connect(self.add_todo)
        self.delete_button.clicked.connect(self.delete_selected)
        self.list_widget.itemDoubleClicked.connect(self.delete_selected)
        # add these widgets to your layout

    def add_todo(self):
        text = self.input.text().strip()
        if text:
            self.list_widget.addItem(QListWidgetItem(text))
            self.input.clear()
            self.update_flip_grid()

    def delete_selected(self):
        for item in self.list_widget.selectedItems():
            self.list_widget.takeItem(self.list_widget.row(item))
        self.update_flip_grid()

    def update_flip_grid(self):
        # Make sure your parent has a reference to the FlipDigitBoard
        items = [self.list_widget.item(i).text() for i in range(self.list_widget.count())]
        if hasattr(self.parent(), "flip_board"):
            self.parent().flip_board.set_todo_list(items)
