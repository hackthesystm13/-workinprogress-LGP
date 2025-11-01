import sys

# Try PyQt5 first, then PySide6. Fail with a clear message if neither is installed.
try:
    from PyQt5.QtWidgets import QApplication
    USING_QT = "PyQt5"
except Exception:
    try:
        from PySide6.QtWidgets import QApplication
        USING_QT = "PySide6"
    except Exception:
        raise RuntimeError("Install a Qt binding first: `pip install PyQt5` or `pip install PySide6`")

# phishing_tool acts as a resilient adapter that will pick your real GUI where it lives
from phishing_tool import PhishingTool

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PhishingTool()
    window.show()

    # Support both app.exec_() (older PyQt) and app.exec() (PySide6)
    if hasattr(app, "exec_"):
        exit_code = app.exec_()
    else:
        exit_code = app.exec()
    sys.exit(exit_code)