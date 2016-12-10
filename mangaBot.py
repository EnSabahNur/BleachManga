import requests
from bs4 import BeautifulSoup as bs4
import urllib.request

url_base = "http://www.mangareader.net/"
start_url = "http://www.mangareader.net/bleach/1"

def numOfPage(soup):
	return int(soup.find_all('div',{'id':'selectpage'})[0].text.split(' of ')[-1])

def downloadImg(url,filename):
	urllib.request.urlretrieve(url, filename+".jpg")
	
def processPage(url,dosya):
	soup_page = bs4(requests.get(url).content,'html.parser')
	url = soup_page.find_all('img',{'id':'img'})[0].get('src')
	dosya.writelines(url+"\n")
	#downloadImg(url,str(page_num))
	
def processChapter(url,dosya):
	soup_page = bs4(requests.get(url).content,'html.parser')
	num = numOfPage(soup_page)
	for i in range(1,num+1):
		processPage(url,dosya)
		soup_page = bs4(requests.get(url).content,'html.parser')
		n = soup_page.find_all('span',{'class':'next'})[0].select('a')[0].get('href')
		url = url_base+n[1:]
		
def processAll(url):
	global url_base
	soup_page = bs4(requests.get(url).content,'html.parser')
	table = soup_page.find_all('table',{'id':'listing'})
	chapters = table[0].select('a')
	chapNum = len(chapters)
	for i in range(1,chapNum+1):
		url = url_base + chapters[i-1].get('href')[1:]
		dosya = open("%s.txt"%str(chapters[i-1].text),"w")
		processChapter(url,dosya)
		dosya.close()
	
	





processAll("http://www.mangareader.net/bleach")
#s = bs4(requests.get(start_url).content,'html.parser')
#print(numOfPage(s))


