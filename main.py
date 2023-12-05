import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QFileDialog, QDateEdit, QLabel
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import pandas as pd

class TemperatureGraphApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Temperature Graph App')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        # Title label
        title_label = QLabel("Temperature Visualization", self)
        title_font = QFont("Arial", 16, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(title_label)

        # Date range selection
        date_range_label = QLabel("Select Date Range:", self)
        date_range_label.setFont(QFont("Arial", 12))
        self.layout.addWidget(date_range_label)

        self.start_date_edit = QDateEdit(self)
        self.end_date_edit = QDateEdit(self)
        self.start_date_edit.setCalendarPopup(True)
        self.end_date_edit.setCalendarPopup(True)

        self.layout.addWidget(self.start_date_edit)
        self.layout.addWidget(self.end_date_edit)

        # Graph display area
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        self.layout.addWidget(self.canvas)

        # Load data button
        self.load_data_button = QPushButton('Load Data', self)
        self.load_data_button.clicked.connect(self.load_data)
        self.layout.addWidget(self.load_data_button)

        # Set styles
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
            }
            QLabel {
                color: #333;
            }
            QDateEdit {
                background-color: #fff;
                border: 1px solid #aaa;
                padding: 5px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: #fff;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        # DataFrame variable to store loaded data
        self.df = None

        # Connect dateChanged signals to update graph when date selections change
        self.start_date_edit.dateChanged.connect(self.update_graph)
        self.end_date_edit.dateChanged.connect(self.update_graph)

    def load_data(self):
        file_dialog = QFileDialog(self)
        csv_file_path, _ = file_dialog.getOpenFileName(self, 'Open CSV File', '', 'CSV Files (*.csv)')

        if csv_file_path:
            # Load CSV data into a pandas DataFrame with date format specification
            self.df = pd.read_csv(csv_file_path, parse_dates=['Date'], date_parser=lambda x: pd.to_datetime(x, format='%Y-%m-%d'))

            # Set the minimum and maximum dates for the date range selection
            min_date = self.df['Date'].min().to_pydatetime().date()
            max_date = self.df['Date'].max().to_pydatetime().date()
            self.start_date_edit.setDate(min_date)
            self.end_date_edit.setDate(max_date)

            # Plot the initial data
            self.update_graph()

    def update_graph(self):
        # Check if DataFrame is loaded
        if self.df is not None:
            # Reload and plot data based on selected date range
            start_date = pd.Timestamp(self.start_date_edit.date().toPyDate())
            end_date = pd.Timestamp(self.end_date_edit.date().toPyDate())
            filtered_df = self.df[(self.df['Date'] >= start_date) & (self.df['Date'] <= end_date)]

            # Plot the data
            self.ax.clear()
            self.ax.plot(filtered_df['Date'], filtered_df['Temperature'], marker='o', linestyle='-', color='#3498db')
            self.ax.set_title('Temperature Over Time')
            self.ax.set_xlabel('Date')
            self.ax.set_ylabel('Temperature (°C)')
            self.ax.grid(True, linestyle='--', alpha=0.7)

            # Draw the plot on the canvas
            self.canvas.draw()

sys._excepthook = sys.excepthook
def exception_hook(exctype, value, traceback):
    print(exctype, value, traceback)
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)
sys.excepthook = exception_hook

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Use Fusion style for a modern look
    app.setWindowIcon(QIcon('icon.png'))  # Replace 'icon.png' with your icon file
    main_window = TemperatureGraphApp()
    main_window.show()
    sys.exit(app.exec_())
