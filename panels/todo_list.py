from PyQt5.QtWidgets import Qt, QWidget, QVBoxLayout, QLineEdit, QListWidget, QListWidgetItem, QPushButton

class TodoList(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.input = QLineEdit(self)
        self.input.setPlaceholderText("Add a new todo…")
        self.list_widget = QListWidget(self)
        self.add_button = QPushButton("Add")
        layout.addWidget(self.input)
        layout.addWidget(self.add_button)
        layout.addWidget(self.list_widget)
        self.add_button.clicked.connect(self.add_todo)
        self.list_widget.itemDoubleClicked.connect(self.delete_todo)
        self.setLayout(layout)

    def add_todo(self):
        text = self.input.text().strip()
        if text:
            self.list_widget.addItem(QListWidgetItem(text))
            self.input.clear()

    def delete_selected(self):
        for item in self.list_widget.selectedItems():
            self.list_widget.takeItem(self.list_widget.row(item))
        self.update_flip_grid()

    def update_flip_grid(self):
        # This syncs the visible grid with the to-do list items
        items = [self.list_widget.item(i).text() for i in range(self.list_widget.count())]
        if hasattr(self.parent(), "flip_board"):
            self.parent().flip_board.set_todo_list(items)
