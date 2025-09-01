import random
import time
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import pygame

class FlipDigitBoard(QWidget):
    def __init__(self, parent=None, sound=None, cols=40, rows=20):
        super().__init__(parent)
        self.cols = cols
        self.rows = rows
        self.cell_size = 32  # Adjust for node size
        self.sound = sound
        self.sound_enabled = True
        self.invert_colors = False
        self.inverted_state = False
        self.animation_speed = 5
        self.show_grid = True
        # Example patterns, fill in from e.g. Wikipedia: https://en.wikipedia.org/wiki/Fourteen-segment_display#Character_encoding
        """    ----------a----------
               |\        |        /|
               | \       |       / |
               |  \      |      /  |
               |   h     l     i   |
               f    \    |    /    b
               |     \   |   /     |
               |      \  |  /      |
               |       \ | /       |
               |---g1----|----g2---|
               |       / | \       |
               |      /  |  \      |
               |     /   |   \     |               
               e    /    |    \    c
               |   j     m     k   |
               |  /      |      \  |
               | /       |       \ |
               |/        |        \|
               ----------d----------
               """
        
        self.fourteen_seg_digits = {
            ' ': [0,0,0,0,0,0,0,0,0,0,0,0,0,0],

            # Digits
            '0': [1,1,1,1,1,1,0,0,0,0,0,0,0,0],
            '1': [0,1,1,0,0,0,0,0,0,1,0,0,0,0],
            '2': [1,1,0,1,1,0,1,1,0,0,0,0,0,0],
            '3': [1,1,1,1,0,0,0,1,0,0,0,0,0,0],
            '4': [0,1,1,0,0,1,1,1,0,0,0,0,0,0],
            '5': [1,0,1,1,0,1,1,1,0,0,0,0,0,0],
            '6': [1,0,1,1,1,1,1,1,0,0,0,0,0,0],
            '7': [1,1,1,0,0,0,0,0,0,0,0,0,0,0],
            '8': [1,1,1,1,1,1,1,1,0,0,0,0,0,0],
            '9': [1,1,1,1,0,1,1,1,0,0,0,0,0,0],

            # Letters
            'A': [1,1,1,0,1,1,1,1,0,0,0,0,0,0],
            'B': [1,1,1,1,1,1,1,1,0,0,0,0,0,0],
            'C': [1,0,0,1,1,1,0,0,0,0,0,0,0,0],
            'D': [0,0,0,0,1,1,0,0,1,0,1,0,0,0],
            'E': [1,0,0,1,1,1,1,1,0,0,0,0,0,0],
            'F': [1,0,0,0,1,1,1,1,0,0,0,0,0,0],
            'G': [1,0,1,1,1,1,0,1,0,0,0,0,0,0],
            'H': [0,1,1,0,1,1,1,1,0,0,0,0,0,0],
            'I': [1,0,0,1,0,0,0,0,0,0,0,0,1,1],
            'J': [1,1,1,1,1,0,0,0,0,0,0,0,0,0],
            'K': [0,0,0,0,0,0,0,0,0,1,0,1,1,1],
            'L': [0,0,0,1,1,1,0,0,0,0,0,0,0,0],
            'M': [0,1,1,0,1,1,0,0,1,1,0,0,0,0],
            'N': [0,1,1,0,1,1,0,0,1,0,0,1,0,0],
            'O': [1,1,1,1,1,1,0,0,0,0,0,0,0,0],
            'P': [1,1,0,0,1,1,1,1,0,0,0,0,0,0],
            'Q': [1,1,1,1,1,1,0,0,0,0,0,1,0,0],
            'R': [1,1,0,0,1,1,1,1,0,0,0,1,0,0],
            'S': [1,0,1,1,0,1,1,1,0,0,0,0,0,0],
            'T': [1,0,0,0,0,0,0,0,0,0,0,0,1,1],
            'U': [0,1,1,1,1,1,0,0,0,0,0,0,0,0],
            'V': [0,1,1,1,1,1,0,0,0,0,0,0,0,0],
            'W': [0,1,1,1,1,1,0,0,0,0,0,0,0,1], # i stopped here
            'X': [0,0,0,0,0,0,0,0,1,1,1,1,0,0],
            'Y': [0,0,0,0,0,0,0,0,1,1,0,0,0,1],
            'Z': [1,0,0,1,0,0,0,0,0,1,1,0,0,0],

            # Symbols
            '-': [0,0,0,0,0,0,1,1,0,0,0,0,0,0],
            '_': [0,0,0,1,0,0,0,0,0,0,0,0,0,0],
            '.': [0,0,0,0,0,0,0,0,0,0,0,1,0,0],  # using k as dot
            '/': [0,0,0,0,0,0,0,0,0,1,1,0,0,0],
            ',': [0,0,0,0,0,0,0,0,0,0,1,1,0,0],
            ':': [0,0,0,0,0,0,0,0,1,0,1,0,0,0],
            "'": [0,0,0,0,0,0,0,0,1,0,0,0,0,0],
        }

        self.board_state = np.zeros((self.rows, self.cols, 14), dtype=int)
        self.target_state = np.zeros((self.rows, self.cols, 14), dtype=int)
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.animate_step)
        self.animation_step_count = 0
        self.total_changes_needed = 0
        self.setMinimumSize(self.cols * self.cell_size, self.rows * self.cell_size)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        bg_color = QColor(15, 23, 42)
        active_color = QColor(0, 255, 100)
        grid_color = QColor(30, 41, 59)
        painter.fillRect(self.rect(), bg_color)
        for row in range(self.rows):
            for col in range(self.cols):
                self.draw_fourteen_segment(
                    painter,
                    col,
                    row,
                    self.board_state[row, col],
                    active_color,
                    grid_color
                )

    def get_fourteen_segment_shapes(self, col, row, cell_size):
        x = col * cell_size
        y = row * cell_size
        w = cell_size
        h = cell_size
        mh_pad = w // 12
        mid_x = x + w // 2
        mid_y = y + h // 2

        th = max(2, w // 10)  # thickness

        return [
            # a (top horizontal)
            [(x+th, y), (x+w-th, y), (x+w-th, y+th), (x+th, y+th)],

            # b (upper right vertical)
            [(x+w-th, y+th), (x+w, y+th), (x+w, y+h//2-th//2), (x+w-th, y+h//2-th//2)],

            # c (lower right vertical)
            [(x+w-th, y+h//2+th//2), (x+w, y+h//2+th//2), (x+w, y+h-th), (x+w-th, y+h-th)],

            # d (bottom horizontal)
            [(x+th, y+h-th), (x+w-th, y+h-th), (x+w-th, y+h), (x+th, y+h)],

            # e (lower left vertical)
            [(x, y+h//2+th//2), (x+th, y+h//2+th//2), (x+th, y+h-th), (x, y+h-th)],

            # f (upper left vertical)
            [(x, y+th), (x+th, y+th), (x+th, y+h//2-th//2), (x, y+h//2-th//2)],

            # g1 (middle horizontal left)
            [(x+th+mh_pad, y+h//2-th//2), (x+w//2-mh_pad, y+h//2-th//2),
            (x+w//2-mh_pad, y+h//2+th//2), (x+th+mh_pad, y+h//2+th//2)],

            # g2 (middle horizontal right)
            [(x+w//2+mh_pad, y+h//2-th//2), (x+w-th-mh_pad, y+h//2-th//2),
            (x+w-th-mh_pad, y+h//2+th//2), (x+w//2+mh_pad, y+h//2+th//2)],


            # h (upper left diagonal)
            [(x+th, y+th), (x+2*th, y+2*th),
            (x+w//2-2*th, y+h//2-2*th), (x+w//2-th, y+h//2-th)],

            # i (upper right diagonal)
            [(x+w-th, y+th), (x+w-2*th, y+2*th),
            (x+w//2+th, y+h//2-th), (x+w//2+2*th, y+h//2-2*th)],

            # j (lower left diagonal)
            [(x+th, y+h-th), (x+2*th, y+h-2*th),
            (x+w//2-2*th, y+h//2+2*th), (x+w//2-th, y+h//2+th)],

            # k (lower right diagonal)
            [(x+w-th, y+h-th), (x+w-2*th, y+h-2*th),
            (x+w//2+2*th, y+h//2+2*th), (x+w//2+th, y+h//2+th)],

            # l (center vertical top)
            [(mid_x - th//2, y + th), (mid_x + th//2, y + th),
            (mid_x + th//2, mid_y - 1), (mid_x - th//2, mid_y - 1)],

            # m (center vertical bottom)
            [(mid_x - th//2, mid_y + 1), (mid_x + th//2, mid_y + 1),
            (mid_x + th//2, y + h - th), (mid_x - th//2, y + h - th)]
        ]




    def draw_fourteen_segment(self, painter, col, row, segments, active_color, grid_color):
        shapes = self.get_fourteen_segment_shapes(col, row, self.cell_size)
        for i, coords in enumerate(shapes):
            points = [QPoint(x, y) for x, y in coords]
            if segments[i]:
                painter.setPen(QPen(active_color, 2))
                painter.setBrush(QBrush(active_color))
                painter.drawPolygon(points)
            else:
                if self.show_grid:
                    painter.setPen(QPen(grid_color, 1))
                    painter.setBrush(Qt.NoBrush)
                    painter.drawPolygon(points)

    
    def bitmap_to_segments(self, bitmap):
        """Convert a bitmap to 7-segment patterns using intelligent analysis"""
        result = np.zeros((bitmap.shape[0], bitmap.shape[1], 14), dtype=int)
        
        for row in range(bitmap.shape[0]):
            for col in range(bitmap.shape[1]):
                if bitmap[row, col]:  # If this pixel should be "on"
                    # Analyze surrounding pixels to determine which segments to activate
                    segments = self.analyze_pixel_for_segments(bitmap, row, col)
                    result[row, col] = segments
                    
        return result
    
    def analyze_pixel_for_segments(self, bitmap, row, col):
        """Analyze a pixel's neighborhood to determine which 14-segments to activate."""
        segments = [0] * 14  # A–M

        rows, cols = bitmap.shape

        # Helper: check if pixel is set and inside bounds
        def on(r, c):
            return 0 <= r < rows and 0 <= c < cols and bitmap[r, c]

        # --- Horizontal segments ---
        if on(row-1, col):  # something above
            segments[0] = 1  # A
        if on(row+1, col):  # something below
            segments[3] = 1  # D
        if on(row, col) and (on(row-1, col) or on(row+1, col)):
            segments[6] = 1  # G1
            segments[7] = 1  # G2

        # --- Vertical segments ---
        if on(row, col+1):
            segments[1] = 1  # B
            segments[2] = 1  # C
        if on(row, col-1):
            segments[4] = 1  # E
            segments[5] = 1  # F

        # --- Diagonals ---
        if on(row-1, col-1):
            segments[8] = 1  # H (top-left diag)
        if on(row-1, col+1):
            segments[9] = 1  # I (top-right diag)
        if on(row+1, col-1):
            segments[10] = 1  # J (bottom-left diag)
        if on(row+1, col+1):
            segments[11] = 1  # K (bottom-right diag)

        # --- Center verticals ---
        if on(row, col-1) and on(row, col):  # pixel + left neighbor
            segments[12] = 1  # L
        if on(row, col+1) and on(row, col):  # pixel + right neighbor
            segments[13] = 1  # M

        # --- Fallback: isolated pixel → show "all on"
        neighborhood = sum(on(row+dr, col+dc) for dr in [-1,0,1] for dc in [-1,0,1])
        if neighborhood == 1:
            segments = [1] * 14

        return segments

    
    def text_to_bitmap(self, text, target_width=None, target_height=None):
        """Convert text to bitmap array using PIL font rendering"""
        try:
            # Calculate optimal dimensions
            if target_width is None:
                target_width = min(self.cols - 4, len(text) * 8)
            if target_height is None:
                target_height = min(self.rows - 4, 16)
            
            # Create PIL image
            img = Image.new('L', (target_width * 6, target_height * 6), 255)
            draw = ImageDraw.Draw(img)
            
            # Try to get a good monospace font
            font_size = target_height * 4
            try:
                # Try different fonts
                for font_name in ['consolas.ttf', 'arial.ttf', 'DejaVuSansMono.ttf']:
                    try:
                        font = ImageFont.truetype(font_name, font_size)
                        break
                    except:
                        continue
                else:
                    font = ImageFont.load_default()
            except:
                font = ImageFont.load_default()
            
            # Get text dimensions and center it
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            x = (img.width - text_width) // 2
            y = (img.height - text_height) // 2
            
            # Draw text
            draw.text((x, y), text, font=font, fill=0)
            
            # Resize to target
            img = img.resize((target_width, target_height), Image.LANCZOS)
            img_array = np.array(img)
            
            # Threshold to binary
            binary = (img_array < 128).astype(int)
            
            return binary
            
        except Exception as e:
            print(f"Error in text_to_bitmap: {e}")
            return np.zeros((target_height or 12, target_width or len(text) * 6), dtype=int)
    
    def set_large_text(self, text, animate=True):
        """Display large text using automatic font rendering with proper 14-segment mapping"""
        self.target_state.fill(0)

        # Calculate size
        available_width = self.cols - 4
        available_height = self.rows - 4

        # Generate bitmap
        bitmap = self.text_to_bitmap(text, available_width, available_height)

        # Convert bitmap to 14-segment patterns
        segments = self.bitmap_to_segments(bitmap)

        # Center on display
        start_row = (self.rows - segments.shape[0]) // 2
        start_col = (self.cols - segments.shape[1]) // 2

        # Apply to target state
        for row_idx in range(segments.shape[0]):
            for col_idx in range(segments.shape[1]):
                target_row = start_row + row_idx
                target_col = start_col + col_idx
                if (0 <= target_row < self.rows and 0 <= target_col < self.cols):
                    self.target_state[target_row, target_col] = segments[row_idx, col_idx]

        if self.inverted_state:
            self.target_state = 1 - self.target_state  # <-- ENSURE INVERSION IS PERSISTENT

        if animate:
            self.start_animation()
        else:
            self.board_state = self.target_state.copy()
            self.update()

    def set_todo_list(self, items, animate=True):
        # Fill the grid with spaces, then place one todo item per row, left-aligned
        self.target_state.fill(0)
        for row, item in enumerate(items):
            if row >= self.rows:
                break
            item = item.upper() 
            for col, char in enumerate(item):
                if col >= self.cols:
                    break
                segs = self.fourteen_seg_digits.get(char, [0]*14)
                self.target_state[row, col] = segs
        if self.inverted_state:
            self.target_state = 1 - self.target_state
        if animate:
            self.start_animation()
        else:
            self.board_state = self.target_state.copy()
            self.update()

        
    def set_text(self, text, animate=True, gap=20):
        """
        Each cell is one 14-segment node; text left-justified, one char per cell, with gap columns in between.
        """
        self.target_state.fill(0)
        text = text.upper()
        col = 0
        for ch in text:
            if col >= self.cols:
                break
            segs = self.fourteen_seg_digits.get(ch, [0]*14)
            # Place character in row 0 (or whichever row you prefer)
            self.target_state[0, col] = segs
            col += 1 + gap  # move to next character position, skipping 'gap' columns
        if self.inverted_state:
            self.target_state = 1 - self.target_state
        if animate:
            self.start_animation()
        else:
            self.board_state = self.target_state.copy()
            self.update()

    def set_image(self, image_array, animate=True):
        """Convert image to flip digit representation with proper 14-segment mapping"""
        self.target_state.fill(0)

        # Resize image to fit board
        img = Image.fromarray(image_array)
        img = img.resize((self.cols, self.rows), Image.LANCZOS)
        img_array = np.array(img)

        # Convert to binary
        if len(img_array.shape) == 3:
            img_array = np.mean(img_array, axis=2)

        threshold = 128
        binary = (img_array < threshold).astype(int)

        # Convert to 14-segment patterns
        segments = self.bitmap_to_segments(binary)
        self.target_state = segments

        if self.inverted_state:
            self.target_state = 1 - self.target_state  # <-- ENSURE INVERSION IS PERSISTENT

        if animate:
            self.start_animation()
        else:
            self.board_state = self.target_state.copy()
            self.update()

    
    def set_show_grid(self, show):
        """Toggle visibility of background grid"""
        self.show_grid = show
        self.update()
        
    
    def start_animation(self):
        """Start animated transition to target state"""
        self.total_changes_needed = np.sum(self.board_state != self.target_state)
        self.animation_step_count = 0
        self.animation_timer.start(max(5, self.animation_speed))
        
    def animate_step(self):
        """Perform one step of animation"""
        diff = self.board_state != self.target_state 

        rows, cols, segs = np.where(diff)
        differences = list(zip(rows, cols, segs))
                            
        if not differences:
            self.animation_timer.stop()
            return
            
        # Fast animation
        remaining = len(differences)
        base_changes = max(1, remaining // 50)
        progress = 1.0 - (remaining / max(1, self.total_changes_needed))
        acceleration = 1 + progress * 3
        num_changes = min(remaining, max(base_changes, int(base_changes * acceleration)))
        
        if self.animation_speed <= 20:
            num_changes = max(num_changes, remaining // 20)
        
        selected_changes = random.sample(differences, num_changes)
        changes_count = 0
        
        for row, col, seg in selected_changes:
            self.board_state[row, col, seg] = self.target_state[row, col, seg]
            changes_count += 1
            
        # Sound effects
        if changes_count > 0 and self.sound_enabled and self.sound:
            sound_count = min(changes_count // 3, 8)
            for i in range(sound_count):
                channel = pygame.mixer.find_channel()
                if channel:
                    volume = random.uniform(0.7, 1.0)
                    self.sound.set_volume(volume)
                    channel.play(self.sound)
                    
        self.update()
        
    def clear_display(self):
        """Clear the entire display"""
        self.target_state.fill(0)
        if self.inverted_state:
            self.target_state = 1 - self.target_state  # <-- ENSURE INVERSION IS PERSISTENT
        self.start_animation()

        
    def set_sound_enabled(self, enabled):
        """Toggle sound effects"""
        self.sound_enabled = enabled
        
    def set_invert_colors(self, invert):
        # If switching ON, flip board_state/target_state
        # If switching OFF, just update the flag (future updates are not inverted)
        if invert and not self.inverted_state:
            self.board_state = 1 - self.board_state
            self.target_state = 1 - self.target_state
        elif not invert and self.inverted_state:
            self.board_state = 1 - self.board_state
            self.target_state = 1 - self.target_state
        self.inverted_state = invert
        self.update()

        
    def set_animation_speed(self, speed):
        """Set animation speed"""
        self.animation_speed = max(5, 510 - speed)
        
    def set_cell_size(self, size):
        """Change the size of individual cells"""
        self.cell_size = max(10, size)
        self.setMinimumSize(self.cols * self.cell_size, self.rows * self.cell_size)
        self.update()
