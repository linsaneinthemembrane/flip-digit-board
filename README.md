# FlipDigit Wallpaper

A Python desktop application that simulates authentic flip-digit panels with realistic animations and sound effects.

## Features

- **Authentic 7-Segment Display Simulation**: Realistic rendering of flip digit panels
- **Image Processing**: Upload images and convert them to flip digit art using OpenCV
- **Text Display**: Show custom text and digital clock in 7-segment style
- **Sound Effects**: Overlapping click sounds that play during segment changes
- **Customizable Animations**: Adjustable animation speed and random timing
- **Color Inversion**: Toggle between black/white display modes
- **Resizable Elements**: Experiment with different cell sizes for various detail levels
- **Modern UI**: Clean, dark-themed customization interface

## Installation

1. Clone or download this repository
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create an `assets` folder in the project root
4. Add your `click.mp3` sound file to the `assets` folder

## Usage

1. Run the application:
   ```bash
   python main.py
   ```
2. Access customization options through the **File > Customize** menu
3. Upload images, display text, show digital clock, or experiment with settings

## File Structure

```
flipdigit_wallpaper/
│
├── main.py                    # Main application entry point
├── assets/
│   └── click.mp3             # Sound effect file (user provided)
├── ui/
│   ├── __init__.py
│   └── customization.py      # Customization interface
├── panels/
│   ├── __init__.py
│   └── flip_digit_board.py   # Core flip digit display logic
├── processing/
│   ├── __init__.py
│   └── image_processor.py    # Image processing with OpenCV
├── requirements.txt          # Dependencies
└── README.md                # This file
```

## Controls

- **Clear Display**: Remove all content from the board
- **Invert Colors**: Toggle between black-on-white and white-on-black
- **Cell Size**: Adjust the size of individual digit segments
- **Show Digital Clock**: Display current time in large 7-segment format
- **Upload Image**: Convert images to flip digit art
- **Display Text**: Show custom text messages
- **Animation Speed**: Control how fast segments animate
- **Enable Click Sounds**: Toggle realistic flip sound effects

## Requirements

- Python 3.7+
- PyQt5
- OpenCV
- Pygame
- NumPy
- Pillow

## Notes

- The application is designed for Windows
- Sound effects require an MP3 file named `click.mp3` in the `assets` folder
- Images are automatically resized and converted to black/white for optimal display
- Multiple sound effects can overlap for realistic clicking during rapid changes