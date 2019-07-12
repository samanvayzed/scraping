from selenium import webdriver
import json
import time

driver = webdriver.Firefox(executable_path = '/usr/local/bin/geckodriver')
driver.get("https://salonboard.com/login/")

uid = driver.find_element_by_name("userId")
uid.send_keys("CC21324")

pw = driver.find_element_by_name("password")
pw.send_keys("Majestic2020!")

submit = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/form/div/div[2]/a")
submit.click()

time.sleep(20) # CAPTCHA

link = driver.find_element_by_xpath("/html/body/div[1]/div/div/ul[2]/li[2]/a/img")
link.click()

link = driver.find_element_by_xpath("/html/body/form[1]/div/div/ul/li[5]/a/img")
link.click()

list_of_table_ids = []

for i in range(1,59):
    if i<10:
        i = "0" + str(i)
    else:
        i = str(i)
    full_id = "TagTBL_MENU_TABLE_0" + i
    list_of_table_ids.append(full_id)

print(list_of_table_ids)

list_of_results = []

for table_id in list_of_table_ids:

    #table = driver.find_element_by_id("TagTBL_MENU_TABLE_001")
    table = driver.find_element_by_id(table_id)

    rows = table.find_elements_by_tag_name("tr") # get all of the rows in the table

    rowcount = 1
    for row in rows:

        if rowcount == 1:
            print("####################  ROW " + str(rowcount) + " #################")
            # Get the columns (all the column 2)
            cols = row.find_elements_by_tag_name("td")#note: index start from 0, 1 is col 2
            
            colcount = 1
            for col in cols:

                if colcount == 1:

                    print("######  COLUMN " + str(colcount) + " ######") 
                    #print(col.text) #prints text from the element
                    selects = col.find_elements_by_tag_name("select")#note: index start from 0, 1 is col 2
                    select = selects[0] 

                    options = select.find_elements_by_tag_name("option")#note: index start from 0, 1 is col 2
                    for option in options:
                        #print(option.text) 
                        #print(option.get_attribute('selected')) 

                        if option.get_attribute('selected') == "true":
                            long_service = option.text
                            #print(option.get_attribute('value'))
                            long_service_arr = long_service.split('：')
                            service = long_service_arr[0]
                    print(service)
                            

                if colcount == 2:

                    print("######  COLUMN " + str(colcount) + " ######") 
                    #print(col.text) #prints text from the element
                    textareas = col.find_elements_by_tag_name("textarea")#note: index start from 0, 1 is col 2
                    textarea = textareas[0] 
                    menu_item = textarea.text

                    print(menu_item)

                if colcount == 4:

                    print("######  COLUMN " + str(colcount) + " ######") 
                    #print(col.text) #prints text from the element
                    uls = col.find_elements_by_tag_name("ul")#note: index start from 0, 1 is col 2
                    ul = uls[0] 

                    lis = ul.find_elements_by_tag_name("li")#note: index start from 0, 1 is col 2
                    
                    radio = 0 
                    for li in lis:
                        inputs = li.find_elements_by_tag_name("input")
                        input1 = inputs[0] 
                        if input1.get_attribute('checked') == "true":
                            break 
                        radio += 1
                    
                    posted = 0
                    
                    if radio == 0:
                        posted = 1
                    if radio == 1: 
                        posted = 0

                    print(posted)

                colcount += 1

        result_dict = {
            "type": "menu",
            "name": menu_item,
            "posted": posted,
            "service": service,
            "salon_id": 102
        }
        rowcount += 1

    list_of_results.append(result_dict)

print(len(list_of_results))

result_json = json.dumps(list_of_results,ensure_ascii=False)
print(result_json)

