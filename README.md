# Python + PySide6 calculator

a simple calculator app built with Python and PySide6 that has basic operations and memory management.

You may recognize that I use PySide for my GUIs, it's the same as PyQt there is only a license difference, the components, events, functionality..... are all the same but you install PyQt5 instead of PySide6 and it only differs in the imports, like:

```python
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton
```

becomes like ths for PyQt5:

```python
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton
```