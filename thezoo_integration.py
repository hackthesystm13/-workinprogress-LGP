import os
from git import Repo
import subprocess

def clone_thezoo():
    thezoo_path = os.path.join(os.path.dirname(__file__), 'TheZoo')
    if not os.path.exists(thezoo_path):
        Repo.clone_from('https://github.com/ytisf/theZoo.git', thezoo_path)
    return thezoo_path

def list_malware_samples():
    thezoo_path = os.path.join(os.path.dirname(__file__), 'TheZoo')
    if not os.path.exists(thezoo_path):
        clone_thezoo()
    malware_path = os.path.join(thezoo_path, 'malwares')
    if not os.path.exists(malware_path):
        return []
    return os.listdir(malware_path)

def fetch_malware_sample(malware_name, target_device):
    thezoo_path = os.path.join(os.path.dirname(__file__), 'TheZoo')
    if not os.path.exists(thezoo_path):
        clone_thezoo()
    malware_path = os.path.join(thezoo_path, 'malwares', malware_name)
    if not os.path.exists(malware_path):
        raise FileNotFoundError(f"Malware sample {malware_name} not found in TheZoo.")
    return malware_path

def deploy_malware(malware_path, target):
    # This function should be updated to match the targeted device and deploy the malware accordingly
    print(f"Deploying malware from {malware_path} to {target}")

def run_thezoo():
    thezoo_path = os.path.join(os.path.dirname(__file__), 'TheZoo')
    if not os.path.exists(thezoo_path):
        clone_thezoo()
    subprocess.run(['python', os.path.join(thezoo_path, 'run.py')])

if __name__ == "__main__":
    samples = list_malware_samples()
    print("Available malware samples:")
    for sample in samples:
        print(sample)