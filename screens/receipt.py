from datetime import datetime

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
from PyQt6.QtCore import Qt


class ReceiptScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 10, 30, 30)

        title = QLabel("Transaction Receipt")
        title.setObjectName("titleLabel")
        layout.addWidget(title)

        self.card = QFrame()
        self.card.setProperty("class", "card")
        self.card_layout = QVBoxLayout(self.card)
        layout.addWidget(self.card)

        layout.addStretch()

        done = QPushButton("Done")
        done.setProperty("class", "primary")
        done.clicked.connect(self.main_window.go_to_main_menu)
        layout.addWidget(done)

    def load(self, receipt):
        stamp = datetime.strptime(f"{receipt['Date']} {receipt['Time']}", "%Y-%m-%d %H:%M:%S")
        rows = [
            ("Name", receipt["Name"]),
            ("Amount", f"{receipt['Amount']:,.2f}"),
            ("Account Details", receipt["Account Details"]),
            ("Transaction No.", receipt["Transaction Number"]),
            ("Date", stamp.strftime("%m/%d/%Y")),
            ("Time", stamp.strftime("%I:%M %p")),
        ]
        while self.card_layout.count():
            item = self.card_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                while item.layout().count():
                    item.layout().takeAt(0).widget().deleteLater()

        for i, (label, value) in enumerate(rows):
            row = QHBoxLayout()
            left = QLabel(label)
            left.setObjectName("subtitleLabel")
            right = QLabel(value)
            right.setWordWrap(True)
            right.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            row.addWidget(left)
            row.addWidget(right, 1)
            self.card_layout.addLayout(row)
            if i < len(rows) - 1:
                line = QFrame()
                line.setFrameShape(QFrame.Shape.HLine)
                self.card_layout.addWidget(line)
