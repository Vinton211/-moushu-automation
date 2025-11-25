#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
弹窗处理器，负责处理各种弹窗
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class PopupHandler:
    """弹窗处理器类"""
    
    def __init__(self, driver, wait):
        """
        初始化弹窗处理器
        
        Args:
            driver: 浏览器驱动
            wait: 显式等待对象
        """
        self.driver = driver
        self.wait = wait
    
    def handle_popups(self):
        """处理各种弹窗"""
        popup_selectors = [
            (".dialog-close", By.CSS_SELECTOR),
            (".xhs-icon--close", By.CSS_SELECTOR),
            (".close-btn", By.CSS_SELECTOR),
            ("//div[@class='dialog']//button[contains(@class, 'close')]", By.XPATH),
            ("//button[text()='关闭']", By.XPATH),
            ("//button[text()='取消']", By.XPATH),
            (".modal-close", By.CSS_SELECTOR),
            (".xhs-modal-close", By.CSS_SELECTOR),
            ("#close-btn", By.ID)
        ]
        
        # 延迟1秒，确保弹窗已经加载
        import time
        time.sleep(1)
        
        for selector, by_type in popup_selectors:
            try:
                # 尝试查找并点击弹窗关闭按钮
                element = self.wait.until(EC.element_to_be_clickable((by_type, selector)))
                element.click()
                print(f"已关闭弹窗: {selector}")
                time.sleep(0.5)  # 等待一下，确保弹窗关闭
            except Exception as e:
                # 忽略单个弹窗处理失败，继续尝试其他选择器
                pass
    
    def accept_all_cookies(self):
        """接受所有 cookies"""
        try:
            # 等待并点击同意所有 cookies 按钮
            accept_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".cookie-accept-all")))
            accept_button.click()
            print("已接受所有 cookies")
        except Exception as e:
            print(f"没有找到或点击同意 cookies 按钮失败: {e}")
