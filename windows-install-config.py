from time import sleep

import requests
import os
import json  # 新增: 导入json库
from tqdm import tqdm  # 导入tqdm库
import zipfile  # 导入zipfile库
import tkinter as tk
from tkinter import simpledialog
import subprocess  # 新增: 导入subprocess库
# 新增: 导入pywinauto库
import pywinauto
# 新增: 导入webbrowser库
import webbrowser
# 新增: 导入win32com.client库
import win32com.client

def download_file(url, target_file):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        total_size = int(response.headers.get('content-length', 0))
        block_size = 128

        with open(target_file, 'wb') as f:
            # 使用tqdm显示进度条
            for data in tqdm(response.iter_content(block_size), total=total_size // block_size, unit='KB', desc=target_file):
                f.write(data)
            f.flush()
    except requests.exceptions.RequestException as e:
        exit(1)

def download_and_merge_files(urls, target_files, merged_file):
    for url, target_file in zip(urls, target_files):
        download_file(url, target_file)
    
    with open(merged_file, 'wb') as outfile:
        for target_file in target_files:
            with open(target_file, 'rb') as infile:
                outfile.write(infile.read())
            outfile.flush()
            os.remove(target_file)  # 删除已合并的文件

# 新增: 解压缩文件的方法
def unzip_file(zip_path, extract_to="."):  # 修改: 将解压缩目录改为当前目录
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    os.remove(zip_path)  # 新增: 解压缩完成后删除压缩包文件

# 新增: 获取用户输入的订阅链接
def get_subscription_link():
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    subscription_link = simpledialog.askstring("输入", "请输入订阅链接:")
    if not subscription_link:
        exit(1)  # 如果用户点击取消或输入为空，则退出程序
    return subscription_link

# urls = [
#     "https://gcore.jsdelivr.net/gh/liliBestCoder/vpn/binary/nekoray.zip.001",
#     "https://gcore.jsdelivr.net/gh/liliBestCoder/vpn/binary/nekoray.zip.002",
#     "https://gcore.jsdelivr.net/gh/liliBestCoder/vpn/binary/nekoray.zip.003"
# ]
# target_files = ["nekoray.zip.001", "nekoray.zip.002", "nekoray.zip.003"]
# merged_file = "nekoray.zip"
#
# download_and_merge_files(urls, target_files, merged_file)
# unzip_file(merged_file)  # 解压缩合并后的文件到当前目录
#
# # 新增: 获取用户输入的订阅链接
# subscription_link = get_subscription_link()
#
# # 新增: 直接写入JSON文件
# group_file_path = "nekoray/config/groups/1.json"
# group_dir = os.path.dirname(group_file_path)
# if not os.path.exists(group_dir):
#     os.makedirs(group_dir)
#
# group_data = {
#     "archive": False,
#     "column_width": [150, 150, 233, 150, 150],
#     "front_proxy_id": -1,
#     "id": 1,
#     "lastup": 1743427857,
#     "manually_column_width": True,
#     "name": "免费订阅",
#     "order": [],
#     "skip_auto_update": False,
#     "url": subscription_link
# }
# with open(group_file_path, 'w', encoding='utf-8') as file:
#     json.dump(group_data, file, ensure_ascii=False, indent=4)
#
# # 新增: 写入pm.json文件
# pm_file_path = "nekoray/config/groups/pm.json"
# pm_data = {
#     "groups": [
#         1
#     ]
# }
# with open(pm_file_path, 'w', encoding='utf-8') as file:
#     json.dump(pm_data, file, ensure_ascii=False, indent=4)
#
# # 新增: 写入nekobox.json文件
# nekobox_file_path = "nekoray/config/groups/nekobox.json"
# nekobox_data = {
#     "active_routing": "Default",
#     "check_include_pre": False,
#     "conn_stat": False,
#     "core_box_clash_api": -9090,
#     "current_group": 1,
#     "custom_inbound": "{\"inbounds\": []}",
#     "custom_route": "{\"rules\": []}",
#     "extraCore": {
#         "core_map": "{\"hysteria2\":\"\",\"naive\":\"\",\"tuic\":\"\"}"
#     },
#     "fakedns": False,
#     "inbound_address": "0.0.0.0",
#     "inbound_auth": {},
#     "inbound_socks_port": 2080,
#     "language": 0,
#     "log_ignore": [],
#     "log_level": "info",
#     "max_log_line": 200,
#     "mux_concurrency": 8,
#     "mux_default_on": False,
#     "mux_padding": False,
#     "mux_protocol": "h2mux",
#     "mw_size": "800x600",
#     "remember_enable": False,
#     "remember_id": -1919,
#     "skip_cert": False,
#     "splitter_state": "AAAA/wAAAAEAAAACAAAA9QAAAPUB/////wEAAAACAA==",
#     "spmode2": [],
#     "start_minimal": False,
#     "sub_auto_update": 1440,
#     "sub_clear": False,
#     "sub_insecure": False,
#     "sub_use_proxy": False,
#     "test_concurrent": 5,
#     "test_dl_timeout": 30,
#     "test_url": "http://cp.cloudflare.com/",
#     "test_url_dl": "http://cachefly.cachefly.net/10mb.test",
#     "theme": "0",
#     "traffic_loop_interval": 1000,
#     "vpn_hide_console": True,
#     "vpn_impl": 0,
#     "vpn_internal_tun": True,
#     "vpn_ipv6": False,
#     "vpn_mtu": 9000,
#     "vpn_rule_white": False,
#     "vpn_strict_route": False
# }
# with open(nekobox_file_path, 'w', encoding='utf-8') as file:
#     json.dump(nekobox_data, file, ensure_ascii=False, indent=4)
#
# # 新增: 写入Default.json文件
# default_file_path = "nekoray/config/routes_box/Default.json"
# default_dir = os.path.dirname(default_file_path)
# if not os.path.exists(default_dir):
#     os.makedirs(default_dir)
#
# default_data = {
#     "block_domain": "geosite:category-ads-all\ndomain:appcenter.ms\ndomain:firebase.io\ndomain:crashlytics.com",
#     "custom": "{\"rules\": []}",
#     "def_outbound": "proxy",
#     "direct_dns": "https://doh.pub/dns-query",
#     "direct_domain": "geosite:cn",
#     "direct_ip": "geoip:cn\ngeoip:private",
#     "dns_final_out": "proxy",
#     "dns_routing": True,
#     "remote_dns": "https://dns.google/dns-query",
#     "sniffing_mode": 1,
#     "use_dns_object": False
# }
# with open(default_file_path, 'w', encoding='utf-8') as file:
#     json.dump(default_data, file, ensure_ascii=False, indent=4)

# 启动进程
nekobox_exe_path = "nekoray/nekobox.exe"
subprocess.Popen([nekobox_exe_path])

# 更新订阅
sleep(5)
app = pywinauto.Application(backend="uia").connect(path=nekobox_exe_path)
dlg = app.window(title_re=".*NekoBox.*")
dlg.type_keys("^U")

# url test
sleep(5)
dlg.type_keys("^%U")

# 按延迟排序
sleep(30)
dlg.child_window(auto_id="MainWindow.centralwidget", control_type="Group")\
   .child_window(auto_id="MainWindow.centralwidget.splitter", control_type="Custom") \
   .child_window(auto_id="MainWindow.centralwidget.splitter.tabWidget", control_type="Group") \
   .child_window(auto_id="MainWindow.centralwidget.splitter.tabWidget.qt_tabwidget_stackedwidget", control_type="Custom") \
   .child_window(auto_id="MainWindow.centralwidget.splitter.tabWidget.qt_tabwidget_stackedwidget.widget1", control_type="Group") \
   .child_window(auto_id="MainWindow.centralwidget.splitter.tabWidget.qt_tabwidget_stackedwidget.widget1.proxyListTable", control_type="Table") \
   .child_window(title="测试结果", control_type="Header") \
   .click_input()

# 选中延迟较小的行
sleep(5)
dlg.child_window(auto_id="MainWindow.centralwidget", control_type="Group") \
    .child_window(auto_id="MainWindow.centralwidget.splitter", control_type="Custom") \
    .child_window(auto_id="MainWindow.centralwidget.splitter.tabWidget", control_type="Group") \
    .child_window(auto_id="MainWindow.centralwidget.splitter.tabWidget.qt_tabwidget_stackedwidget", control_type="Custom") \
    .child_window(auto_id="MainWindow.centralwidget.splitter.tabWidget.qt_tabwidget_stackedwidget.widget1", control_type="Group") \
    .child_window(auto_id="MainWindow.centralwidget.splitter.tabWidget.qt_tabwidget_stackedwidget.widget1.proxyListTable", control_type="Table") \
    .child_window(control_type="DataItem", found_index=0)\
    .click_input()

# 启动节点
sleep(2)
dlg.type_keys("{ENTER}")

# 开启系统代理
sleep(2)
dlg["系统代理"].click_input()

# 创建桌面快捷方式
sleep(2)
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
shortcut_path = os.path.join(desktop, "NekoBox.lnk")
shell = win32com.client.Dispatch("WScript.Shell")
shortcut = shell.CreateShortCut(shortcut_path)
shortcut.Targetpath = nekobox_exe_path
shortcut.WorkingDirectory = os.path.dirname(nekobox_exe_path)
shortcut.save()

# 打开浏览器访问https://www.google.com
sleep(2)
webbrowser.open("https://www.google.com.hk/search?q=nekoBox&newwindow=1&sca_esv=84558b4239d0d7dc&sxsrf=AHTn8zqOVZkWiUB0UD4J6yHoZww-wGTq5g%3A1743498263127&ei=F6zrZ5a-B56k2roPr7ffmAU")

