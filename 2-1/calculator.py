from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, 
                             QVBoxLayout, QGridLayout, QPushButton, QLabel)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont


class CalculatorWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('아이폰 계산기')
        self.setMinimumSize(300, 500)
        
        self.reset_calc()
        
        self.init_ui()
    
    def reset_calc(self):
        self.display_value = '0'
        self.waiting_for_operand = True
        self.pending_operand = 0
        self.pending_operation = ''
        self.last_button_was_equals = False
    
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        self.result_label = QLabel(self.display_value)
        self.result_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.result_label.setFont(QFont('Arial', 48))
        self.result_label.setStyleSheet('''
            QLabel {
                color: white;
                background-color: #333333;
                padding: 15px;
                min-height: 100px;
            }
        ''')
        main_layout.addWidget(self.result_label)
        
        buttons_widget = QWidget()
        buttons_layout = QGridLayout(buttons_widget)
        buttons_layout.setSpacing(1)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        
        button_data = [
            ('AC', 0, 0, self.on_clear), ('±', 0, 1, self.on_toggle_sign), 
            ('%', 0, 2, self.on_percent), ('÷', 0, 3, self.on_operator),
            ('7', 1, 0, self.on_digit), ('8', 1, 1, self.on_digit), 
            ('9', 1, 2, self.on_digit), ('×', 1, 3, self.on_operator),
            ('4', 2, 0, self.on_digit), ('5', 2, 1, self.on_digit), 
            ('6', 2, 2, self.on_digit), ('-', 2, 3, self.on_operator),
            ('1', 3, 0, self.on_digit), ('2', 3, 1, self.on_digit), 
            ('3', 3, 2, self.on_digit), ('+', 3, 3, self.on_operator),
            ('0', 4, 0, self.on_digit, 2), ('.', 4, 2, self.on_decimal), 
            ('=', 4, 3, self.on_equals)
        ]
        
        for data in button_data:
            if len(data) == 5:
                text, row, col, callback, colspan = data
                button = self.create_button(text, callback)
                buttons_layout.addWidget(button, row, col, 1, colspan)
            else:
                text, row, col, callback = data
                button = self.create_button(text, callback)
                buttons_layout.addWidget(button, row, col)
        
        main_layout.addWidget(buttons_widget)
    
    def create_button(self, text, callback):
        button = QPushButton(text)
        button.setMinimumSize(QSize(80, 80))
        button.setFont(QFont('Arial', 24))
        
        if text in ['÷', '×', '-', '+', '=']:
            button.setStyleSheet('''
                QPushButton {
                    background-color: #FF9500;
                    color: white;
                    border-radius: 40px;
                }
                QPushButton:pressed {
                    background-color: #FFCC80;
                }
            ''')
        elif text in ['AC', '±', '%']:
            button.setStyleSheet('''
                QPushButton {
                    background-color: #A5A5A5;
                    color: black;
                    border-radius: 40px;
                }
                QPushButton:pressed {
                    background-color: #D9D9D9;
                }
            ''')
        else:
            button.setStyleSheet('''
                QPushButton {
                    background-color: #333333;
                    color: white;
                    border-radius: 40px;
                }
                QPushButton:pressed {
                    background-color: #737373;
                }
            ''')
        
        button.clicked.connect(lambda: callback(text))
        
        return button
    
    def update_display(self):
        self.result_label.setText(self.display_value)
    
    def on_digit(self, digit):
        if self.waiting_for_operand or self.display_value == '0' or self.last_button_was_equals:
            self.display_value = digit
            self.waiting_for_operand = False
        else:
            self.display_value += digit
        
        self.last_button_was_equals = False
        self.update_display()
    
    def on_decimal(self, _):
        if self.waiting_for_operand or self.last_button_was_equals:
            self.display_value = '0.'
            self.waiting_for_operand = False
        elif '.' not in self.display_value:
            self.display_value += '.'
        
        self.last_button_was_equals = False
        self.update_display()
    
    def on_operator(self, operator):
        operand = float(self.display_value)
        
        if self.pending_operation and not self.waiting_for_operand:
            self.calculate()
        else:
            self.pending_operand = operand
        
        self.pending_operation = operator
        self.waiting_for_operand = True
        self.last_button_was_equals = False
    
    def on_equals(self, _):
        if self.pending_operation and not self.waiting_for_operand:
            self.calculate()
            self.pending_operation = ''
            self.last_button_was_equals = True
    
    def calculate(self):
        operand = float(self.display_value)
        
        if self.pending_operation == '+':
            result = self.pending_operand + operand
        elif self.pending_operation == '-':
            result = self.pending_operand - operand
        elif self.pending_operation == '×':
            result = self.pending_operand * operand
        elif self.pending_operation == '÷':
            if operand == 0:
                result = 'Error'
            else:
                result = self.pending_operand / operand
        else:
            result = operand
        
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        
        self.display_value = str(result)
        self.pending_operand = result
        self.waiting_for_operand = True
        self.update_display()
    
    def on_clear(self, _):
        self.reset_calc()
        self.update_display()
    
    def on_toggle_sign(self, _):
        value = float(self.display_value)
        value = -value
        
        if value.is_integer():
            value = int(value)
        
        self.display_value = str(value)
        self.update_display()
    
    def on_percent(self, _):
        value = float(self.display_value)
        value = value / 100
        
        if value.is_integer():
            value = int(value)
        
        self.display_value = str(value)
        self.update_display()


def main():
    app = QApplication([])
    calculator = CalculatorWindow()
    calculator.show()
    app.exec_()


if __name__ == '__main__':
    main()