
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
customer_name = ''
x = ''
salon_board_status = ''
sb_username = ''
sb_password = ''
# print(id)
# print("hello")
# exit()
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
	
# ncdte = datetime.datetime.now() + datetime.timedelta(days=1)
# ndate = ncdte.strftime("%Y")+ncdte.strftime("%m")+ncdte.strftime("%d")


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
        global customer_name
        global x
        global salon_board_status
        global username
        global password
        global reservation_type
        mySQLConnection = mysql.connector.connect(host='34.85.64.241',
                                             database='jtsboard_new',
                                             user='jts',
                                             password='Jts5678?')






        
        cursor = mySQLConnection.cursor()
        sql_select_query = """select employee_ids,start_date, all_day, start_time, end_time, reservation_type, user_id, customer_id from reservations where id = %s"""
        cursor.execute(sql_select_query , (reservation_id,))
        record = cursor.fetchall()
        employee_id = int(record[0][0])
        x = str(record[0][1])
        all_day = str(record[0][2])
        start_time = str(record[0][3])
        end_time = str(record[0][4])
        reservation_type = int(record[0][5])
        user_id = str(record[0][6])
        customer_id = str(record[0][7])
        x = re.sub('-','',x)
        x = '#' + x
        reservation_date = japanese_date(record[0][1])
        start_hours, start_minutes, sec = map(int, start_time.split(':'))
        end_hours, end_minutes, sec = map(int, end_time.split(':'))

        sql_select_query = """select name from customers where id = %s"""
        cursor.execute(sql_select_query , (customer_id,))
        record = cursor.fetchall()
        print(record)
        customer_name = record[0][0].decode("utf-8")
        # print(type(customer_name.decode("utf-8")))
        print(customer_name)
        # exit()



        sql_select_query = """select name from employees where id = %s"""
        cursor.execute(sql_select_query , (employee_id,))
        record = cursor.fetchall()
        employee_name = record[0][0]
        print(employee_name)

        

        sql_select_query = """select salon_board_status,sb_username,sb_password from users where id = %s"""
        cursor.execute(sql_select_query , (user_id,))
        record = cursor.fetchall()
        salon_board_status = record[0][0]
        sb_username = record[0][1]
        sb_password = record[0][2]
        username = sb_username.decode('ASCII') 
        password = sb_password.decode('ASCII') 

        # print(reservation_type)
        # print(type(salon_board_status))
        # print(type(username))
        # print(type(password))
        # exit()
      
    except mysql.connector.Error as error:
        print("Failed to get record from database: {}".format(error))
    finally:
        if (mySQLConnection.is_connected()):
            cursor.close()
            mySQLConnection.close()

def calenderSpace():
	try:
		WebDriverWait(driver, 100).until( lambda driver: driver.find_element_by_xpath('/html/body/div[8]/div[1]/div[1]/div[1]/div/p[3]/a'))
		time.sleep(2)
		driver.find_element_by_xpath('/html/body/div[8]/div[1]/div[1]/div[1]/div/p[3]/a').click()

		time.sleep(2)
		actions = ActionChains(driver)
		WebDriverWait(driver, 100).until( lambda driver: driver.find_element_by_xpath('/html/body/div[8]/div[2]/div[2]/div[2]/ul[1]/li[1]/div/div[1]'))
		blank = driver.find_element_by_xpath('/html/body/div[8]/div[2]/div[2]/div[2]/ul[1]/li[1]/div/div[1]')
		empty_space = actions.move_to_element(blank)
		empty_space.click().perform()
		driver.find_element_by_xpath("/html/body/div[8]/ul/li[1]/a").click()
		driver.find_element_by_link_text("予定を登録する").click()
		time.sleep(2)
	except:
		calenderSpace()

		


userRecords = getSalonboarUser()

url = "https://salonboard.com/login/"
# username = "CC21324"
# password = "Majestic@2019"
# username = sb_username
# password = sb_password
options = Options()
options.add_argument('-headless')
# driver = webdriver.Firefox(executable_path=r'/usr/local/bin/geckodriver')
driver = webdriver.Firefox(executable_path=r'/usr/local/bin/geckodriver', options=options)

print("before driver")



if __name__ == "__main__":
	#driver = webdriver.Firefox()
	#driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub', desired_capabilities=webdriver.DesiredCapabilities.FIREFOX)
	print(type(int(reservation_type)))
	if (username != '' and password != '' and reservation_type == 1):
		driver.get(url)
		print("before login")

		uname = driver.find_element_by_name("userId")# ← find by element name
		uname.send_keys(username) # ← enters the username in textbox
		passw = driver.find_element_by_name("password")
		passw.send_keys(password)  #← enters the password in textbox
		# Find the submit button using class name and click on it.
		submit_button = driver.find_element_by_class_name("input_area_btn_01").click()
		print("after login")

		WebDriverWait(driver, 100).until( lambda driver: driver.find_element_by_xpath('//*[@id="globalNavi"]/ul[2]/li[1]/a/img'))
		time.sleep(2)
		driver.find_element_by_xpath('//*[@id="globalNavi"]/ul[2]/li[1]/a/img').click()

		try:
			WebDriverWait(driver, 100).until( lambda driver: driver.find_element_by_xpath('/html/body/div[8]/div[1]/div[1]/div[1]/div/p[3]/a'))
			time.sleep(2)
			driver.find_element_by_xpath('/html/body/div[8]/div[1]/div[1]/div[1]/div/p[3]/a').click()

			time.sleep(2)
			actions = ActionChains(driver)
			WebDriverWait(driver, 100).until( lambda driver: driver.find_element_by_xpath('/html/body/div[8]/div[2]/div[2]/div[2]/ul[1]/li[1]/div/div[1]'))
			blank = driver.find_element_by_xpath('/html/body/div[8]/div[2]/div[2]/div[2]/ul[1]/li[1]/div/div[1]')
			empty_space = actions.move_to_element(blank)
			empty_space.click().perform()
			driver.find_element_by_xpath("/html/body/div[8]/ul/li[1]/a").click()
			driver.find_element_by_link_text("予定を登録する").click()
			time.sleep(2)
		except:
			calenderSpace()
			


		time.sleep(2)
		select = Select(driver.find_element_by_name("staffId"))
		select.select_by_visible_text(employee_name.decode("utf-8"))

		driver.find_element_by_xpath('//*[@id="jsiSchDateDummy"]').click()
		time.sleep(2)

		# driver.find_element_by_css_selector("a[href*='"+x+"']").click()
		try:
			driver.find_element_by_css_selector("a[href*='"+x+"']").click()
		except:
			WebDriverWait(driver, 100).until( lambda driver: driver.find_element_by_xpath('//*[@id="prevMonth"]'))
			time.sleep(2)
			driver.find_element_by_xpath('//*[@id="prevMonth"]').click()
			driver.find_element_by_css_selector("a[href*='"+x+"']").click()



		# driver.find_element_by_link_text(str(x)).click()
		time.sleep(2)

		select = Select(driver.find_element_by_name("rsvHour"))
		select.select_by_visible_text(str(start_hours))

		print("start_hours")
		print(start_hours)

		select = Select(driver.find_element_by_name("rsvMinute"))
		if(start_minutes == 0):
			select.select_by_visible_text('00')
		else:
			select.select_by_visible_text(str(start_minutes))
		print("start_minutes")
		print(start_minutes)

		select = Select(driver.find_element_by_name("schEndHour"))
		select.select_by_visible_text(str(end_hours))
		print("end_hours")
		print(end_hours)

		select = Select(driver.find_element_by_name("schEndMinute"))
		if(end_minutes == 0):
			select.select_by_visible_text('00')
		else:
			select.select_by_visible_text(str(end_minutes))
		print("end_minutes")
		print(end_minutes)
		# select = driver.find_element_by_name("schTitle")
		# select.select_by_visible_text(customer_name)
		schtitle = driver.find_element_by_name("schTitle")
		print('start')

		print(customer_name)
		print('end')
		schtitle.send_keys(customer_name)

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
		
		
		try:
			WebDriverWait(driver, 100).until( lambda driver: driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/div/ul/li/b'))
			blank = driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/div/ul/li/b')
			if((blank.text == '入力された予定登録日にはすでに予定が登録されています。終日の予定を登録すると、すでに登録されていた予定の情報は失われます。入力内容を再度ご確認の上、問題なければ「登録する」を押してください。') | (blank.text == '入力された時間帯に別のシフトまたは予定が登録されています。シフトまたは予定が重複しない時間を入力してください。')):
				print('succ already')
				driver.quit()
				exit()
			else:
				print('succ new')
				driver.quit()
				exit()
		

		except:
			print("Already Not blocked")	
		
	print('succ')
	driver.quit()
exit()
