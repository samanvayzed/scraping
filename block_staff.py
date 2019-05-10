# -*- coding: utf-8 -*-
import sys
from datetime import datetime 
import time 
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
#from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import salon_board_utility
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create a file handler
handler = logging.FileHandler('scrape.log')
handler.setLevel(logging.DEBUG)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)


reservation_id = sys.argv[1]

logger.info('Received Reservation Id (block staff for holiday):'+str(reservation_id))


def staffHolidayUrlGenerator(date_str,mapper,employee_name):
    employee_name = employee_name.replace('\u3000',' ')
    employee_name = employee_name.strip()

    if employee_name not in mapper:
        return 1

    url = "https://salonboard.com/KLP/reserve/ext/extReserveRegist/?staffId=employee_id&date=date_str&rsvHour=10&rsvMinute=00"

    date_str = date_str.replace("#", "") 

    url = url.replace("date_str", date_str)
    url = url.replace("employee_id", str(mapper[employee_name])) 

    logger.info("Staff holiday  Url formed %s" %(url))

    return url

def markHoliday(url,employee_name,start_date_original,start_date,start_hours,start_minutes,end_hours,end_minutes,all_day):

    all_day = str(all_day)
    # employee_name = employee_name.replace('\u3000',' ')
    # employee_name = employee_name.strip()

    data = {}

    current_date = datetime.today().strftime('%Y-%m-%d')

    if(start_date_original<current_date):
        data['status'] = 0
        data['msg'] = "The holiday schedule date has already passed"
        return data

    if(all_day!='1' and (start_minutes%5!=0 or end_minutes%5!=0)):
        data['status'] = 0
        data['msg'] = "End minute or start minute is not multiple of 5"
        return data

    if all_day!='1' and start_hours<10:
        data['status'] = 0
        data['msg'] = "Start hours cant be less than 10"
        return data

    logger.info("Marking Holiday for: %s for date %s , starting time %s:%s to end time %s:%s"% (employee_name,start_date,start_hours,start_minutes,end_hours,end_minutes))

    driver.get(url)
    time.sleep(3)

    suceessful_url_change = salon_board_utility.find_url_change_succedded(driver.page_source)

    if( not suceessful_url_change):
        data['status'] = 0
        data['msg'] = "Url "+url+" doesnt look valid url for employee holiday marking"
        return data

    driver.find_element_by_link_text("予定を登録する").click()
    time.sleep(2)

            
    select = Select(driver.find_element_by_name("staffId"))
    #select.select_by_visible_text(employee_name.decode("utf-8"))
    select.select_by_visible_text(employee_name)

    driver.find_element_by_xpath('//*[@id="jsiSchDateDummy"]').click()
    time.sleep(2)

    # driver.find_element_by_css_selector("a[href*='#20190422']").click()
    driver.find_element_by_css_selector("a[href*='"+str(start_date)+"']").click()

    # driver.find_element_by_link_text(str(x)).click()
    time.sleep(2)


    all_day_pre_selected = driver.find_element_by_xpath('//*[@id="allDayFlg"]').is_selected()

    if(all_day_pre_selected):
        #if all day is pre selected first unselect it
        driver.find_element_by_xpath('//*[@id="allDayFlg"]').click()
        time.sleep(2)

    if(all_day == '1'):
        driver.find_element_by_xpath('//*[@id="allDayFlg"]').click()
        driver.find_element_by_xpath('//*[@id="regist"]').click()

    else:
        select = Select(driver.find_element_by_name("rsvHour"))
        select.select_by_visible_text(str(start_hours))
        select = Select(driver.find_element_by_name("rsvMinute"))

        if(start_minutes == 0):
            select.select_by_visible_text('00')
        else:
            select.select_by_visible_text(str(start_minutes))

        select = Select(driver.find_element_by_name("schEndHour"))
        select.select_by_visible_text(str(end_hours))

        select = Select(driver.find_element_by_name("schEndMinute"))
        if(end_minutes == 0):
            select.select_by_visible_text('00')
        else:
            select.select_by_visible_text(str(end_minutes))

        driver.find_element_by_xpath('//*[@id="regist"]').click()

    time.sleep(4)

    try:
        alert = driver.switch_to.alert
        time.sleep(3)
        alert.accept()
        data['status'] = 1;

        
    except:
        data['status'] = 0;
        data['msg'] = "Holiday final stage: click on alert box failed"


    return data

salonBoardData = salon_board_utility.getSalonboardUser(reservation_id)
logger.info('Got salon board data like password, username etc from datastore')

url = "https://salonboard.com/login/"

webDriverSetting = salon_board_utility.getWebDriverInfo()
options = Options()
options.add_argument('-headless')
#driver = webdriver.Chrome(webDriverSetting['chrome_path'], options=options)
driver = webdriver.Firefox(executable_path=r'/usr/local/bin/geckodriver', options=options)



if __name__ == "__main__":
    driver.get(url)
    time.sleep(2)
    logger.info('Fetched Login URL, trying to login...')

	

    if (('sb_username' in salonBoardData and salonBoardData['sb_username'] != '') and ('sb_password' in salonBoardData and salonBoardData['sb_password'] != '')):

        uname = driver.find_element_by_name("userId")# ← find by element name
        uname.send_keys(salonBoardData['sb_username']) # ← enters the username in textbox
        passw = driver.find_element_by_name("password")
        passw.send_keys(salonBoardData['sb_password'])  #← enters the password in textbox
        # Find the submit button using class name and click on it.
        submit_button = driver.find_element_by_class_name("input_area_btn_01").click()
        logger.info('Logged Into Salon Board')

        WebDriverWait(driver, 100).until( lambda driver: driver.find_element_by_xpath('//*[@id="globalNavi"]/ul[2]/li[1]/a/img'))
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="globalNavi"]/ul[2]/li[1]/a/img').click()
        time.sleep(5)

        mapper = salon_board_utility.find_staff_name_id_map(driver.page_source, driver)
        logger.info("Applying Holiday for %s employee(s)" % (str(len(salonBoardData['employee_ids']))))
			
        for emp in salonBoardData['employee_ids']:

            salonBoardData['employee_name'] = salon_board_utility.findEmployeeName(emp)
            if(salonBoardData['employee_name'] != ''):
                url = staffHolidayUrlGenerator(salonBoardData['start_date'],mapper,salonBoardData['employee_name'].decode("utf-8"))
                #url = staffHolidayUrlGenerator(salonBoardData['start_date'],mapper,salonBoardData['employee_name'])

                

                markedHoliday = markHoliday(url,salonBoardData['employee_name'].decode("utf-8"),salonBoardData['start_date_original'],salonBoardData['start_date'],salonBoardData['start_hours'],salonBoardData['start_minutes'],salonBoardData['end_hours'],salonBoardData['end_minutes'],salonBoardData['all_day'])
                #markedHoliday = markHoliday(url,salonBoardData['employee_name'],salonBoardData['start_date_original'],salonBoardData['start_date'],salonBoardData['start_hours'],salonBoardData['start_minutes'],salonBoardData['end_hours'],salonBoardData['end_minutes'],salonBoardData['all_day'])

                if(markedHoliday['status']):
                    logger.info("Reservation Id %s holiday marked successfully for employee id %s" % (reservation_id,str(emp)))
                    salon_board_utility.send_message_to_slack("Reservation Id %s holiday marked successfully for employee id %s" % (reservation_id,str(emp)))
                else:
                    logger.info("Reservation Id %s holiday marking failed for employee id %s. Failure Reason:%s" % (reservation_id,str(emp),markedHoliday['msg']))
                    salon_board_utility.send_message_to_slack("Reservation Id %s holiday marking failed for employee id %s. Failure Reason:%s" % (reservation_id,str(emp),markedHoliday['msg']))
			
        driver.quit()
exit()
