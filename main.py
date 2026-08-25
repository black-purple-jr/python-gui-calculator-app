import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QPushButton,
    QGridLayout,
    QLCDNumber,
    QLayoutItem,
    QSizePolicy,
)


class FenetrePrincipale(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculator")
        self.setMinimumSize(500, 600)
        self.setMaximumSize(500, 600)
        self.setStyleSheet("background-color: #333333; border: 5px solid #333333")

        # variables de fonctionnement
        self.current_value = "0"
        self.first_operand = None
        self.operator = None
        self.waiting_for_second_operand = False
        self.memory = 0.0

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        grid = QGridLayout()

        self.screen = QLCDNumber()
        self.screen.setDigitCount(15)
        self.screen.display("0")
        grid.addWidget(self.screen, 0, 0, 1, 4)

        grid.addWidget(self.create_button("MC"), 1, 0)
        grid.addWidget(self.create_button("M+"), 1, 1)
        grid.addWidget(self.create_button("M-"), 1, 2)
        grid.addWidget(self.create_button("MR"), 1, 3)

        grid.addWidget(self.create_button("7"), 2, 0)
        grid.addWidget(self.create_button("8"), 2, 1)
        grid.addWidget(self.create_button("9"), 2, 2)
        grid.addWidget(self.create_button("/"), 2, 3)

        grid.addWidget(self.create_button("4"), 3, 0)
        grid.addWidget(self.create_button("5"), 3, 1)
        grid.addWidget(self.create_button("6"), 3, 2)
        grid.addWidget(self.create_button("*"), 3, 3)

        grid.addWidget(self.create_button("1"), 4, 0)
        grid.addWidget(self.create_button("2"), 4, 1)
        grid.addWidget(self.create_button("3"), 4, 2)
        grid.addWidget(self.create_button("-"), 4, 3)

        grid.addWidget(self.create_button("0"), 5, 0, 1, 2)
        grid.addWidget(self.create_button("."), 5, 2)
        grid.addWidget(self.create_button("+"), 5, 3)

        reset_button = self.create_button("Reset")
        grid.addWidget(reset_button, 6, 0, 1, 3)
        equal_button = self.create_button("=")
        grid.addWidget(equal_button, 6, 3)

        for line in range(7):
            grid.setRowStretch(line, 2 if line == 0 else 1)

        for idx in range(grid.count()):
            item: QLayoutItem = grid.itemAt(idx)
            widget = item.widget()
            widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

            if isinstance(widget, QPushButton):
                widget.setStyleSheet(
                    "background-color: #444444; color: white; font-weight: bold; font-size: 20px;"
                )
            else:
                widget.setStyleSheet("background-color: #a2af77; font-weight: bold;")

        equal_button.setStyleSheet(
            "background-color: white; font-weight: bold; font-size: 20px; color: #444444"
        )
        reset_button.setStyleSheet(
            "background: #b22222; font-weight: bold; font-size: 20px; color: white"
        )

        central_widget.setLayout(grid)

    def create_button(self, text):
        button = QPushButton(text)
        button.clicked.connect(lambda: self.handle_button_click(text))
        return button

    def handle_button_click(self, text):
        if text.isdigit():
            self.input_digit(text)
        elif text == ".":
            self.input_decimale_point()
        elif text in ["+", "-", "*", "/"]:
            self.input_operator(text)
        elif text == "=":
            self.calculate_result()
        elif text == "M+":
            self.memory_add()
        elif text == "M-":
            self.memory_delete()
        elif text == "MR":
            self.memory_display()
        elif text == "MC":
            self.memory_clear()
        elif text == "Reset":
            self.reset_calculator()

    def input_digit(self, digit):
        if self.waiting_for_second_operand:
            self.current_value = digit
            self.waiting_for_second_operand = False

        else:
            if self.current_value == "0":
                self.current_value = digit
            else:
                self.current_value += digit

        self.update_screen()

    def input_decimale_point(self):
        if self.waiting_for_second_operand:
            self.current_value = "0."
            self.waiting_for_second_operand = False

        else:
            if "." not in self.current_value:
                self.current_value += "."

        self.update_screen()

    def input_operator(self, operator):
        current_number = float(self.current_value)
        if self.first_operand == None:
            self.first_operand = current_number

        else:
            if self.operator is not None:
                result = self.perform_calculation(
                    self.first_operand, current_number, self.operator
                )
                if result is None:
                    self.show_error()
                    return
                self.first_operand = result
                self.current_value = self.format_number(result)
                self.update_screen()
        self.operator = operator
        self.waiting_for_second_operand = True

    def calculate_result(self):
        if self.operator is None or self.first_operand is None:
            return

        second_operand = float(self.current_value)
        result = self.perform_calculation(
            self.first_operand, second_operand, self.operator
        )

        if result is None:
            self.show_error()
            return

        self.current_value = self.format_number(result)
        self.update_screen()
        self.first_operand = None
        self.operator = None
        self.waiting_for_second_operand = True

    def perform_calculation(self, first, second, operator):
        if operator == "+":
            return first + second
        elif operator == "-":
            return first - second
        elif operator == "*":
            return first * second
        elif operator == "/":
            if second == 0:
                return None
            return first / second
        return second

    def memory_add(self):
        try:
            self.memory += float(self.current_value)
            self.waiting_for_second_operand = True
        except ValueError:
            self.show_error()

    def memory_delete(self):
        try:
            self.memory -= float(self.current_value)
            self.waiting_for_second_operand = True
        except ValueError:
            self.show_error()

    def memory_display(self):
        self.current_value = self.format_number(self.memory)
        self.update_screen()
        self.waiting_for_second_operand = True

    def memory_clear(self):
        self.memory = 0.0

    def reset_calculator(self):
        # NB: réinitialiser la calculatrice sans effacer la mémoire
        self.current_value = "0"
        self.first_operand = None
        self.operator = None
        self.waiting_for_second_operand = False
        self.update_screen()

    def update_screen(self):
        self.screen.display(self.current_value)

    def show_error(self):
        self.screen.display("Error")
        self.current_value = "0"
        self.first_operand = None
        self.operator = None
        self.waiting_for_second_operand = True

    def format_number(self, number):
        if number == int(number):
            return str(int(number))
        return str(round(number, 10))


if __name__ == "__main__":
    app = QApplication(sys.argv)

    app.setStyleSheet("""
        QLCDNumber {
            border-radius: 12px;
            
        }

        QPushButton {
            border-radius: 12px;
        }
    """)

    myWindow = FenetrePrincipale()
    myWindow.show()
    sys.exit(app.exec())
