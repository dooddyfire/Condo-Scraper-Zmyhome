import datetime
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
#Fix
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


filename = input("ชื่อไฟล์ : ")
#Insert file name
start_page = int(input("ใส่เลขหน้าเริ่มต้น: "))

#Insert result name
end_page = int(input("ใส่เลขหน้าสุดท้าย: "))
keyword = "https://th.zmyhome.com/project/condo?page={}&sortFilter=yearnew&per-page=40".format(start_page)



page = []

#Get bot selenium make sure you can access google chrome
driver = webdriver.Chrome(ChromeDriverManager().install())


title_lis = []
url_lis = []
address_lis = []
dev_lis = []
year_lis = []
price_lis = []
public_price_lis = []
area_lis = []
total_condo_lis = []
total_floor_lis =[]
total_unit_lis = []
park_area_lis = []
lat_lis = []
long_lis = []


count = 0
for i in range(start_page,end_page+1):
    
    url = "https://th.zmyhome.com/project/condo?page={}&sortFilter=yearnew&per-page=40".format(start_page,end_page)
    
    driver.get(url)
    print(driver.page_source)

    soup = BeautifulSoup(driver.page_source,'html.parser')
    
    lis = ["https://th.zmyhome.com/"+i.find('a')['href'] for i in soup.find_all('div',{'class':'card_project__head-detail'})]
    for link in lis: 
        driver.get(link)
        
        
        soupx = BeautifulSoup(driver.page_source,'html.parser')

        #ชื่อโครงการ
        title = driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div/div/div/div/h2")
        print(title.text)
        title_lis.append(title.text.strip())

        url_lis.append(link)
        print(link)

        address = driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div/div/div/div/h5/span[2]")
        print(address.text)
        address_lis.append(address.text.strip())
    
        project_detail_item_lis = [ d.find('strong').text.strip() for d in soupx.find("ul",{'class':'info-project__list'}).find_all('li')]
        dev_lis.append(project_detail_item_lis[0].strip())
        print(project_detail_item_lis[0].strip())

        year_lis.append(project_detail_item_lis[1].strip())
        print(project_detail_item_lis[1].strip())

        price_lis.append(project_detail_item_lis[2].strip())
        print(project_detail_item_lis[2].strip())

        public_price_lis.append(project_detail_item_lis[3].strip())
        print(project_detail_item_lis[3].strip())

        area_lis.append(project_detail_item_lis[4].strip())
        print(project_detail_item_lis[4].strip())

        total_condo_lis.append(project_detail_item_lis[5].strip())
        print(project_detail_item_lis[5].strip())

        total_floor_lis.append(project_detail_item_lis[6].strip())
        print(project_detail_item_lis[6].strip())

        total_unit_lis.append(project_detail_item_lis[7].strip())
        print(project_detail_item_lis[7].strip())

        park_area_lis.append(project_detail_item_lis[8].strip())
        print(project_detail_item_lis[8].strip())

        lat_long = soupx.find('div',{'id':'map'}).find('iframe')['src']
        print(lat_long)

        lat_long_lis = lat_long.split(",")
        lat = lat_long_lis[0].split("&q=")[1]
        print("Lat : ",lat)
        lat_lis.append(lat)

        long = lat_long_lis[1]
        print("Long : ",long)
        long_lis.append(long)
   

    print(lis)

time.sleep(2)


df = pd.DataFrame()

df['ชื่อโครงการ'] = title_lis 
df['ลิงค์'] = url_lis 
df['ที่อยู่เต็ม'] = address_lis 
df['ผู้พัฒนา'] = dev_lis 
df['ปีทีสร้างเสร็จ'] = year_lis 
df['ราคาเปิดตัว'] = price_lis 
df['ค่าส่วนกลาง'] = public_price_lis
df['พื้นที่โครงการ'] = area_lis 
df['จำนวนตึก'] = total_condo_lis 
df['จำนวนชั้น'] = total_floor_lis 
df['ยูนิตทั้งหมด'] = total_unit_lis
df['พื้นที่จอดรถ'] = park_area_lis 
df['Latitude'] = lat_lis 
df['Longtitude'] = long_lis

df.to_excel(filename)

print("All Done")