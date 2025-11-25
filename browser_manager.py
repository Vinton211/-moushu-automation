#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
浏览器管理器，负责浏览器的初始化和管理
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import psutil
import os
import time

class BrowserManager:
    """浏览器管理器类"""
    
    def __init__(self, headless=False, driver_path='./chromedriver.exe', reuse_browser=False):
        """
        初始化浏览器管理器
        
        Args:
            headless: 是否使用无头模式
            driver_path: ChromeDriver的路径
            reuse_browser: 是否尝试复用已打开的浏览器实例
        """
        self.headless = headless
        self.driver_path = driver_path
        self.reuse_browser = reuse_browser
        self.driver = None
        self.wait = None
        self.debug_port = 9222  # Chrome远程调试端口
    
    def initialize_browser(self):
        """初始化浏览器，尝试复用已打开的实例"""
        # 配置Chrome选项
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument('--headless')  # 无头模式
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        chrome_options.add_argument('--user-data-dir=' + os.path.join(os.getcwd(), 'chrome_profile'))  # 使用自定义配置文件
        chrome_options.add_argument('--remote-debugging-port=' + str(self.debug_port))  # 始终添加远程调试端口
        
        # 尝试复用已打开的浏览器实例
        if self.reuse_browser:
            try:
                print("正在尝试复用已打开的浏览器实例...")
                # 检查是否有Chrome进程正在运行，并且监听了我们的调试端口
                chrome_processes = []
                for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                    if proc.info['name'] in ['chrome.exe', 'chrome']:
                        cmdline = proc.info.get('cmdline', [])
                        # 检查命令行参数中是否包含我们的调试端口
                        if any(f'--remote-debugging-port={self.debug_port}' in arg for arg in cmdline):
                            chrome_processes.append(proc)
                
                if chrome_processes:
                    # 设置debuggerAddress选项连接到已打开的Chrome实例
                    chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{self.debug_port}")
                    
                    # 使用debuggerAddress连接已打开的浏览器
                    self.driver = webdriver.Chrome(service=Service(self.driver_path), options=chrome_options)
                    self.wait = WebDriverWait(self.driver, 10)  # 显式等待10秒
                    print("成功复用已打开的浏览器实例！")
                    return self.driver, self.wait
                else:
                    print("未找到运行中的Chrome进程（或未监听指定端口），将创建新的浏览器实例...")
            except Exception as e:
                print(f"复用浏览器实例失败: {e}")
                print("将创建新的浏览器实例...")
        
        # 创建新的浏览器实例
        service = Service(self.driver_path)
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)  # 显式等待10秒
        print("已创建新的浏览器实例")
        
        return self.driver, self.wait
    
    def close_browser(self):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()
            self.driver = None
            self.wait = None
    
    def get_driver(self):
        """获取浏览器驱动"""
        return self.driver
    
    def get_wait(self):
        """获取显式等待对象"""
        return self.wait
