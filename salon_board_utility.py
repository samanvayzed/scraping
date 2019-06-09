import mysql.connector
import logging
import re
import requests
import time 
from selenium import webdriver
#from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup as bs

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

def find_url_change_succedded(html):

    soup = bs(html)
    success =  soup.find(class_="errorModuleId")
    
    #error class not found
    if success is None:
        return 1
    else:
        return 0

def find_staff_name_id_map(html, driver):
    

    mapper={}
    try:
        soup = bs(html)
        main_div = soup.find("div", {"id": "schedule"})
        employees_ul = main_div.find("ul",class_="jscScheduleMainHeadListStaff")
        employees_li = employees_ul.findAll("li")

        for li in employees_li:
            emp_id = li['id']
            emp_id_split=emp_id.split("_")
            emp_id = emp_id_split[1]
            emp_name = li.find("span",class_="scheduleLinkInner").text
            mapper[emp_name.strip()] = emp_id
    except:
        WebDriverWait(driver, 100).until( lambda driver: driver.find_element_by_xpath('/html/body/div[8]/div[1]/div[1]/div[1]/div/p[1]/a'))
        time.sleep(2)
        driver.find_element_by_xpath('/html/body/div[8]/div[1]/div[1]/div[1]/div/p[1]/a').click()
        time.sleep(10)
        html = driver.page_source
        
        soup = bs(html)
        main_div = soup.find("div", {"id": "schedule"})
        employees_ul = main_div.find("ul",class_="jscScheduleMainHeadListStaff")
        employees_li = employees_ul.findAll("li")

        for li in employees_li:
            emp_id = li['id']
            emp_id_split=emp_id.split("_")
            emp_id = emp_id_split[1]
            emp_name = li.find("span",class_="scheduleLinkInner").text
            mapper[emp_name.strip()] = emp_id

            
    return mapper



def send_message_to_slack(msg):
    webhook_endpoint = "https://hooks.slack.com/services/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"
    r = requests.post(webhook_endpoint, json={"text": msg})
    
def getWebDriverInfo():
    setting = {}
    setting['chrome_path'] = "/Users/imox/ahlat/webdriverio-test/chromedriver"

    return setting

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

def getMysqlCredentials():
    cred = {};
    cred['host'] = '34.85.64.241'
    cred['database'] = 'jtsboard_new'
    cred['user'] = 'jts'
    cred['password'] = 'Jts5678?'

    return cred;

def queryStore(query_type):
    selected_query = ""

    if query_type=="reservations_detail":
        selected_query = """select employee_ids,start_date, all_day, start_time, end_time, reservation_type, user_id from reservations where id = %s"""

    elif query_type=="employee_name":
        selected_query = """select name from employees where is_technician = 1 and id = %s"""

    elif query_type=="sb_username_password":
        selected_query = """select salon_board_status,sb_username,sb_password from users where id = %s"""


    return selected_query;

def findEmployeeName(emp_id):

    cred = getMysqlCredentials()
    mySQLConnection = mysql.connector.connect(host=cred['host'],
                                         database=cred['database'],
                                         user=cred['user'],
                                         password=cred['password'])

    cursor = mySQLConnection.cursor()
    employee_name_query = queryStore("employee_name")
    cursor.execute(employee_name_query , (emp_id,))
    record = cursor.fetchall()
    return record[0][0]

def getSalonboardUser(reservation_id):
    
    '''using reservation id find the user and then from user_id find his username and password for 
       salon board stored in mysql db'''

    #make connection to the data store
    cred = getMysqlCredentials()
    mySQLConnection = mysql.connector.connect(host=cred['host'],
                                         database=cred['database'],
                                         user=cred['user'],
                                         password=cred['password'])

    try:
    	
        fetched_data = {}

        cursor = mySQLConnection.cursor()

        #get reservation detail
        reservations_detail_query = queryStore("reservations_detail");
        cursor.execute(reservations_detail_query , (reservation_id,))
        record = cursor.fetchall()

        fetched_data['employee_id'] = int(record[0][0])
        fetched_data['employee_ids'] = str(fetched_data['employee_id']).split(',')
        fetched_data['start_date'] = str(record[0][1])
        fetched_data['start_date_original'] = str(record[0][1])
        fetched_data['all_day'] = str(record[0][2])
        fetched_data['start_time'] = str(record[0][3]) if record[0][3] is not None else 0
        fetched_data['end_time'] = str(record[0][4]) if record[0][4] is not None else 0
        fetched_data['reservation_type'] = int(record[0][5])
        fetched_data['user_id'] = str(record[0][6])
        fetched_data['start_date'] = re.sub('-','',fetched_data['start_date'])
        fetched_data['start_date'] = '#' + fetched_data['start_date']
        fetched_data['reservation_date'] = japanese_date(record[0][1])

        if fetched_data['start_time'] !=0:
            fetched_data['start_hours'], fetched_data['start_minutes'], fetched_data['start_sec'] = map(int, fetched_data['start_time'].split(':'))
        else:
            fetched_data['start_hours'] = 0
            fetched_data['start_minutes'] = 0
            fetched_data['start_sec'] = 0

        if fetched_data['end_time'] !=0:
            fetched_data['end_hours'], fetched_data['end_minutes'], fetched_data['end_sec'] = map(int, fetched_data['end_time'].split(':'))
        else:
            fetched_data['end_hours'] = 0
            fetched_data['end_minutes'] = 0
            fetched_data['end_sec'] = 0
            
        #find employee name to whom reservation was assigned
        if("," not in str(fetched_data['employee_id'])):
            employee_name_query = queryStore("employee_name")
            cursor.execute(employee_name_query , (fetched_data['employee_id'],))
            record = cursor.fetchall()
            fetched_data['employee_name'] = record[0][0]

        #find sb username password so that we can login
        sb_username_password_query = queryStore("sb_username_password")
        cursor.execute(sb_username_password_query , (fetched_data['user_id'],))
        record = cursor.fetchall()

        fetched_data['salon_board_status'] = record[0][0]
        fetched_data['sb_username'] = record[0][1]
        fetched_data['sb_password'] = record[0][2]
        logger.info("Username found:"+str(fetched_data['sb_username']))
        logger.info("Password found:"+str(fetched_data['sb_password']))

        if not isinstance(fetched_data['sb_username'], str):
            fetched_data['sb_username'] = fetched_data['sb_username'].decode('ASCII') 

        if not isinstance(fetched_data['sb_password'], str):
            fetched_data['sb_password'] = fetched_data['sb_password'].decode('ASCII') 
        
        fetched_data['status'] = 1

    except mysql.connector.Error as error:
        fetched_data['status'] = 0
        logger.debug("Failed to get record from database: {}".format(error))
    finally:
        if (mySQLConnection.is_connected()):
            cursor.close()
            mySQLConnection.close()
        return fetched_data
