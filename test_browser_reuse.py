#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试浏览器复用功能的简单脚本
"""

from browser_manager import BrowserManager
from login_manager import LoginManager
from popup_handler import PopupHandler
import time

def test_browser_reuse():
    """测试浏览器复用功能"""
    print("=== 测试浏览器复用功能 ===")
    
    # 创建浏览器管理器，开启浏览器复用
    browser_manager = BrowserManager(reuse_browser=True)
    
    # 初始化浏览器
    driver, wait = browser_manager.initialize_browser()
    
    # 初始化其他组件
    popup_handler = PopupHandler(driver, wait)
    login_manager = LoginManager(driver, wait, popup_handler)
    
    # 打开小红书创作服务平台
    login_manager.open_xiaohongshu(is_creator=True)
    
    # 检查登录状态
    print("\n检查登录状态...")
    is_logged_in = login_manager._check_login_status()
    
    if is_logged_in:
        print("✅ 用户已登录，将跳过登录流程")
    else:
        print("❌ 用户未登录，需要执行登录流程")
    
    # 保持浏览器打开，等待用户操作
    print("\n浏览器将保持打开状态，您可以手动操作")
    print("按 Enter 键关闭浏览器...")
    input()
    
    # 关闭浏览器
    browser_manager.close_browser()
    print("浏览器已关闭")

if __name__ == "__main__":
    test_browser_reuse()