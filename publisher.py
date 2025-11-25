#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
发布器，负责内容发布功能
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

class Publisher:
    """发布器类"""
    
    def __init__(self, driver, wait, popup_handler):
        """
        初始化发布器
        
        Args:
            driver: 浏览器驱动
            wait: 显式等待对象
            popup_handler: 弹窗处理器
        """
        self.driver = driver
        self.wait = wait
        self.popup_handler = popup_handler
    
    def publish_note(self, note_data):
        """
        发布笔记
        
        Args:
            note_data: 笔记数据，包含标题、内容、图片路径等
        
        Returns:
            bool: 发布是否成功
        """
        try:
            # # 处理弹窗
            # self.popup_handler.handle_popups()
            
            # 检查当前URL，判断是否为创作服务平台
            # current_url = self.driver.current_url
            # is_creator_platform = "creator.xiaohongshu.com" in current_url
            
            # if is_creator_platform:
            #     # 创作服务平台发布流程
            print("使用创作服务平台发布笔记")
            # 跳转到发布图文页面
            self.driver.get("https://creator.xiaohongshu.com/publish/publish?from=menu&target=image")
            time.sleep(3)  # 等待页面加载
            
            # # 处理弹窗
            # self.popup_handler.handle_popups()
            
            # 添加上传图片
            self._add_images(note_data.get('image_paths'))
            
            # 输入标题
            if note_data.get('title'):
                self._input_title(note_data['title'])
            
            # 输入正文内容
            if note_data.get('content'):
                self._input_content(note_data['content'])
            
            # # 选择话题标签
            # if note_data.get('tags'):
            #     self._add_tags(note_data['tags'])
            
            # # 选择分类
            # if note_data.get('category'):
            #     self._select_category(note_data['category'])
            
            # 点击发布按钮
            self._click_publish_button()
            time.sleep(2)  # 等待发布完成
            # # 检查发布结果
            # return self._check_publish_result()
        except Exception as e:
            print(f"发布笔记过程中发生错误: {e}")
            return False
    
    def _input_title(self, title):
        """
        输入标题
        
        Args:
            title: 笔记标题
        """
        try:
            # 过滤掉非BMP字符
            filtered_title = self._filter_non_bmp(title)
            
            # 查找标题输入框
            title_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.title-input[placeholder*='标题']")))
            title_input.clear()
            title_input.send_keys(filtered_title)
            print(f"已输入标题: {filtered_title}")
        except Exception as e:
            print(f"输入标题失败: {e}")
    
    def _filter_non_bmp(self, text):
        """
        过滤掉非BMP字符，只保留BMP字符
        
        Args:
            text: 原始文本
        
        Returns:
            str: 只包含BMP字符的文本
        """
        return ''.join(c for c in text if ord(c) <= 0xFFFF)
    
    def _input_content(self, content):
        """
        输入正文内容
        
        Args:
            content: 笔记正文内容
        """
        try:
            # 过滤掉非BMP字符
            filtered_content = self._filter_non_bmp(content)
            
            # 查找正文输入框，使用更精准的CSS选择器匹配contenteditable div元素
            content_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.tiptap.ProseMirror[contenteditable='true'][role='textbox']")))
            
            # 使用JavaScript设置内容，避免send_keys的字符限制问题
            self.driver.execute_script("arguments[0].innerHTML = '';", content_input)
            time.sleep(1)
            self.driver.execute_script("arguments[0].textContent = arguments[1];", content_input, filtered_content)
            print(f"已输入正文内容")
        except Exception as e:
            print(f"输入正文内容失败: {e}")
            # 增加更详细的错误信息
            import traceback
            traceback.print_exc()
    
    def _add_tags(self, tags):
        """
        选择话题标签
        
        Args:
            tags: 标签列表
        """
        try:
            # 查找标签输入框
            tag_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='tags'], .tag-input")))
            
            for tag in tags:
                tag_input.send_keys(tag)
                tag_input.send_keys(" ")  # 发送空格，触发标签添加
                print(f"已添加标签: {tag}")
                time.sleep(1)  # 等待标签添加
        except Exception as e:
            print(f"添加标签失败: {e}")
    
    def _select_category(self, category):
        """
        选择分类
        
        Args:
            category: 分类名称
        """
        try:
            # 查找分类选择器
            category_selector = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".category-selector")))
            category_selector.click()
            
            # 查找并点击分类选项
            category_option = self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[contains(text(), '{category}')]")))
            category_option.click()
            print(f"已选择分类: {category}")
        except Exception as e:
            print(f"选择分类失败: {e}")
    
    def _click_publish_button(self):
        """
        点击发布按钮
        """
        try:
            # 使用精确的CSS选择器查找发布按钮
            publish_button = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.d-button.d-button-large.--size-icon-large.--size-text-h6.d-button-with-content.--color-static.bold.--color-bg-fill.--color-text-paragraph.custom-button.red.publishBtn[type='button']")))
            publish_button.click()
            print("已点击发布按钮")
        except Exception as e:
            print(f"点击发布按钮失败: {e}")
    
    def _check_publish_result(self):
        """
        检查发布结果
        
        Returns:
            bool: 发布是否成功
        """
        try:
            # 等待发布结果
            time.sleep(10)
            
            # 检查当前URL，判断是否发布成功
            current_url = self.driver.current_url
            print(f"发布后URL: {current_url}")
            
            if "published" in current_url or "success" in current_url.lower() or "dashboard" in current_url:
                print("发布成功！")
                return True
            else:
                # 检查页面中是否有发布成功的提示
                try:
                    success_message = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), '发布成功') or contains(text(), 'Published successfully')]")))
                    if success_message:
                        print("发布成功！")
                        return True
                except Exception as e:
                    print(f"未找到发布成功提示: {e}")
            
            print("发布失败！")
            return False
        except Exception as e:
            print(f"检查发布结果失败: {e}")
            return False
    
    def _add_images(self, image_paths):
        """
        添加上传图片
        
        Args:
            image_paths: 图片路径列表（如果提供则使用，否则随机生成）
        """
        try:
            print("开始处理图片上传...")
            
            # 尝试多种方式定位和处理图片上传
            file_input = None
            upload_success = False
            
            try:
                # 方式1：直接查找文件上传输入框
                print("尝试直接查找文件上传输入框...")
                file_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.upload-input[type='file']")))
                print("成功找到文件上传输入框")
            except Exception as e1:
                print(f"直接查找文件上传输入框失败: {e1}")
                
                # 方式2：先点击上传区域，再查找文件上传输入框
                try:
                    print("尝试先点击上传区域...")
                    upload_area = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".upload-area")))
                    upload_area.click()
                    print("成功点击上传区域")
                    time.sleep(1)  # 等待上传区域展开
                    
                    # 再次尝试查找文件上传输入框
                    file_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']")))
                    print("点击上传区域后成功找到文件上传输入框")
                except Exception as e2:
                    print(f"点击上传区域后查找文件上传输入框失败: {e2}")
                    
                    # 方式3：尝试使用其他常见的文件上传输入框选择器
                    try:
                        print("尝试使用其他常见选择器查找文件上传输入框...")
                        file_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']")))
                        print("使用通用选择器成功找到文件上传输入框")
                    except Exception as e3:
                        print(f"所有尝试都失败了，无法找到文件上传输入框: {e3}")
                        # 不再抛出异常，允许继续执行
                        return
            
            if image_paths:
                # 为每个图片路径发送文件路径
                for image_path in image_paths:
                    try:
                        print(f"准备上传图片: {image_path}")
                        file_input.send_keys(image_path)
                        print(f"已添加图片: {image_path}")
                        time.sleep(3)  # 增加等待时间，确保图片上传完成
                        upload_success = True
                    except Exception as e:
                        print(f"上传图片 {image_path} 失败: {e}")
                        # 继续尝试上传下一张图片
                        continue
            else:
                # 从网络随机生成图片并上传
                print("没有提供图片路径，将使用随机生成的图片")
                
                # 由于Selenium无法直接处理网络图片上传，我们可以使用第三方API获取随机图片
                import urllib.request
                import tempfile
                import os
                
                # 生成2张随机图片，增加重试机制
                for i in range(2):
                    retry_count = 0
                    max_retries = 3
                    success = False
                    
                    while retry_count < max_retries and not success:
                        try:
                            # 生成1024x1024的随机图片
                            image_url = f"https://picsum.photos/1024/1024?random={i}_{retry_count}"
                            
                            # 下载图片到临时文件
                            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
                                temp_path = temp_file.name
                            
                            print(f"尝试下载随机图片 {i+1} (重试 {retry_count+1}/{max_retries}): {image_url}")
                            urllib.request.urlretrieve(image_url, temp_path)
                            print(f"已下载随机图片: {image_url} 到临时文件: {temp_path}")
                            
                            # 上传图片
                            file_input.send_keys(temp_path)
                            print(f"已上传随机图片 {i+1}")
                            time.sleep(4)  # 增加等待时间，确保图片上传完成
                            
                            # 删除临时文件
                            os.unlink(temp_path)
                            print(f"已删除临时文件: {temp_path}")
                            
                            success = True
                            upload_success = True
                            break
                        except urllib.error.HTTPError as e:
                            print(f"下载图片时出现HTTP错误: {e}")
                            retry_count += 1
                            time.sleep(2)  # 等待2秒后重试
                        except Exception as e:
                            print(f"处理随机图片时出现错误: {e}")
                            break
                    
                    if not success:
                        print(f"无法下载随机图片 {i+1}")
            
            if upload_success:
                print("图片上传处理完成")
            else:
                print("图片上传失败，但将继续执行后续步骤")
        except Exception as e:
            print(f"添加上传图片失败: {e}")
            # 增加更详细的错误信息
            import traceback
            traceback.print_exc()
            # 不抛出异常，允许继续执行后续步骤
    
    def _add_random_image(self, max_images=9):
        """
        添加随机图片（备用方法）
        
        Args:
            max_images: 最大添加图片数量
        """
        try:
            # 查找图片上传区域
            upload_area = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".upload-area")))
            upload_area.click()
            print("已点击图片上传区域")
        except Exception as e:
            print(f"点击图片上传区域失败: {e}")
