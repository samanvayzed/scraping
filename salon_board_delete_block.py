#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 11:08:37 2019

@author: imox
"""

# -*- coding: utf-8 -*-
import sys
import logging
import time 
from datetime import datetime       
from selenium import webdriver
#from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import salon_board_utility


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

logger.info('Received Reservation Id (unBlock):'+str(reservation_id))

def deleteUrlGenerator(date_str,mapper,employee_name,start_hour,start_minute):
	employee_name = employee_name.replace('\u3000',' ')
	employee_name = employee_name.strip()

	if(start_hour ==0):
		start_hour = "00"

	if(start_minute ==0):
		start_minute = "00"


	if employee_name not in mapper:
		return 1

	url ="https://salonboard.com/KLP/set/scheduleChange/?date=date_str&hour=start_hour&minute=start_minute&staffId=employee_id";
	date_str = date_str.replace("#", "") 


	url = url.replace("date_str", date_str)
	url = url.replace("start_hour", str(start_hour))
	url = url.replace("start_minute", str(start_minute))
	url = url.replace("employee_id", str(mapper[employee_name])) 

	logger.info("Delete Url formed %s" %(url))

	return url

def goToTheDatePage(date_str):
	date_str = date_str.replace("#", "") 
	date_url = "https://salonboard.com/KLP/schedule/salonSchedule/?date=";
	driver.get(date_url+str(date_str))
	logger.info("Moved Url to date url: %s"% (date_url+str(date_str)))
	time.sleep(3)

def clickOneOfTheBlocked():

	clicked_success = 0
	for blocked in driver.find_elements_by_class_name('scheduleToDoInner'):
		try:
			blocked.click()
			clicked_success = 1
			break
		except:
			pass

	return clicked_success

def unBlock(employee_name,date_original,date,start_hour,start_minute,end_hour,end_minute,all_day):
	data = {}

	current_date = datetime.today().strftime('%Y-%m-%d')

	if(date_original<current_date):
		data['status'] = 0
		data['msg'] = "The blocking schedule date has already passed"
		return data

	if(start_minute%5!=0 or end_minute%5!=0):
		data['status'] = 0
		data['msg'] = "End minute or start minute is not multiple of 5"
		return data

	#goToTheDatePage(date)
	# clicked_success = clickOneOfTheBlocked()

	# if(not clicked_success):
	# 	data['status'] = 0
	# 	data['msg'] = "Can't find the blocked area"
	# 	return data

	



	# driver.find_element_by_class_name("mod_btn_10").click()
	# time.sleep(2)

	logger.info("Unblocking Action activated for: %s for date %s , starting time %s:%s to end time %s:%s"% (employee_name,date,start_hour,start_minute,end_hour,end_minute))

	mapper = salon_board_utility.find_staff_name_id_map(driver.page_source, driver)
	url = deleteUrlGenerator(date,mapper,employee_name.decode("utf-8"),start_hour,start_minute)

	if(url==1):
		data['status'] = 0
		data['msg'] = "Employee id not found"
		return data

	driver.get(url)
	logger.info("Moved to delete url: %s"% (url))
	time.sleep(4)

	suceessful_url_change = salon_board_utility.find_url_change_succedded(driver.page_source)

	if( not suceessful_url_change):
		data['status'] = 0
		data['msg'] = "Url "+url+" doesnt look valid url for unblocking"
		return data


	selectStaff = Select(driver.find_element_by_name("staffId"))
	

	

	# found_staff = 0
	# for staffOption in selectStaff.options:
	# 	if employee_name==staffOption.text:
	# 		found_staff = 1
	# 		staffOption.click()
	# 		break

	# if(not found_staff):
	# 	data['status'] = 0
	# 	data['msg'] = "Can't find the staff to block"
	# 	return data

	selectStaff.select_by_visible_text(employee_name.decode("utf-8"))

	driver.find_element_by_xpath('//*[@id="jsiSchDateDummy"]').click()
	time.sleep(2)



	driver.find_element_by_css_selector("a[href*='"+date+"']").click()
	time.sleep(2)

	all_day_pre_selected = driver.find_element_by_xpath('//*[@id="allDayFlg"]').is_selected()
	

	if(all_day_pre_selected):
		#if all day is pre selected first unselect it
		driver.find_element_by_xpath('//*[@id="allDayFlg"]').click()
		time.sleep(2)
	if(all_day == '1'):
		driver.find_element_by_xpath('//*[@id="allDayFlg"]').click()

	else:
		select = Select(driver.find_element_by_name("schStartHour"))
		if(start_hour == 0):
			select.select_by_visible_text('0')
		else:
			select.select_by_visible_text(str(start_hour))

		select = Select(driver.find_element_by_name("schStartMinute"))

		if(start_minute == 0):
			select.select_by_visible_text('00')
		else:
			select.select_by_visible_text(str(start_minute))

		select = Select(driver.find_element_by_name("schEndHour"))
		if(end_hour == 0):
			select.select_by_visible_text('0')
		else:
			select.select_by_visible_text(str(end_hour))
		
		select = Select(driver.find_element_by_name("schEndMinute"))
		if(end_minute == 0):
			select.select_by_visible_text('00')
		else:
			select.select_by_visible_text(str(end_minute))

	
	
	driver.find_element_by_xpath('//*[@id="delete"]').click()

	time.sleep(4)

	try:
		alert = driver.switch_to.alert
		time.sleep(3)
		alert.accept()
		data['status'] = 1;
	except:
		data['status'] = 0;
		data['msg'] = "Unblock final stage: click on alert box failed"
	
	
	return data

url = "https://salonboard.com/login/"
salonBoardData = salon_board_utility.getSalonboardUser(reservation_id)
webDriverSetting = salon_board_utility.getWebDriverInfo()

options = Options()
options.add_argument('-headless')
# driver = webdriver.Chrome(webDriverSetting['chrome_path'], options=options)
# driver = webdriver.Firefox(executable_path=r'/usr/local/bin/geckodriver')
driver = webdriver.Firefox(executable_path=r'/usr/local/bin/geckodriver', options=options)

logger.info('Driver Initialized')

if __name__ == "__main__":
	# print(salonBoardData)
	if (('sb_username' in salonBoardData and salonBoardData['sb_username'] != '') and ('sb_password' in salonBoardData and salonBoardData['sb_password'] != '')):
		driver.get(url)
		logger.info('Getting the login page')

		uname = driver.find_element_by_name("userId")# ← find by element name
		uname.send_keys(salonBoardData['sb_username']) # ← enters the username in textbox
		passw = driver.find_element_by_name("password")
		passw.send_keys(salonBoardData['sb_password'])  #← enters the password in textbox
		# Find the submit button using class name and click on it.
		submit_button = driver.find_element_by_class_name("input_area_btn_01").click()
		logger.info('Clicked submit & trying to login')

		# browser.current_url

		WebDriverWait(driver, 100).until( lambda driver: driver.find_element_by_xpath('/html/body/div[1]/div/div/ul[2]/li[1]/a/img'))
		time.sleep(2)
		driver.find_element_by_xpath('/html/body/div[1]/div/div/ul[2]/li[1]/a/img').click()
		time.sleep(5)

		unblocked = unBlock(salonBoardData['employee_name'],salonBoardData['start_date_original'],salonBoardData['start_date'],salonBoardData['start_hours'],salonBoardData['start_minutes'],salonBoardData['end_hours'],salonBoardData['end_minutes'],salonBoardData['all_day'])
		
		if(unblocked['status']):
			logger.info("Reservation Id %s unblocked successfully",(reservation_id,))
			salon_board_utility.send_message_to_slack("Reservation Id %s unblocked successfully." %(reservation_id))
		else:
			logger.info("Reservation Id %s unblocking Failed" %(reservation_id))
			logger.info("Failure reason %s" %(unblocked['msg']))
			salon_board_utility.send_message_to_slack("Reservation Id %s unblocking Failed. Failure reason: %s" %(reservation_id,unblocked['msg']))

	else:
		salon_board_utility.send_message_to_slack("Reservation Id %s unblocking Failed. Failure reason: username or password for login not found" %(reservation_id))
		logger.info("Reservation Id %s unblocking Failed. Failure reason: username or password for login not found" %(reservation_id))

	driver.quit()

exit()

