from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton


class TransactionFormScreen(QWidget):
    """Base for Send, Payment, Cash In and Cash Out (same layout as the wireframes).

    Subclasses set: kind, title, action_text, fields = [(key, label, placeholder)]
    and implement build_details(values, amount) -> (details, summary).
    """
    kind = ""
    title = ""
    action_text = "Continue"
    fields = []

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.inputs = {}

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 10, 30, 30)
        layout.setSpacing(6)

        title = QLabel(self.title)
        title.setObjectName("titleLabel")
        layout.addWidget(title)

        for key, label, placeholder in self.fields:
            layout.addWidget(QLabel(label))
            widget = self.create_input(key, placeholder)
            self.inputs[key] = widget
            layout.addWidget(widget)

        layout.addWidget(QLabel("Amount"))
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("0.00")
        layout.addWidget(self.amount_input)

        self.error_label = QLabel("")
        self.error_label.setObjectName("errorLabel")
        self.error_label.setWordWrap(True)
        layout.addWidget(self.error_label)

        layout.addStretch()

        buttons = QHBoxLayout()
        cancel = QPushButton("Cancel")
        cancel.setProperty("class", "secondary")
        cancel.clicked.connect(self.main_window.go_to_main_menu)
        action = QPushButton(self.action_text)
        action.setProperty("class", "primary")
        action.clicked.connect(self.on_submit)
        buttons.addWidget(cancel)
        buttons.addWidget(action)
        layout.addLayout(buttons)

    def create_input(self, key, placeholder):
        field = QLineEdit()
        field.setPlaceholderText(placeholder)
        return field

    def build_details(self, values, amount):
        raise NotImplementedError

    def reset(self):
        for widget in self.inputs.values():
            if isinstance(widget, QLineEdit):
                widget.clear()
            elif isinstance(widget, QComboBox):
                widget.setCurrentIndex(0)
        self.amount_input.clear()
        self.error_label.setText("")

    def parse_amount(self):
        try:
            amount = float(self.amount_input.text().replace(",", "").strip())
        except ValueError:
            return None
        return amount if amount > 0 else None

    def on_submit(self):
        values = {}
        for key, widget in self.inputs.items():
            text = widget.currentText() if isinstance(widget, QComboBox) else widget.text()
            values[key] = text.strip()
        amount = self.parse_amount()

        if amount is None or not all(values.values()):
            self.error_label.setText("Fill in every field and enter an amount above zero.")
            return

        self.error_label.setText("")
        details, summary = self.build_details(values, amount)
        self.main_window.go_to_confirm(self.kind, details, summary)
