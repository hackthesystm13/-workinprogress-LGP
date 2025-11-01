"""Clean, robust full GUI implementation for the project.

This file defines a full-featured `PhishingTool` window that the project can
use. It imports Qt classes from PyQt5 or PySide6 (whichever is available) and
defers imports of heavier project internals (core/malware) until runtime so
that importing this module is less likely to fail in test or analysis runs.

The implementations here keep user-facing behavior similar to the original
design but are defensive about missing dependencies.
"""
from __future__ import annotations

try:
    # Prefer PyQt5
    from PyQt5.QtWidgets import (
        QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit,
        QTextEdit, QMessageBox, QComboBox, QTabWidget, QFormLayout, QGroupBox, QFileDialog
    )
    USING_QT = "PyQt5"
except Exception:
    # Fall back to PySide6
    from PySide6.QtWidgets import (
        QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit,
        QTextEdit, QMessageBox, QComboBox, QTabWidget, QFormLayout, QGroupBox, QFileDialog
    )
    USING_QT = "PySide6"

from typing import List


def _safe_import_core():
    """Try to import core functions; return a dict of callables or placeholders.

    Import errors are caught and replaced with stub functions that show an
    error message when called. This prevents import-time failures.
    """
    def _missing(name: str):
        def _fn(*args, **kwargs):
            raise ImportError(f"Optional dependency missing: {name}")

        return _fn

    try:
        from core.sms_sender import send_sms
    except Exception:
        send_sms = _missing("core.sms_sender.send_sms")

    try:
        from core.email_sender import send_email
    except Exception:
        send_email = _missing("core.email_sender.send_email")

    try:
        from core.proxy_config import configure_proxies
    except Exception:
        configure_proxies = _missing("core.proxy_config.configure_proxies")

    try:
        # these live in malware/thezoo_integration.py
        from malware.thezoo_integration import fetch_malware_sample, deploy_malware, list_malware_samples, run_thezoo
    except Exception:
        fetch_malware_sample = _missing("malware.thezoo_integration.fetch_malware_sample")
        deploy_malware = _missing("malware.thezoo_integration.deploy_malware")
        list_malware_samples = lambda: []
        run_thezoo = _missing("malware.thezoo_integration.run_thezoo")

    return {
        "send_sms": send_sms,
        "send_email": send_email,
        "configure_proxies": configure_proxies,
        "fetch_malware_sample": fetch_malware_sample,
        "deploy_malware": deploy_malware,
        "list_malware_samples": list_malware_samples,
        "run_thezoo": run_thezoo,
    }


class PhishingTool(QMainWindow):
    """A full GUI for managing phishing campaigns and (optional) malware tasks."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Letsgophishing Pro")
        self.setGeometry(100, 100, 900, 700)

        self._core = _safe_import_core()

        self._init_ui()

    def _init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout()
        central.setLayout(layout)

        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        self._create_phishing_tab()
        self._create_malware_tab()

    def _create_phishing_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.title_label = QLabel("Phishing Campaign Manager")
        layout.addWidget(self.title_label)

        self.target_input = QLineEdit()
        self.target_input.setPlaceholderText("Enter target email(s) or phone numbers")
        layout.addWidget(self.target_input)

        self.message_input = QTextEdit()
        self.message_input.setPlaceholderText("Enter phishing message")
        layout.addWidget(self.message_input)

        self.template_combo = QComboBox()
        self.template_combo.addItems(["Facebook", "Google", "Microsoft", "Custom"])
        layout.addWidget(self.template_combo)

        self.select_custom_template_button = QPushButton("Select Custom Template")
        self.select_custom_template_button.clicked.connect(self.select_custom_template)
        layout.addWidget(self.select_custom_template_button)

        self.custom_email_input = QLineEdit()
        self.custom_email_input.setPlaceholderText("Enter custom from email (optional)")
        layout.addWidget(self.custom_email_input)

        self.custom_sms_input = QLineEdit()
        self.custom_sms_input.setPlaceholderText("Enter custom from SMS number (optional)")
        layout.addWidget(self.custom_sms_input)

        self.start_button = QPushButton("Start Campaign")
        self.start_button.clicked.connect(self.start_campaign)
        layout.addWidget(self.start_button)

        self.status_label = QLabel("Status: Idle")
        layout.addWidget(self.status_label)

        self.configure_proxies_button = QPushButton("Configure Proxies")
        self.configure_proxies_button.clicked.connect(self.configure_proxies)
        layout.addWidget(self.configure_proxies_button)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "Phishing Campaign")

    def _create_malware_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        group = QGroupBox("Malware Deployment")
        form = QFormLayout()

        self.malware_combo = QComboBox()
        samples = []
        try:
            samples = list(self._core["list_malware_samples"]())
        except Exception:
            samples = []
        if not samples:
            samples = ["(no samples available)"]
        self.malware_combo.addItems(samples)
        form.addRow("Select Malware:", self.malware_combo)

        self.device_combo = QComboBox()
        self.device_combo.addItems(["Windows", "Linux", "MacOS", "Android", "iOS"])
        form.addRow("Select Target Device:", self.device_combo)

        self.deploy_malware_button = QPushButton("Deploy Malware")
        self.deploy_malware_button.clicked.connect(self.deploy_malware)
        form.addRow(self.deploy_malware_button)

        self.run_thezoo_button = QPushButton("Run TheZoo")
        self.run_thezoo_button.clicked.connect(self._safe_run_thezoo)
        form.addRow(self.run_thezoo_button)

        group.setLayout(form)
        layout.addWidget(group)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "Malware Deployment")

    def start_campaign(self):
        targets = self.target_input.text().strip()
        message = self.message_input.toPlainText().strip()
        template = self.template_combo.currentText()
        custom_email = self.custom_email_input.text().strip()
        custom_sms = self.custom_sms_input.text().strip()

        self.status_label.setText("Status: Campaign Started")

        # Attempt to call start/send functions; show friendly errors on failure
        try:
            # Prefer an explicit start function if provided; otherwise call send functions
            send_email = self._core["send_email"]
            send_sms = self._core["send_sms"]

            if custom_email:
                send_email(targets, message, custom_email)
            else:
                send_email(targets, message)

            if custom_sms:
                send_sms(targets, message, custom_sms)
            else:
                send_sms(targets, message)
        except ImportError as e:
            QMessageBox.warning(self, "Missing Dependency", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

        QMessageBox.information(self, "Campaign Started", "Phishing campaign workflow executed (see logs).")

    def configure_proxies(self):
        try:
            configure = self._core["configure_proxies"]
            configure()
            QMessageBox.information(self, "Proxy Configuration", "Proxies have been configured successfully!")
        except ImportError as e:
            QMessageBox.warning(self, "Missing Dependency", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def deploy_malware(self):
        malware_name = self.malware_combo.currentText()
        target = self.target_input.text().strip()
        try:
            fetch = self._core["fetch_malware_sample"]
            deploy = self._core["deploy_malware"]
            path = fetch(malware_name)
            deploy(path, target)
            QMessageBox.information(self, "Malware Deployment", f"Malware {malware_name} has been deployed to {target} successfully!")
        except ImportError as e:
            QMessageBox.warning(self, "Missing Dependency", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def _safe_run_thezoo(self):
        try:
            run = self._core["run_thezoo"]
            run()
            QMessageBox.information(self, "TheZoo", "TheZoo executed (see logs).")
        except ImportError as e:
            QMessageBox.warning(self, "Missing Dependency", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def select_custom_template(self):
        options = QFileDialog.Options()
        file_dialog = QFileDialog()
        file_dialog.setOptions(options)
        file_dialog.setNameFilter("HTML files (*.html)")
        file_dialog.setWindowTitle("Select Custom Template")
        # Use the exec pattern for both PyQt and PySide compatibility
        accepted = file_dialog.exec_() if hasattr(file_dialog, "exec_") else file_dialog.exec()
        if accepted:
            self.custom_template_path = file_dialog.selectedFiles()[0]
            QMessageBox.information(self, "Custom Template Selected", f"Custom template selected: {self.custom_template_path}")


__all__ = ["PhishingTool", "USING_QT"]
