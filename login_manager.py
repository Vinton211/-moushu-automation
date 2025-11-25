#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
登录管理器，负责登录相关功能
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

class LoginManager:
    """登录管理器类"""
    
    def __init__(self, driver, wait, popup_handler):
        """
        初始化登录管理器
        
        Args:
            driver: 浏览器驱动
            wait: 显式等待对象
            popup_handler: 弹窗处理器
        """
        self.driver = driver
        self.wait = wait
        self.popup_handler = popup_handler
    
    def open_xiaohongshu(self, is_creator=False):
        """
        打开小红书创作者服务平台
        
        Args:
            is_creator: 是否打开创作服务平台（默认False，此处仅用于兼容接口）
        """
        # 只打开创作者服务平台
        url = "https://creator.xiaohongshu.com/"
        print(f"正在打开小红书创作服务平台: {url}")
        self.driver.get(url)
        # 处理弹窗
        self.popup_handler.handle_popups()
    
    def login(self, phone_number=None, password=None, is_creator=False, use_verification_code=True):
        """
        登录小红书创作者服务平台
        
        Args:
            phone_number: 手机号（可选，若不提供则使用默认值188********）
            password: 密码（可选，此处仅用于兼容接口）
            is_creator: 是否是创作服务平台登录（默认False，此处仅用于兼容接口）
            use_verification_code: 是否使用验证码登录（默认True）
        
        Returns:
            bool: 登录是否成功
        """
        try:
            # 处理弹窗
            self.popup_handler.handle_popups()
            
            # 设置默认手机号
            if phone_number is None:
                phone_number = "188********"
            
            # 输入手机号 - 使用更通用的定位方式
            try:
                phone_input = None
                # 尝试1: 精确CSS选择器
                try:
                    phone_input = self.wait.until(EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "input[placeholder='手机号'].css-19z0sa3.css-nt440g.dyn")
                    ))
                except:
                    # 尝试2: 仅使用placeholder
                    phone_input = self.wait.until(EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "input[placeholder='手机号']")
                    ))
                
                phone_input.clear()
                # 输入手机号
                for char in phone_number:
                    phone_input.send_keys(char)
                    time.sleep(0.1)  # 模拟人工输入
                print(f"已输入手机号: {phone_number}")
            except Exception as e:
                print(f"输入手机号失败: {e}")
                return False
            
            # 点击发送验证码按钮 - 使用多种定位方式
            try:
                send_code_button = None
                # 尝试1: 原始XPATH
                try:
                    send_code_button = self.wait.until(EC.element_to_be_clickable(
                        (By.XPATH, "//div[contains(@class, 'css-1vfl29') and text()='发送验证码']")
                    ))
                except:
                    # 尝试2: 仅使用文本
                    try:
                        send_code_button = self.wait.until(EC.element_to_be_clickable(
                            (By.XPATH, "//*[contains(text(), '发送验证码')]")))
                    except:
                        # 尝试3: CSS选择器
                        send_code_button = self.wait.until(EC.element_to_be_clickable(
                            (By.CSS_SELECTOR, ".send-code-btn")))
                
                send_code_button.click()
                print("已点击发送验证码按钮")
                # 等待验证码发送成功（可能需要处理弹窗）
                self.popup_handler.handle_popups()
            except Exception as e:
                print(f"点击发送验证码按钮失败: {e}")
                return False
            
            # 等待用户输入验证码
            code = input("请输入收到的验证码: ").strip()
            
            # 输入验证码 - 使用更通用的定位方式
            try:
                code_input = None
                # 尝试1: 精确CSS选择器（原始）
                try:
                    code_input = self.wait.until(EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "input[placeholder='验证码'].css-19z0sa3.css-1ge5flv.dyn")
                    ))
                except:
                    # 尝试2: 另一精确CSS选择器
                    try:
                        code_input = self.wait.until(EC.presence_of_element_located(
                            (By.CSS_SELECTOR, "input[placeholder='验证码'].css-19z0sa3.css-nt440g.dyn")
                        ))
                    except:
                        # 尝试3: 仅使用placeholder
                        code_input = self.wait.until(EC.presence_of_element_located(
                            (By.CSS_SELECTOR, "input[placeholder='验证码']")
                        ))
                
                code_input.clear()
                code_input.send_keys(code)
                print("已输入验证码")
            except Exception as e:
                print(f"输入验证码失败: {e}")
                return False
            
            # 点击登录按钮 - 使用更通用的定位方式
            try:
                login_confirm_button = None
                # 尝试1: 原始精确CSS选择器
                try:
                    login_confirm_button = self.wait.until(EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, "button.css-1jgt0wa.css-y4h4ay.dyn.beer-login-btn")
                    ))
                except:
                    # 尝试2: 提交按钮type
                    try:
                        login_confirm_button = self.wait.until(EC.element_to_be_clickable(
                            (By.CSS_SELECTOR, "button[type='submit']")
                        ))
                    except:
                        # 尝试3: 精确CSS选择器备选
                        try:
                            login_confirm_button = self.wait.until(EC.element_to_be_clickable(
                                (By.CSS_SELECTOR, "button.css-1525zvt.css-q63c9r.dyn")
                            ))
                        except:
                            # 尝试4: 原始XPATH定位
                            login_confirm_button = self.wait.until(EC.element_to_be_clickable(
                                (By.XPATH, "//button[.//span[contains(text(), '登录')]]")
                            ))
                
                login_confirm_button.click()
                print("已点击登录确认按钮")
                # 等待页面加载
                time.sleep(2)
            except Exception as e:
                print(f"点击登录确认按钮失败: {e}")
                return False
            
            # 处理弹窗
            self.popup_handler.handle_popups()
            
            # 等待页面加载，检查登录状态
            time.sleep(5)
            
            # 检查登录是否成功
            if self._check_login_status():
                print("登录成功！")
                return True
            else:
                print("登录失败！")
                return False
        except Exception as e:
            print(f"登录过程中发生错误: {e}")
            return False
    
    def _check_login_status(self):
        """
        检查登录状态
        
        Returns:
            bool: 登录是否成功
        """
        try:
            # 创作者服务平台登录状态检查
            current_url = self.driver.current_url
            print(f"当前URL: {current_url}")
            
            # 检查是否在创作者服务平台
            if "creator.xiaohongshu.com" in current_url:
                # 检查是否已登录（如果URL包含dashboard或没有login相关内容）
                if "login" not in current_url:
                    return True
            
            # 尝试刷新页面，再次检查
            self.driver.refresh()
            time.sleep(3)
            current_url = self.driver.current_url
            if "creator.xiaohongshu.com" in current_url and ("login" not in current_url):
                return True
            
            return False
        except Exception as e:
            print(f"检查登录状态失败: {e}")
            return False
