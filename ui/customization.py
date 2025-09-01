from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QSlider, 
                           QPushButton, QCheckBox, QFileDialog, QLabel, 
                           QSpinBox, QGroupBox, QGridLayout, QLineEdit, 
                           QFrame, QSizePolicy, QListWidget)
from PyQt5.QtCore import Qt, QTimer, QTime
from PyQt5.QtGui import QFont, QPixmap
import cv2
import numpy as np
from processing.image_processor import ImageProcessor

class CustomizationWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.image_processor = ImageProcessor()
        self.clock_timer = QTimer()
        self.clock_timer.timeout.connect(self.update_clock)
        
        self.setWindowTitle("FlipDigit Controls")
        self.setGeometry(1200, 100, 350, 700)  # Position to the right of main window
        
        # Make window stay on top and non-modal
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        
        self.setup_ui()
        self.apply_custom_styling()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Header
        header = QLabel("FlipDigit Controls")
        header.setObjectName("header")
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # Display Controls Group
        display_group = self.create_group("Display Controls")
        display_layout = QVBoxLayout(display_group)
        
        # Clear Display Button
        self.clear_btn = self.create_button("Clear Display", "#ef4444")
        self.clear_btn.clicked.connect(self.clear_display)
        display_layout.addWidget(self.clear_btn)

        # Show Grid Checkbox
        self.show_grid_cb = QCheckBox("Show Grid")
        self.show_grid_cb.setChecked(True)
        self.show_grid_cb.toggled.connect(self.toggle_grid)
        display_layout.addWidget(self.show_grid_cb)
        
        # Controls row
        controls_row = QHBoxLayout()
        self.invert_cb = QCheckBox("Invert")
        controls_row.addWidget(self.invert_cb)
        self.invert_cb.toggled.connect(self.toggle_invert)
        controls_row.addStretch()
        display_layout.addLayout(controls_row)
        
        # Cell Size
        size_layout = QHBoxLayout()
        size_layout.addWidget(QLabel("Size:"))
        self.cell_size_slider = QSlider(Qt.Horizontal)
        self.cell_size_slider.setRange(10, 40)
        self.cell_size_slider.setValue(20)
        self.cell_size_slider.valueChanged.connect(self.change_cell_size)
        size_layout.addWidget(self.cell_size_slider)
        display_layout.addLayout(size_layout)
        
        layout.addWidget(display_group)
        
        # Clock Controls Group
        clock_group = self.create_group("Clock")
        clock_layout = QVBoxLayout(clock_group)
        
        self.show_clock_cb = QCheckBox("Show Digital Clock")
        self.show_clock_cb.toggled.connect(self.toggle_clock)
        clock_layout.addWidget(self.show_clock_cb)
        
        layout.addWidget(clock_group)
        
        # Image Controls Group
        image_group = self.create_group("Image")
        image_layout = QVBoxLayout(image_group)
        
        self.upload_btn = self.create_button("Upload Image", "#3b82f6")
        self.upload_btn.clicked.connect(self.upload_image)
        image_layout.addWidget(self.upload_btn)
        
        layout.addWidget(image_group)
        
        # --- Todo List Controls Group ---
        todo_group = self.create_group("Todo List")
        todo_layout = QVBoxLayout(todo_group)

        self.todo_input = QLineEdit()
        self.todo_input.setPlaceholderText("Add a new todo…")
        todo_layout.addWidget(self.todo_input)

        self.todo_add_btn = self.create_button("Add Todo", "#10b981")
        self.todo_add_btn.clicked.connect(self.add_todo)
        todo_layout.addWidget(self.todo_add_btn)

        self.todo_list_widget = QListWidget()
        todo_layout.addWidget(self.todo_list_widget)

        self.todo_delete_btn = self.create_button("Delete Selected", "#ef4444")
        self.todo_delete_btn.clicked.connect(self.delete_selected)
        todo_layout.addWidget(self.todo_delete_btn)

        layout.addWidget(todo_group)

        
        # Animation Controls Group  
        anim_group = self.create_group("Animation")
        anim_layout = QVBoxLayout(anim_group)
        
        # Speed slider
        speed_layout = QHBoxLayout()
        speed_layout.addWidget(QLabel("Speed:"))
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setRange(500, 1000)
        self.speed_slider.setValue(500)
        self.speed_slider.valueChanged.connect(self.change_speed)
        speed_layout.addWidget(self.speed_slider)
        anim_layout.addLayout(speed_layout)
        
        # Sound checkbox
        self.sound_cb = QCheckBox("Enable Click Sounds")
        self.sound_cb.setChecked(True)
        self.sound_cb.toggled.connect(self.toggle_sound)
        anim_layout.addWidget(self.sound_cb)
        
        layout.addWidget(anim_group)
        
        # Add stretch to push everything to top
        layout.addStretch()
        
    def create_group(self, title):
        group = QGroupBox(title)
        group.setObjectName("group")
        return group
        
    def create_button(self, text, color):
        button = QPushButton(text)
        button.setObjectName("customButton")
        button.setStyleSheet(f"""
            QPushButton#customButton {{
                background-color: {color};
                border: none;
                color: white;
                padding: 8px 16px;
                font-size: 13px;
                font-weight: 500;
                border-radius: 6px;
                min-height: 30px;
            }}
            QPushButton#customButton:hover {{
                background-color: {self.adjust_color(color, -20)};
            }}
            QPushButton#customButton:pressed {{
                background-color: {self.adjust_color(color, -40)};
            }}
        """)
        return button
        
    def adjust_color(self, hex_color, adjustment):
        """Lighten or darken a hex color"""
        hex_color = hex_color.lstrip('#')
        rgb = [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]
        rgb = [max(0, min(255, c + adjustment)) for c in rgb]
        return '#{:02x}{:02x}{:02x}'.format(*rgb)
        
    def apply_custom_styling(self):
        self.setStyleSheet(f"""
            QWidget {{
                background-color: #0f172a;
                color: #94a3b8;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                font-size: 13px;
            }}
            
            QLabel#header {{
                color: #e2e8f0;
                font-size: 18px;
                font-weight: 600;
                padding: 10px;
                margin-bottom: 10px;
            }}
            
            QGroupBox {{
                color: #e2e8f0;
                font-weight: 500;
                border: 1px solid #334155;
                border-radius: 8px;
                margin-top: 8px;
                padding-top: 8px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 12px;
                padding: 2px 8px;
                background-color: #0f172a;
            }}
            
            QLineEdit {{
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 6px;
                padding: 8px;
                color: #e2e8f0;
            }}
            QLineEdit:focus {{
                border-color: #3b82f6;
            }}
            
            QCheckBox {{
                color: #94a3b8;
                spacing: 8px;
            }}
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                border-radius: 3px;
                border: 1px solid #334155;
                background-color: #1e293b;
            }}
            QCheckBox::indicator:checked {{
                background-color: #3b82f6;
                border-color: #3b82f6;
            }}
            
            QSlider::groove:horizontal {{
                border: 1px solid #334155;
                height: 6px;
                background: #1e293b;
                border-radius: 3px;
            }}
            QSlider::handle:horizontal {{
                background: #3b82f6;
                border: none;
                width: 18px;
                height: 18px;
                margin: -6px 0;
                border-radius: 9px;
            }}
            QSlider::sub-page:horizontal {{
                background: #3b82f6;
                border-radius: 3px;
            }}
        """)
        
    # All the existing methods remain the same
    def clear_display(self):
        if self.parent and hasattr(self.parent, 'flip_board'):
            self.parent.flip_board.clear_display()
            
    def toggle_invert(self, checked):
        if self.parent and hasattr(self.parent, 'flip_board'):
            self.parent.flip_board.set_invert_colors(checked)
            
    def change_cell_size(self, value):
        if self.parent and hasattr(self.parent, 'flip_board'):
            self.parent.flip_board.set_cell_size(value)
            
    def toggle_clock(self, checked):
        if checked:
            self.clock_timer.start(1000)
            self.update_clock()
        else:
            self.clock_timer.stop()
            
    def update_clock(self):
        current_time = QTime.currentTime().toString('hh:mm')
        if self.parent and hasattr(self.parent, 'flip_board'):
            self.parent.flip_board.set_large_text(current_time)  # Use large text for clock
            
    def upload_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Upload Image", 
            "", 
            "Image files (*.jpg *.jpeg *.png *.bmp *.gif)"
        )
        
        if file_path:
            processed_image = self.image_processor.process_image(file_path)
            if processed_image is not None and self.parent and hasattr(self.parent, 'flip_board'):
                self.parent.flip_board.set_image(processed_image)
                
    def display_text(self):
        text = self.text_input.text()
        if text and self.parent and hasattr(self.parent, 'flip_board'):
            self.parent.flip_board.set_text(text)
            
    def change_speed(self, value):
        if self.parent and hasattr(self.parent, 'flip_board'):
            self.parent.flip_board.set_animation_speed(value)
            
    def toggle_sound(self, checked):
        if self.parent and hasattr(self.parent, 'flip_board'):
            self.parent.flip_board.set_sound_enabled(checked)

    # Add this method:
    def toggle_grid(self, checked):
        if self.parent and hasattr(self.parent, 'flip_board'):
            self.parent.flip_board.set_show_grid(checked)
            
    def closeEvent(self, event):
        # Don't close the app when this window is closed
        self.hide()
        event.ignore()

    def add_todo(self):
        text = self.todo_input.text().strip()
        if text:
            self.todo_list_widget.addItem(text)
            self.todo_input.clear()
            self.update_flip_grid_from_todo()

    def delete_selected(self):
        for item in self.todo_list_widget.selectedItems():
            self.todo_list_widget.takeItem(self.todo_list_widget.row(item))
        self.update_flip_grid_from_todo()

    def update_flip_grid_from_todo(self):
        items = [self.todo_list_widget.item(i).text() for i in range(self.todo_list_widget.count())]
        if self.parent and hasattr(self.parent, "flip_board"):
            self.parent.flip_board.set_todo_list(items)