#!/usr/bin/python3
import requests,re,bs4
url="https://www.imooc.com/course/list"
req=requests.get(url)
req.encoding="UTF-8"
soup=bs4.BeautifulSoup(req.text,'lxml')
li=soup.find_all("li",class_="course-nav-item ")
lb=[]#方向+类别，结构：名称 链接'
for index in range(len(li)):
    lb.append([li[index].text,li[index].a.get('href')])
def deal(str):
    r=requests.get(url+str)
    r.encoding="UTF-8"
    soup=bs4.BeautifulSoup(r.text,'lxml')
    pages=soup.find_all('div',class_='page')
    m=len(pages[0].find_all('a')) 
    cons=[]
    for k in range(1,m+2):
        re=requests.get(url+str+"&page=%d" %(k))
        re.encoding="UTF-8"
        soup=bs4.BeautifulSoup(re.text,'lxml')
        contex=soup.find_all('div',class_="course-card-container")
        #用于第一个链接具体内容，结构：课程名 等级 人数 时长 分数 备注 链接
        for index in range(len(contex)):
            spans=contex[index].find_all('span')
            rs=requests.get('https://www.imooc.com'+contex[index].a.get('href'))
            s=bs4.BeautifulSoup(rs.text,'lxml')
            lon=s.find_all('div',class_='static-item l')
            grade=s.find('div',class_='static-item l score-btn')
            cons.append([contex[index].h3.text,spans[0].text,spans[1].text,lon[2].find_all('span',class_="meta-value")[0].text,grade.find_all('span',class_="meta-value")[0].text,contex[index].p.text,contex[index].a.get('href')])
    return cons
