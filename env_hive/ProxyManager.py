import os
import random


def get_all_proxies():
    with open(os.path.join("proxies.txt"), "r") as file:
        proxies = []
        for line in file.readlines():
            proxies.append(line.replace("\n", "").replace("\r", "").replace("\r\n", "").replace("\n\r", "").replace(" ", ""))
        return proxies


def proxy_string_to_proxy_header(proxy_ip):
    task_proxy = ""
    if proxy_ip != "":
        temp_proxy = proxy_ip.split(":")
        if len(temp_proxy) == 4:
            task_proxy = {
                "http": "http://" + temp_proxy[2] + ":" + temp_proxy[3] + "@" + temp_proxy[0] + ":" + temp_proxy[1],
                "https": "http://" + temp_proxy[2] + ":" + temp_proxy[3] + "@" + temp_proxy[0] + ":" + temp_proxy[1],
            }
        else:
            task_proxy = {
                "http": "http://" + temp_proxy[0] + ":" + temp_proxy[1],
                "https": "http://" + temp_proxy[0] + ":" + temp_proxy[1],
            }
    return task_proxy


def get_random_proxy():
    proxies = get_all_proxies()
    if len(proxies) > 0:
        proxy = random.choice(proxies)
        task_proxy = proxy_string_to_proxy_header(proxy)
        return task_proxy
    else:
        return None