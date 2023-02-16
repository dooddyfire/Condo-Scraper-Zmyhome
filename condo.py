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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
fac_lis = []
google_map_lis = []
rec_lis = []
prov_lis = []
amphor_lis = []
#tel_lis = []
#web_lis = []
count = 0
for i in range(start_page,end_page+1):
    
    url = "https://th.zmyhome.com/project/condo?page={}&sortFilter=yearnew&per-page=40".format(start_page,end_page)
    
    driver.get(url)
    print(driver.page_source)

    soup = BeautifulSoup(driver.page_source,'html.parser')
    prov_amphor_lis = [ p.find("small").text.split(",") for p in soup.find_all('div',{'class':'card_project__head-detail'})]
    for g in prov_amphor_lis:
        prov_lis.append(g[1])
        amphor_lis.append(g[0])
    print(prov_amphor_lis)
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
        google_map_lis.append(lat_long)
        print(lat_long)

        lat_long_lis = lat_long.split(",")
        lat = lat_long_lis[0].split("&q=")[1]
        print("Lat : ",lat)
        lat_lis.append(lat)

        long = lat_long_lis[1]
        print("Long : ",long)
        long_lis.append(long)
        
        try:
            print(soupx.find('div',{'class':'facality'}))
      
            fac = [ i.text.strip() for i in soupx.find('div',{'class':'facality'}).find_all('span',{'class':'label'})]
            fac_info = ",".join(fac)
            fac_lis.append(fac_info)
        except:
            print("ไม่มี")
            fac_lis.append("ไม่มี")

        card_proj = [ x.text.strip() for x in soupx.find_all('div',{'class':'nearby-place__list__item'})]
        print(card_proj)
        card_proj_item = ",".join(card_proj)
        rec_lis.append(card_proj_item)

        viewClass = '//*[@id="contactOwner"]'
        driver.execute_script("arguments[0].click();", WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, viewClass))))

        """
        contact_ownder_lis = soupx.find('ul',{'class':'contact-owner'}).find_all('contact-owner__list')
        print(contact_ownder_lis)
        tel = contact_ownder_lis[0].text
        print(tel)
        tel_lis.append(tel)

        web = contact_ownder_lis[1].text 
        print(web)
        web_lis.append(web)
        """

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
df['Facility'] = fac_lis 
df['Google Map'] = google_map_lis
df['สถานที่ใกล้เคียง'] = rec_lis 
df['เขต'] = amphor_lis 
df['จังหวัด'] = prov_lis 
#df['Web'] = web_lis
#df['โทร'] = tel_lis


df.to_excel(filename)

print("All Done")