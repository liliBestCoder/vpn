from time import sleep

import requests
import os
import json  # 新增: 导入json库
import zipfile  # 导入zipfile库
import tkinter as tk
from tkinter import simpledialog
import subprocess  # 新增: 导入subprocess库
# 新增: 导入pywinauto库
import pywinauto
# 新增: 导入webbrowser库
import webbrowser
# 新增: 导入win32com.client库
import winshell
from win32com.client import Dispatch
# 新增: 导入tqdm库
from tqdm import tqdm
import sys
import threading
import time

def show_floating_tip(message, duration=5):
    def run_tip():
        root = tk.Tk()
        root.overrideredirect(True)  # 去除窗口边框
        root.attributes("-topmost", True)  # 置顶
        root.attributes("-alpha", 0.9)  # 设置透明度

        # 设置标签
        label = tk.Label(root, text=message, bg="#444", fg="white", font=("Segoe UI", 30), padx=10, pady=5)
        label.pack()

        # 获取屏幕尺寸 & 计算窗口位置（右下角）
        root.update_idletasks()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = label.winfo_reqwidth()
        window_height = label.winfo_reqheight()

        x = screen_width - window_width - 20
        y = screen_height - window_height - 50
        root.geometry(f"+{x}+{y}")

        # 设置定时关闭
        def close_after_delay():
            time.sleep(duration)
            root.destroy()

        threading.Thread(target=close_after_delay, daemon=True).start()
        root.mainloop()

    threading.Thread(target=run_tip, daemon=True).start()

def download_file(url, target_file, total_size):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        block_size = 1024  # 减少每次更新的数据块大小

        # 强制指定输出流 + 动态刷新
        output_stream = sys.stdout if sys.stdout else sys.stderr
        progress_bar = tqdm(
            total=total_size,  # 确保total_size参数正确传递
            unit='B',  # 修改: 将unit参数设置为'B'
            unit_scale=True,
            file=output_stream,
            dynamic_ncols=True,
            leave=True,
            unit_divisor=1024,
            bar_format='{l_bar}{bar:60}{r_bar}'  # 指定进度条宽度为20
        )

        with open(target_file, 'wb') as f:
            for data in response.iter_content(block_size):
                f.write(data)
                progress_bar.update(len(data))
        progress_bar.close()
    except requests.exceptions.RequestException as e:
        print(f"下载失败: {e}")
        exit(1)

def download_and_merge_files(urls, target_files, file_sizes, merged_file):
    for url, target_file, total_size in zip(urls, target_files, file_sizes):
        download_file(url, target_file, total_size)
    
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

def create_shortcut(name, target, icon=None):
    desktop = winshell.desktop()
    shortcut_path = os.path.join(desktop, f"{name}.lnk")

    shell = Dispatch("WScript.Shell")
    shortcut = shell.CreateShortcut(shortcut_path)

    shortcut.TargetPath = os.path.abspath(target)
    shortcut.WorkingDirectory = os.path.dirname(os.path.abspath(target))

    if icon:
        shortcut.IconLocation = icon
    else:
        shortcut.IconLocation = os.path.abspath(target)

    shortcut.save()

urls = [
    "https://gcore.jsdelivr.net/gh/liliBestCoder/vpn/binary/nekoray.zip.001",
    "https://gcore.jsdelivr.net/gh/liliBestCoder/vpn/binary/nekoray.zip.002",
    "https://gcore.jsdelivr.net/gh/liliBestCoder/vpn/binary/nekoray.zip.003"
]
target_files = ["nekoray.zip.001", "nekoray.zip.002", "nekoray.zip.003"]
file_sizes = [18.0 * 1024 * 1024, 18.0 * 1024 * 1024, 3.97 * 1024 * 1024]  # 文件大小列表，单位为字节
merged_file = "nekoray.zip"


print("============自动安装配置总共需要11步，请耐心等待配置完成，配置过程中请勿操作电脑。=================")
print("==================================1.下载nekoray.zip================================================")
download_and_merge_files(urls, target_files, file_sizes, merged_file)  # 修改: 传递文件大小列表
print("==================================2.解压缩nekoray.zip==============================================")
unzip_file(merged_file)  # 解压缩合并后的文件到当前目录
print("==================================3.配置分组=======================================================")
# 新增: 获取用户输入的订阅链接
subscription_link = get_subscription_link()

# 新增: 直接写入JSON文件
group_file_path = "nekoray/config/groups/1.json"
group_dir = os.path.dirname(group_file_path)
if not os.path.exists(group_dir):
    os.makedirs(group_dir)

group_data = {
    "archive": False,
    "column_width": [150, 150, 233, 150, 150],
    "front_proxy_id": -1,
    "id": 1,
    "lastup": 1743427857,
    "manually_column_width": True,
    "name": "免费订阅",
    "order": [],
    "skip_auto_update": False,
    "url": subscription_link
}
with open(group_file_path, 'w', encoding='utf-8') as file:
    json.dump(group_data, file, ensure_ascii=False, indent=4)

# 新增: 写入pm.json文件
pm_file_path = "nekoray/config/groups/pm.json"
pm_data = {
    "groups": [
        1
    ]
}
with open(pm_file_path, 'w', encoding='utf-8') as file:
    json.dump(pm_data, file, ensure_ascii=False, indent=4)

# 新增: 写入nekobox.json文件
nekobox_file_path = "nekoray/config/groups/nekobox.json"
nekobox_data = {
    "active_routing": "Default",
    "check_include_pre": False,
    "conn_stat": False,
    "core_box_clash_api": -9090,
    "current_group": 1,
    "custom_inbound": "{\"inbounds\": []}",
    "custom_route": "{\"rules\": []}",
    "extraCore": {
        "core_map": "{\"hysteria2\":\"\",\"naive\":\"\",\"tuic\":\"\"}"
    },
    "fakedns": False,
    "inbound_address": "0.0.0.0",
    "inbound_auth": {},
    "inbound_socks_port": 2080,
    "language": 0,
    "log_ignore": [],
    "log_level": "info",
    "max_log_line": 200,
    "mux_concurrency": 8,
    "mux_default_on": False,
    "mux_padding": False,
    "mux_protocol": "h2mux",
    "mw_size": "800x600",
    "remember_enable": False,
    "remember_id": -1919,
    "skip_cert": False,
    "splitter_state": "AAAA/wAAAAEAAAACAAAA9QAAAPUB/////wEAAAACAA==",
    "spmode2": [],
    "start_minimal": False,
    "sub_auto_update": 1440,
    "sub_clear": False,
    "sub_insecure": False,
    "sub_use_proxy": False,
    "test_concurrent": 5,
    "test_dl_timeout": 30,
    "test_url": "http://cp.cloudflare.com/",
    "test_url_dl": "http://cachefly.cachefly.net/10mb.test",
    "theme": "0",
    "traffic_loop_interval": 1000,
    "vpn_hide_console": True,
    "vpn_impl": 0,
    "vpn_internal_tun": True,
    "vpn_ipv6": False,
    "vpn_mtu": 9000,
    "vpn_rule_white": False,
    "vpn_strict_route": False
}
with open(nekobox_file_path, 'w', encoding='utf-8') as file:
    json.dump(nekobox_data, file, ensure_ascii=False, indent=4)

print("==================================4.配置路由======================================================")
show_floating_tip('正在配置路由...', duration=15)

# 新增: 写入Default.json文件
default_file_path = "nekoray/config/routes_box/Default.json"
default_dir = os.path.dirname(default_file_path)
if not os.path.exists(default_dir):
    os.makedirs(default_dir)

default_data = {
    "block_domain": "geosite:category-ads-all\ndomain:appcenter.ms\ndomain:firebase.io\ndomain:crashlytics.com",
    "custom": "{\"rules\": []}",
    "def_outbound": "proxy",
    "direct_dns": "https://doh.pub/dns-query",
    "direct_domain": "geosite:cn",
    "direct_ip": "geoip:cn\ngeoip:private",
    "dns_final_out": "proxy",
    "dns_routing": True,
    "remote_dns": "https://dns.google/dns-query",
    "sniffing_mode": 1,
    "use_dns_object": False
}
with open(default_file_path, 'w', encoding='utf-8') as file:
    json.dump(default_data, file, ensure_ascii=False, indent=4)

# 启动进程
nekobox_exe_path = "nekoray/nekobox.exe"
subprocess.Popen([nekobox_exe_path])

# 更新订阅
sleep(5)
app = pywinauto.Application(backend="uia").connect(path=nekobox_exe_path)
dlg = app.window(title_re=".*NekoBox.*")

show_floating_tip('正在更新订阅...勿动', duration=15)
print("==================================5.更新订阅=======================================================")
dlg.type_keys("^U")

# url test
show_floating_tip('正在URL Test...勿动', duration=15)
sleep(5)
print("==================================6.URL Test测试=====================================================")
dlg.type_keys("^%U")

# 按延迟排序
show_floating_tip('正在按延迟排序...勿动', duration=60)
print("==================================7.按延迟排序======================================================")
sleep(60)
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
show_floating_tip('正在启动服务器...勿动', duration=15)
print("==================================8.启动服务器======================================================")
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
print("==================================9.开启系统代理======================================================")
show_floating_tip('正在开启系统代理...勿动', duration=15)
dlg["系统代理"].click_input()

# 创建桌面快捷方式
sleep(2)
print("==================================10.创建桌面快捷方式===================================================")
show_floating_tip('正在创建桌面快捷方式...勿动', duration=15)
create_shortcut(
    name="NekoBox",
    target=nekobox_exe_path  # 把这个替换为你的实际路径
)

# 打开浏览器访问https://www.google.com
sleep(2)
print("==================================11.打开浏览器，尝试访问谷歌===============================================")
show_floating_tip('配置已完成, 正在尝试访问谷歌...', duration=15)
webbrowser.open("https://www.google.com.hk/search?q=nekoBox&newwindow=1&sca_esv=84558b4239d0d7dc&sxsrf=AHTn8zqOVZkWiUB0UD4J6yHoZww-wGTq5g%3A1743498263127&ei=F6zrZ5a-B56k2roPr7ffmAU")


# 新增: 脚本执行完毕后自动退出命令窗口
os._exit(0)