#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import openpyxl

# 打开Excel文件
file_path = './xiaohongshu_content.xlsx'
wb = openpyxl.load_workbook(file_path)
sheet = wb.active

# 打印表头
print('表头:', [cell.value for cell in sheet[1]])

# 打印前5行数据
print('前5行数据:')
for row in sheet.iter_rows(min_row=1, max_row=6, values_only=True):
    print(row)

# 关闭工作簿
wb.close()
