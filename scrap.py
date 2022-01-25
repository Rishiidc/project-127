from os import scandir
from bs4 import BeautifulSoup
import time 
import csv
import requests

starturl = "https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"
time.sleep(10)
starsdata = []
newstarsdata = []

headers = ["Proper Name","Bayer Designation"]

def scrap():
    for i in range(1,50):
        while True:
            time.sleep(10)
            for tr_tag in soup.find_all("tr",attrs={"class","headerSort"}):
                th_tags = tr_tag.find_all("th")
                temp = []
                for index,th_tag in enumerate(th_tags):
                    if index == 0:
                        temp.append(th_tag.find_all("a")[0].contents[0])
                    else:
                        try:
                            temp.append(th_tag.contents[0])
                        except:
                            temp.append("")
                hyperlink_li_tag = th_tags[0]
                temp.append("https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"+hyperlink_li_tag.find_all("a",href=True)[0]["href"])    
                starsdata.append(temp)
    
def extradetails(hyperlink):
    try:
        page = requests.get(hyperlink)
        soup = BeautifulSoup(page.content,"html.parser")
        for tr_tag in soup.find_all("tr",attrs={"class":"fact_row"}):
            td_tags = tr_tag.find_all("td")
            temp = []
            for td_tag in td_tags:
                try:
                    temp.append(td_tag.find_all("div",attrs={"class":"value"})[0].contents[0])
                except:
                    temp.append("")
            newstarsdata.append(temp)
    except:
        time.sleep(1)
        extradetails(hyperlink)

scrap()

for index,data in enumerate(starsdata):
    extradetails(data[2])

finalstarsdata = []
for index,data in enumerate(starsdata):
    npde = newstarsdata[index]
    npde = [elem.replace("\n", "") for elem in npde]
    npde = npde[:7]
    finalstarsdata.append(data+npde)

with open("Starsdata.csv","w") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(headers)
        csvwriter.writerow(finalstarsdata)