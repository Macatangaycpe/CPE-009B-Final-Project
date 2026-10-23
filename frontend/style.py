"""Halloween theme for the E-Wallet. Same selectors as before, new colors."""
 
# Palette
MIDNIGHT = "#17101f"   # window background
CRYPT = "#241733"      # cards and inputs
GRAVE = "#3b2757"      # borders, disabled
PUMPKIN = "#ff7a1a"    # primary actions, titles
EMBER = "#ff9a4d"      # primary hover
WITCH = "#8b4dff"      # secondary actions, focus
BONE = "#f3e6d0"       # main text
FOG = "#a898c2"        # secondary text
SLIME = "#a6e22e"      # balance only
BLOOD = "#ff5c6a"      # errors
 
STYLE_SHEET = f"""
QWidget {{
    background-color: {MIDNIGHT};
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 14px;
    color: {BONE};
}}
 
QLabel {{
    background-color: transparent;
}}
 
QScrollArea {{
    background-color: transparent;
    border: none;
}}
 
QLabel#titleLabel {{
    font-family: 'Chiller', 'Georgia', serif;
    font-size: 34px;
    font-weight: bold;
    color: {PUMPKIN};
    margin-bottom: 20px;
    margin-top: 20px;
}}
 
QLabel#balanceLabel {{
    font-size: 32px;
    font-weight: bold;
    color: {SLIME};
    background-color: transparent;
    border: none;
}}
 
QLabel#subtitleLabel {{
    font-size: 16px;
    color: {FOG};
    margin-bottom: 10px;
}}
 
QLabel#errorLabel {{
    color: {BLOOD};
    background-color: transparent;
}}
 
QLineEdit, QComboBox {{
    padding: 10px;
    border: 1px solid {GRAVE};
    border-radius: 8px;
    background-color: {CRYPT};
    color: {BONE};
    font-size: 16px;
    selection-background-color: {WITCH};
    placeholder-text-color: {FOG};
}}
 
QLineEdit:focus, QComboBox:focus {{
    border: 1px solid {PUMPKIN};
}}
 
QComboBox::drop-down {{
    border: none;
    width: 28px;
}}
 
QComboBox QAbstractItemView {{
    background-color: {CRYPT};
    color: {BONE};
    border: 1px solid {PUMPKIN};
    selection-background-color: {WITCH};
    selection-color: {BONE};
}}
 
QPushButton.primary {{
    background-color: {PUMPKIN};
    color: #1a0d00;
    border: none;
    border-radius: 8px;
    padding: 12px;
    font-size: 16px;
    font-weight: bold;
}}
 
QPushButton.primary:hover {{
    background-color: {EMBER};
}}
 
QPushButton.primary:pressed {{
    background-color: #d9620d;
}}
 
QPushButton.primary:disabled {{
    background-color: {GRAVE};
    color: {FOG};
}}
 
QPushButton.secondary {{
    background-color: transparent;
    color: {WITCH};
    border: 2px solid {WITCH};
    border-radius: 8px;
    padding: 10px;
    font-size: 16px;
}}
 
QPushButton.secondary:hover {{
    background-color: {WITCH};
    color: {BONE};
}}
 
QPushButton.secondary:disabled {{
    color: {FOG};
    border-color: {GRAVE};
}}
 
QPushButton.menuButton {{
    background-color: {CRYPT};
    color: {BONE};
    border: 2px solid {PUMPKIN};
    border-radius: 12px;
    padding: 20px;
    font-size: 18px;
    font-weight: bold;
}}
 
QPushButton.menuButton:hover {{
    background-color: {PUMPKIN};
    color: #1a0d00;
}}
 
QFrame.card {{
    background-color: {CRYPT};
    border: 1px solid {WITCH};
    border-radius: 12px;
    padding: 20px;
}}
 
QFrame.card QLabel {{
    background-color: transparent;
    border: none;
}}
 
QScrollBar:vertical {{
    background: {MIDNIGHT};
    width: 10px;
    margin: 0;
}}
 
QScrollBar::handle:vertical {{
    background: {WITCH};
    border-radius: 5px;
    min-height: 24px;
}}
 
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}
 
QToolTip {{
    background-color: {CRYPT};
    color: {PUMPKIN};
    border: 1px solid {PUMPKIN};
}}
"""
