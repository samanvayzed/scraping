# -*- coding: utf-8 -*-
import sys
import selenium
import datetime
import time 
import json
import requests
from selenium.common.exceptions import NoSuchElementException        
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import mysql.connector
from mysql.connector import errorcode
from selenium.webdriver.support.ui import Select
import re
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.alert import Alert
from pyvirtualdisplay import Display

reservation_id = sys.argv[1]
print(reservation_id)
# reservation_id = 4504
staff_name = ''
reservation_date = ''
reservation_time = ''
start_hours = ''
start_minutes = ''
end_hours = ''
end_minutes = ''
all_day = ''
employee_name = ''
x = ''

def getSalonboarUser():

    try:
    	
        global staff_name
        global reservation_date
        global reservation_time
        global start_hours
        global start_minutes
        global end_hours
        global end_minutes
        global all_day
        global employee_name
        global employee_ids
        global x
        global username
        global password
        mySQLConnection = mysql.connector.connect(host='34.85.64.241',
                                             database='jtsboard_new',
                                             user='jts',
                                             password='Jts5678?')
        cursor = mySQLConnection.cursor()
        sql_select_query = """select employee_ids,start_date, all_day, start_time, end_time, reservation_type, user_id from reservations where id = %s"""
        cursor.execute(sql_select_query , (reservation_id,))
        record = cursor.fetchall()
        employee_id = record[0][0]
        employee_ids = employee_id.split(',')
        # print(employee_ids)
        # exit()
        x = str(record[0][1])
        all_day = str(record[0][2])
        start_time = str(record[0][3])
        end_time = str(record[0][4])
        reservation_type = str(record[0][5])
        user_id = str(record[0][6])
        x = re.sub('-','',x)
        x = '#' + x
        # print(employee_id)
        # exit()
        reservation_date = japanese_date(record[0][1])

        sql_select_query = """select salon_board_status,sb_username,sb_password from users where id = %s"""
        cursor.execute(sql_select_query , (user_id,))
        record = cursor.fetchall()
        salon_board_status = record[0][0]
        sb_username = record[0][1]
        sb_password = record[0][2]
        username = sb_username.decode('ASCII') 
        password = sb_password.decode('ASCII') 

        # reservation_date = "2019年03月22日（ 水）"
        # print(reservation_date)
        # print(start_time)
        # print(start_hours)
        # print(start_minutes) 
        # print(end_hours)
        # print(end_minutes)
        # print(all_day)
        # print(employee_name)
        # exit()
    except mysql.connector.Error as error:
        print("Failed to get record from database: {}".format(error))
    finally:
        if (mySQLConnection.is_connected()):
            cursor.close()
            mySQLConnection.close()




def japanese_date(x):
	cday = x.strftime("%a")
	if cday == "Mon":
		cnday = "月" 
	elif cday == "Tue":
		cnday = "水" 
	elif cday == "Wed":
		cnday = "水" 
	elif cday == "Thu":
		cnday = "木" 
	elif cday == "Fri":
		cnday = "金" 
	elif cday == "Sat":
		cnday = "土" 
	elif cday == "Sun":
		cnday = "日" 
	return  x.strftime("%Y")+"年"+x.strftime("%m")+"月"+x.strftime("%d")+"日（ "+cnday+"）"


def selectDate(x):

    try:
    	driver.find_element_by_css_selector("a[href*='"+x+"']").click()

    except :
    	#openCalendarLabel > a > b
    	selectDate(x)

def getSalonboarEmployee(employee_id):

    try:
        mySQLConnection = mysql.connector.connect(host='34.85.64.241',
                                             database='jtsboard_new',
                                             user='jts',
                                             password='Jts5678?')



        cursor = mySQLConnection.cursor()



        sql_select_query = """select name from employees where id = %s"""
        cursor.execute(sql_select_query , (employee_id,))
        record = cursor.fetchall()
        employee_name = record[0][0]
        return employee_name
    except mysql.connector.Error as error:
        print("Failed to get record from database: {}".format(error))
    finally:
        if (mySQLConnection.is_connected()):
            cursor.close()
            mySQLConnection.close()    

userRecords = getSalonboarUser()
url = "https://salonboard.com/login/"
blockpage_url = "https://salonboard.com/KLP/reserve/ext/extReserveRegist/?staffId=W000263987&date=20190410&rsvHour=13&rsvMinute=45&rlastupdate=20190410232814"
# username = "CC21324"
# password = "Majestic2019"
options = Options()
options.add_argument('-headless')
# driver = webdriver.Firefox(executable_path=r'/usr/local/bin/geckodriver')
driver = webdriver.Firefox(executable_path=r'/usr/local/bin/geckodriver', options=options)
print("before driver")


if __name__ == "__main__":
	#driver = webdriver.Firefox()
	#driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub', desired_capabilities=webdriver.DesiredCapabilities.FIREFOX)
	driver.get(url)
	print(username)
	print("before login")
	print(password)
	uname = driver.find_element_by_name("userId")# ← find by element name
	uname.send_keys(username) # ← enters the username in textbox
	passw = driver.find_element_by_name("password")
	passw.send_keys(password)  #← enters the password in textbox
	# Find the submit button using class name and click on it.
	submit_button = driver.find_element_by_class_name("input_area_btn_01").click()
	print("after login")

	if (username != '' and password != ''):
			

		for emp in employee_ids:
			# driver.get(blockpage_url)
			WebDriverWait(driver, 100).until( lambda driver: driver.find_element_by_xpath('//*[@id="globalNavi"]/ul[2]/li[1]/a/img'))
			time.sleep(2)
			driver.find_element_by_xpath('//*[@id="globalNavi"]/ul[2]/li[1]/a/img').click()
			WebDriverWait(driver, 100).until( lambda driver: driver.find_element_by_xpath('/html/body/div[8]/div[1]/div[1]/div[1]/div/p[3]/a'))
			time.sleep(2)
			driver.find_element_by_xpath('/html/body/div[8]/div[1]/div[1]/div[1]/div/p[3]/a').click()
			WebDriverWait(driver, 100).until( lambda driver: driver.find_element_by_xpath('/html/body/div[7]/div/div/ul/li[2]/a/img'))

			time.sleep(2)
			actions = ActionChains(driver)
			WebDriverWait(driver, 100).until( lambda driver: driver.find_element_by_xpath('/html/body/div[8]/div[2]/div[2]/div[2]/ul[1]/li[1]/ol/li[2]'))
			blank = driver.find_element_by_xpath('/html/body/div[8]/div[2]/div[2]/div[2]/ul[1]/li[1]/ol/li[2]')
			empty_space = actions.move_to_element(blank)
			empty_space.click().perform()

			
			driver.find_element_by_xpath("/html/body/div[8]/ul/li[2]/a").click()
			driver.find_element_by_link_text("予定を登録する").click()
			time.sleep(2)

			emp_name = getSalonboarEmployee(emp)
			select = Select(driver.find_element_by_name("staffId"))
			select.select_by_visible_text(emp_name.decode("utf-8"))

			driver.find_element_by_xpath('//*[@id="jsiSchDateDummy"]').click()
			time.sleep(2)

			# driver.find_element_by_css_selector("a[href*='#20190422']").click()
			driver.find_element_by_css_selector("a[href*='"+x+"']").click()

			# driver.find_element_by_link_text(str(x)).click()
			time.sleep(2)

			if(all_day == '1'):
				driver.find_element_by_xpath('//*[@id="allDayFlg"]').click()
			driver.find_element_by_xpath('//*[@id="regist"]').click()

			time.sleep(2)
			try:
				alert = driver.switch_to.alert
				print(alert.text)
				time.sleep(3)
				alert.accept()
				print('suc alert')
				
			except:
				# print "no alert to accept"
				print("No alert")


	print('succ')
	exit()
	driver.quit()
exit()
