#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import time

#URL（北海道札幌市の中古マンション）
base_url = 'https://suumo.jp/jj/bukken/ichiran/JJ012FC001/?ar=010&bs=011&sa=01&ta=01&po=0&pj=1&pc=100'
def GetData(url):
	#データ取得
	result = requests.get(url)
	c = result.content
	
	#HTMLを元に、オブジェクトを作る
	soup = BeautifulSoup(c)
	if soup == []:
		print("no soup?")
		return False
	
	#物件リストの部分を切り出し
	bukkenList = soup.find("div",{'id':'js-bukkenList'})
	#print(bukkenList)
	if bukkenList == None:
		print("no bukkenList?")
		return False
		
	#物件リストの情報を取得
	propertyUnit = bukkenList.find_all("div",{'class':"property_unit-body ofh"})
	if propertyUnit == []:
		print("no property_unit?")
		return False	
		
	for unit in propertyUnit:
		dd = unit.find_all("dd")
		for d in dd:
			print(d)
	
		kakaku = str(dd[0].find("span"))
		kakaku = kakaku.replace('<span class="dottable-value">', '')
		kakaku = kakaku.replace('万円</span>', '')
		
		senyuu = str(dd[3])
		senyuu = senyuu.replace('<dd>', '')
		senyuu = senyuu.replace('m<sup>2</sup>', '')
		senyuu = senyuu.replace('</dd>', '')
		senyuu = re.sub(r"（.*）", "", senyuu)
		
		syozaiti = str(dd[1])
		syozaiti = syozaiti.replace('<dd>', '')
		syozaiti = syozaiti.replace('</dd>', '')
	
		barukoni =  str(dd[5])
		barukoni = barukoni.replace('<dd>', '')
		barukoni = barukoni.replace('m<sup>2</sup>', '')
		barukoni = barukoni.replace('</dd>', '')
	
		ensen = str(dd[2])
		ensen = ensen.replace('<dd>', '')
		ensen = ensen.replace('</dd>', '')
		
		tikatetu = 0
		siden = 0
		jr = 0
		
		bus = ""
		toho = ""
		teiho = ""
		
		if ensen.find('地下鉄') != -1 :
			tikatetu = 1
		elif ensen.find('市電') != -1 :
			siden = 1
		elif ensen.find('ＪＲ') != -1 :
			jr = 1
		
		toho_str = re.findall("徒歩\d*分",ensen)
		bus_str = re.findall("バス\d*分",ensen)
		teiho_str = re.findall("停歩\d*分",ensen)
		
		#if bus_str != [] :print(bus_str[0])
		#if toho_str != [] :print(toho_str[0])
		#f teiho_str != [] :print(teiho_str[0])
		
		if toho_str != []:
			toho = toho_str[0].replace('徒歩', '')
			toho = toho.replace('分', '')
		#	print(toho)
		
		if bus_str != []:
			bus = bus_str[0].replace('バス', '')
			bus = bus.replace('分', '')
		#	print(bus)
		
		if teiho_str != []:
			teiho = teiho_str[0].replace('停歩', '')
			teiho = teiho.replace('分', '')
		#	print(teiho)	
		
		madori = str(dd[4])
		madori = madori.replace('<dd>', '')
		madori = madori.replace('</dd>', '')
	
		tikunengetu = str(dd[6])
		tikunengetu = tikunengetu.replace('<dd>', '')
		tikunengetu = tikunengetu.replace('</dd>', '')
		tikunengetu = tikunengetu.replace('年', '/')
		tikunengetu = tikunengetu.replace('月', '')
		
		f = open('UsedApartmentPrice.csv','a')
		f.write(kakaku + "," + senyuu + "," + syozaiti + "," + barukoni + "," + 
				ensen + "," + madori + "," + tikunengetu + "," + 
				str(tikatetu) + "," + str(siden) + "," + str(jr) + ","+
				toho + "," + bus + "," + teiho + "," + "\n")
		f.close()
		
	#しばし待ちます（マナー）
	time.sleep(5)

#ヘッダー作成
f = open('UsedApartmentPrice.csv','w')
f.write("価格" + "," + "占有面積" + "," + "所在地" + "," + "バルコニー" + "," + 
		"沿線・駅" + "," + "間取り" + "," + "築年月" + "," + "地下鉄" + "," +
		"市電" + "," + "ＪＲ" + ","
		"徒歩" + "," + "バス" + "," + "停歩" +"\n")
f.close()

#1ページ目スクレイピング
request_url = base_url
GetData(request_url)
print("1page get!!!")

#2ページ目以降スクレイピング
for i in range(2,26):
	request_url = base_url + "&pn=" + str(i)
	#print(request_url)
	GetData(request_url)
	print(str(i) + "pages get!!!")