# coding = utf-8
from selenium import webdriver
import time

browser = webdriver.Firefox()

browser.get("https://www.baidu.com")

browser.find_element_by_id("kw").send_keys("selenium")
browser.find_element_by_id("su").click()

time.sleep(5)

result = browser.find_element_by_xpath("//div/h3/a[text()='官方']/../a/em").text
if result == "Selenium":
    print("测试成功，结果和预期结果匹配！")
    browser.quit()
else:
    print("结果不符合预期")

