from flask import Flask, request, jsonify
import os
import json
import traceback
import subprocess


app = Flask(__name__)

os.environ['PATH'] += ':'+os.path.dirname(os.path.realpath(__file__))+"/webdrivers"

@app.route("/blockstaff", methods=['POST'])
def block_staff():
        jsonq = request.json
        id = jsonq['reservation_id']
        print(id)
        
        var = subprocess.run(["python3", "block_staff.py", id], stdout=subprocess.PIPE)
        var_str = str(var)

        #command = "/home/manishkumar_zed/env/bin/python3 /home/manishkumar_zed/scraping/block_staff.py " + id
        #os.system(command)
        out = {"status":var_str,"id":id}
        out_json = json.dumps(out)
        return out_json 


@app.route("/salonboarddeleteblock", methods=['POST'])
def salon_board_delete_block():
        jsonq = request.json
        id = jsonq['reservation_id']
        print(id)
        var = subprocess.run(["python3", "salon_board_delete_block.py", id], stdout=subprocess.PIPE)
        var_str = str(var)
        #command = "/home/manishkumar_zed/env/bin/python3 /home/manishkumar_zed/scraping/salon_board_delete_block.py " + id
        #os.system(command)
        out = {"status":var_str,"id":id}
        out_json = json.dumps(out)
        return out_json 

@app.route("/inputscraper", methods=['POST'])
def input_scraper():
        jsonq = request.json
        id = jsonq['reservation_id']
        print(id)
        var = subprocess.run(["python3", "input_scraper.py", id], stdout=subprocess.PIPE)
        var_str = str(var)
        #cur_dir = os.path.dirname('__file__')
        #print("Current Dir: " + cur_dir)

        #fo  = open('hello.py',"r+")
        #fo = open("/home/manishkumar_zed/scraping/hello.py", "r+")
        #str = fo.read()
        #print ("Read String is : ", str)

        #command = "cat /home/manishkumar_zed/scraping/input_scraper.py"
        #print("Command:" + command)
        #os.system(command)
        out = {"status":var_str,"id":id}
        out_json = json.dumps(out)
        return out_json 

if __name__ == '__main__':
        app.run(debug=True)
