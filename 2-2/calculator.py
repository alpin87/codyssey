from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, 
                             QVBoxLayout, QGridLayout, QPushButton, QLabel)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont


class Calculator:
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.current_value = 0
        self.stored_value = 0
        self.operation = ''
        self.result = '0'
        self.new_input = True
        self.last_button_was_equals = False
    
    def add(self, a, b):
        return a + b
    
    def subtract(self, a, b):
        return a - b
    
    def multiply(self, a, b):
        return a * b
    
    def divide(self, a, b):
        if b == 0:
            return 'Error'
        return a / b
    
    def negative_positive(self):
        current = float(self.result)
        current = -current
        
        if current.is_integer():
            current = int(current)
        
        self.result = str(current)
        return self.result
    
    def percent(self):
        current = float(self.result)
        current = current / 100
        
        if current.is_integer():
            current = int(current)
        
        self.result = str(current)
        return self.result
    
    def calculate(self):
        try:
            a = self.stored_value
            b = float(self.result)
            
            if self.operation == '+':
                result = self.add(a, b)
            elif self.operation == '-':
                result = self.subtract(a, b)
            elif self.operation == '×':
                result = self.multiply(a, b)
            elif self.operation == '÷':
                result = self.divide(a, b)
            else:
                return self.result
            
            if isinstance(result, float) and result.is_integer():
                result = int(result)
                
            if isinstance(result, float):
                decimal_places = len(str(result).split('.')[-1])
                if decimal_places > 6:
                    result = round(result, 6)
            
            self.result = str(result)
            return self.result
        
        except (ValueError, TypeError):
            self.result = 'Error'
            return self.result
    
    def equal(self):
        if not self.operation:
            return self.result
            
        result = self.calculate()
        self.operation = ''
        self.stored_value = float(result)
        self.new_input = True
        self.last_button_was_equals = True
        return result
    
    def set_operation(self, operation):
        if not self.new_input and self.operation:
            self.equal()
        
        try:
            self.stored_value = float(self.result)
        except ValueError:
            self.reset()
            return self.result
            
        self.operation = operation
        self.new_input = True
        self.last_button_was_equals = False
        return self.result
    
    def input_digit(self, digit):
        if self.new_input or self.result == '0' or self.last_button_was_equals:
            self.result = digit
            self.new_input = False
        else:
            self.result += digit
        
        self.last_button_was_equals = False
        return self.result
    
    def input_decimal(self):
        if self.new_input or self.last_button_was_equals:
            self.result = '0.'
            self.new_input = False
        elif '.' not in self.result:
            self.result += '.'
        
        self.last_button_was_equals = False
        return self.result


class CalculatorWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('아이폰 계산기')
        self.setMinimumSize(300, 500)
        
        self.calculator = Calculator()
        
        self.init_ui()
    
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        self.result_label = QLabel(self.calculator.result)
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
    
    def update_display(self, value=None):
        if value is None:
            value = self.calculator.result
            
        font_size = 48
        if len(value) > 9:
            font_size = 36
        if len(value) > 12:
            font_size = 28
        if len(value) > 16:
            font_size = 24
            
        self.result_label.setFont(QFont('Arial', font_size))
        self.result_label.setText(value)
    
    def on_digit(self, digit):
        result = self.calculator.input_digit(digit)
        self.update_display(result)
    
    def on_decimal(self, _):
        result = self.calculator.input_decimal()
        self.update_display(result)
    
    def on_operator(self, operator):
        result = self.calculator.set_operation(operator)
        self.update_display(result)
    
    def on_equals(self, _):
        result = self.calculator.equal()
        self.update_display(result)
    
    def on_clear(self, _):
        self.calculator.reset()
        self.update_display()
    
    def on_toggle_sign(self, _):
        result = self.calculator.negative_positive()
        self.update_display(result)
    
    def on_percent(self, _):
        result = self.calculator.percent()
        self.update_display(result)


def main():
    app = QApplication([])
    calculator = CalculatorWindow()
    calculator.show()
    app.exec_()


if __name__ == '__main__':
    main()