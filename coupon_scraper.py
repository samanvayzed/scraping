from selenium import webdriver
import json
import time

import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox(executable_path = '/usr/local/bin/geckodriver')
driver.get("https://salonboard.com/login/")

uid = driver.find_element_by_name("userId")
uid.send_keys("CC21324")

pw = driver.find_element_by_name("password")
pw.send_keys("Majestic2020!")

submit = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/form/div/div[2]/a")
submit.click()

time.sleep(20) # CAPTCHA

list_of_results = []

def get_info(row_num):
    print("--------------------")
    print(row_num)

    link = driver.find_element_by_xpath("/html/body/div[1]/div/div/ul[2]/li[2]/a/img")
    link.click()

    link = driver.find_element_by_xpath("/html/body/form[1]/div/div/ul/li[8]/a/img")
    link.click()

    table = driver.find_element_by_xpath("/html/body/div[2]/div/table[2]")
    rows = table.find_elements_by_tag_name("tr")
   
    row = rows[row_num]
    cols = row.find_elements_by_tag_name("td")


    print("XXX")
    col1 = cols[0]
    print(col1.text) 
    inputs1 = col1.find_elements_by_tag_name("input")
    input1 = inputs1[0]
    posted = input1.get_attribute('value')
    print(posted)
    print("XXX")

    if posted == "":
        posted = 0 
    else:
        posted = 1

    col = cols[6]        
    links = col.find_elements_by_tag_name("a")
    link = links[0]
    link.click()
    time.sleep(2)

    table2 = driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/div/form/table")
    tbodys = table2.find_elements_by_tag_name("tbody")
    tbody= tbodys[1]

    trs = tbody.find_elements_by_tag_name("tr")
    
    
    tr= trs[2]

    tds = tr.find_elements_by_tag_name("td")
    td= tds[1]

    inputs = td.find_elements_by_tag_name("input")
    input1= inputs[0]

    name = input1.get_attribute('value')
    print(name)

    tr1= trs[7]
    tds1 = tr1.find_elements_by_tag_name("td")
    print(len(tds1))
    td1= tds1[0]

    selects1 = td1.find_elements_by_tag_name("select")
    select = selects1[0] 

    options = select.find_elements_by_tag_name("option")
    for option in options:
        if option.get_attribute('selected') == "true":
            long_service = option.text
            long_service_arr = long_service.split('：')
            service = long_service_arr[0]
    print(service)

    driver.back()
    time.sleep(2)

    result_dict = {
        "type": "coupon",
        "name": name,
        "posted": posted,
        "service": service,
        "salon_id": 102

    }

    list_of_results.append(result_dict)

for i in range(2,76):
    get_info(i)

#for i in range(2,4):
#    get_info(i)
print(len(list_of_results))
result_json = json.dumps(list_of_results,ensure_ascii=False)
print(result_json)


