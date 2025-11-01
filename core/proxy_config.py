import os

def configure_proxies():
    proxy_list = [
        "socks5 127.0.0.1 9050",
        "http 192.168.1.1 8080",
        "socks4 10.0.0.1 1080"
    ]

    conf_file = "/etc/proxychains4.conf"

    with open(conf_file, 'a') as file:
        file.write("\n[ProxyList]\n")
        for proxy in proxy_list:
            file.write(proxy + "\n")

    os.system("sed -i '/proxy_dns/d' " + conf_file)
    os.system("sed -i '/tcp_read_time_out/d' " + conf_file)
    os.system("sed -i '/tcp_connect_time_out/d' " + conf_file)

    with open(conf_file, 'a') as file:
        file.write("proxy_dns\n")
        file.write("tcp_read_time_out 15000\n")
        file.write("tcp_connect_time_out 8000\n")

    print("ProxyChains configuration updated successfully.")