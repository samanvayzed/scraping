import subprocess

#proc = subprocess.Popen(["cat", "/home/manishkumar_zed/scraping/hello.py"], stdout=subprocess.PIPE, shell=True)
#(out, err) = proc.communicate()
#print ("program output:"+ out)


#command = "/home/manishkumar_zed/env/bin/python3 /home/manishkumar_zed/scraping/input_scraper.py " + id
id = 7185

var = subprocess.run(["/home/manishkumar_zed/env/bin/python3", "/home/manishkumar_zed/scraping/input_scraper.py", str(id)], stdout=subprocess.PIPE)

print(var)


