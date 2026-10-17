from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame

from components.pin_input import PinInputWidget
from utils.transactions import confirm_payment, confirm_transaction, confirm_deposit, confirm_withdraw

CONFIRMERS = {
    "send": confirm_transaction,
    "payment": confirm_payment,
    "cash_in": confirm_deposit,
    "cash_out": confirm_withdraw,
}


class ConfirmTransactionScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.kind = None
        self.details = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 10, 30, 30)

        title = QLabel("Confirm Transaction")
        title.setObjectName("titleLabel")
        layout.addWidget(title)

        self.card = QFrame()
        self.card.setProperty("class", "card")
        self.card_layout = QVBoxLayout(self.card)
        layout.addWidget(self.card)

        layout.addSpacing(10)
        layout.addWidget(QLabel("Enter your 4-digit PIN"))
        self.pin_input = PinInputWidget()
        layout.addWidget(self.pin_input)

        self.error_label = QLabel("")
        self.error_label.setObjectName("errorLabel")
        self.error_label.setWordWrap(True)
        layout.addWidget(self.error_label)

        layout.addStretch()

        buttons = QHBoxLayout()
        cancel = QPushButton("Cancel")
        cancel.setProperty("class", "secondary")
        cancel.clicked.connect(self.main_window.go_to_main_menu)
        verify = QPushButton("Verify")
        verify.setProperty("class", "primary")
        verify.clicked.connect(self.on_verify)
        buttons.addWidget(cancel)
        buttons.addWidget(verify)
        layout.addLayout(buttons)

    def load(self, kind, details, summary):
        self.kind, self.details = kind, details
        while self.card_layout.count():
            self.card_layout.takeAt(0).widget().deleteLater()
        for line in summary:
            self.card_layout.addWidget(QLabel(line))
        self.pin_input.clear()
        self.error_label.setText("")

    def on_verify(self):
        pin = self.pin_input.get_pin()
        if len(pin) != 4 or not self.main_window.verify_pin(pin):
            self.error_label.setText("Incorrect PIN. Try again.")
            self.pin_input.clear()
            return

        result = CONFIRMERS[self.kind](self.details)
        if result["Status"] == "Failed":
            self.error_label.setText(result["Message"])
            return
        self.main_window.go_to_receipt(result)