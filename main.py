#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import traceback
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

def simulate_click(driver, element):
    """利用 JS 模拟点击事件"""
    driver.execute_script("""
        var evt = new MouseEvent('click', {
            bubbles: true,
            cancelable: true,
            view: window
        });
        arguments[0].dispatchEvent(evt);
        """, element)

def main():
    # 初始化 ChromeDriver
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # 1. 登录流程
        login_url = "https://www40.polyu.edu.hk/poss/secure/login/loginhome.do"
        driver.get(login_url)
        time.sleep(2)
        
        driver.find_element(By.NAME, "j_username").send_keys(" ")  # 替换为真实用户名
        driver.find_element(By.NAME, "j_password").send_keys(" ")  # 替换为真实密码
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        WebDriverWait(driver, 10).until(lambda d: "secure/home.do" in d.current_url)
        print("✅ Login successful!")
        
        # 2. 进入工作页
        job_url = "https://www40.polyu.edu.hk/capspjb/secure/welcome.do"
        driver.get(job_url)
        time.sleep(2)
        
        # 3. 等待 Disclaimer 弹窗出现，并点击对应复选框
        disclaimer_container = WebDriverWait(driver, 15).until(
            lambda d: d.find_element(By.XPATH, "//*[contains(text(), 'I have read and agreed')]")
        )
        print("Disclaimer popup appeared!")
        
        # 如果弹窗在 iframe 内，请取消下面代码的注释：
        # iframes = driver.find_elements(By.TAG_NAME, "iframe")
        # if iframes:
        #     driver.switch_to.frame(iframes[0])
        
        # 4. 点击两个 checkbox
        checkboxes = WebDriverWait(driver, 10).until(
            lambda d: d.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
        )
        if len(checkboxes) >= 2:
            actions = ActionChains(driver)
            actions.move_to_element(checkboxes[0]).click(checkboxes[0]).perform()
            time.sleep(0.1)
            actions.move_to_element(checkboxes[1]).click(checkboxes[1]).perform()
            time.sleep(0.1)
            print("✔️ Clicked both checkboxes.")
        else:
            print("未找到足够的 checkbox 元素！")
            return
        
        # 5. 点击“Continue”按钮
        continue_button = WebDriverWait(driver, 10).until(
            lambda d: d.find_element(By.XPATH, "//*[contains(text(),'Continue to access PolyU Job Board')]/ancestor::button[not(@disabled)]")
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", continue_button)
        time.sleep(0.5)
        continue_button.click()
        print("✔️ Clicked the continue button.")
        
        # 6. 定义保存职位数据的列表，并初始化当前页码和全局计数器
        job_data_list = []
        page_number = 1
        page_limit = 5000  # 测试仅抓取前 
        job_counter = 0  # 全局计数器，从 0 开始
        
        while page_number <= page_limit:
            print(f"======== 正在抓取第 {page_number} 页的职位 ========")
            # 等待当前页面职位加载完成（每页约有20个职位）
            WebDriverWait(driver, 15).until(
                lambda d: len(d.find_elements(By.XPATH, "//button[@role='tab' and contains(., 'Ref:')]")) > 0
            )
    
            # 使用 while 循环，每次重新查询当前页面的职位按钮列表
            job_index = 0
            while True:
                current_jobs = driver.find_elements(By.XPATH, "//button[@role='tab' and contains(., 'Ref:')]")
                if job_index >= len(current_jobs):
                    break
                
                job = current_jobs[job_index]
                simulate_click(driver, job)
                time.sleep(0)  # 根据网页反应速度适当调整等待时间
                
                job_counter += 1
                
                # 从职位按钮内部提取公司、职位和招聘编号
                p_tags = job.find_elements(By.TAG_NAME, "p")
                if len(p_tags) >= 3:
                    company = p_tags[0].text.strip()
                    position = p_tags[1].text.strip()
                    ref_text = p_tags[2].text.strip()
                    ref_no = ref_text.replace("Ref:", "").strip()
                else:
                    company = position = ref_no = ""
                
                # 利用 JavaScript XPath 提取发布时间和截止日期
                posted_date = ""
                closing_date = ""
                try:
                    posted_date = driver.execute_script(
                        "return document.evaluate('string(.//ul/li[1]/span/span/text()[2])', arguments[0], null, XPathResult.STRING_TYPE, null).stringValue;",
                        job)
                    closing_date = driver.execute_script(
                        "return document.evaluate('string(.//ul/li[2]/span/span/text()[2])', arguments[0], null, XPathResult.STRING_TYPE, null).stringValue;",
                        job)
                except Exception:
                    print(f"第 {job_counter} 个职位未能找到时间信息。")
                
                # 提取薪资信息
                salary = ""
                try:
                    salary = job.find_element(By.XPATH, ".//ul/li[3]/span").text.strip()
                except Exception:
                    print(f"第 {job_counter} 个职位未能找到薪资信息。")
                
                # 【新增】提取类型信息
                job_type = ""
                try:
                    job_type = driver.find_element(By.XPATH, "/html/body/div/div/main/div/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div/div/span").text.strip()
                except Exception:
                    print(f"第 {job_counter} 个职位未能找到类型信息。")
                
                # 额外抓取工作详情（直接抓取 innerHTML，不做转换）
                job_details_html = ""
                details_elements = driver.find_elements(By.XPATH, "/html/body/div/div/main/div/div[2]/div[2]/div")
                if details_elements:
                    job_details_html = details_elements[0].get_attribute("innerHTML").strip()
                else:
                    print(f"第 {job_counter} 个职位没有找到工作详情的 HTML 信息。")
                
                # 将抓取的职位数据添加到列表中
                job_data_list.append({
                    "序号": job_counter,
                    "公司名": company,
                    "职位": position,
                    "招聘编号": ref_no,
                    "发布时间": posted_date,
                    "截止日期": closing_date,
                    "薪资": salary,
                    "类型": job_type,
                    "工作详情(HTML)": job_details_html
                })
                print(f"已抓取第 {job_counter} 个职位。")
                
                job_index += 1  # 继续处理下一个职位
    
            # 检查是否已达到预设页数
            if page_number >= page_limit:
                print(f"已抓取 {page_limit} 页，测试结束。")
                break
            
            # 7. 尝试点击下一页（假设分页栏按钮的 title 属性为 "Page {页码}"）
            try:
                next_page_button = driver.find_element(
                    By.XPATH, f"//span[@title='Page {page_number + 1}']/button[not(@disabled)]"
                )
                simulate_click(driver, next_page_button)
                time.sleep(1)  # 等待新页面加载
                page_number += 1
                print(f"✅ 成功跳转到第 {page_number} 页。")
            except Exception:
                print("没有找到下一页按钮或已到最后一页，结束抓取。")
                break
        
        # 8. 将数据保存为 Excel 文件，并调整列宽和行高
        if job_data_list:
            df = pd.DataFrame(job_data_list)
            output_filename = "job_listings.xlsx"
            with pd.ExcelWriter(output_filename, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Sheet1')
                workbook  = writer.book
                worksheet = writer.sheets['Sheet1']

                text_wrap_fmt = workbook.add_format({'text_wrap': True})
                max_col_width = 60

                for i, col in enumerate(df.columns):
                    content_length = df[col].astype(str).map(len).max()
                    header_length = len(col)
                    col_width = max(content_length, header_length) + 2
                    col_width = min(col_width, max_col_width)
                    worksheet.set_column(i, i, col_width, text_wrap_fmt)

                for row in range(1, len(df.index) + 1):
                    worksheet.set_row(row, 80)

            print(f"✔️ 数据已保存到 {output_filename}，且列宽和行高已调整。")
        else:
            print("未抓取到任何职位数据。")
        
        time.sleep(5)
    
    except Exception as ex:
        print("Exception during execution:", ex)
        traceback.print_exc()
    finally:
        driver.quit()

if __name__ == "__main__":
    main()