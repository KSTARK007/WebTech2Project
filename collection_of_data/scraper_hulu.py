import requests 
from bs4 import BeautifulSoup
import urllib.request

opener=urllib.request.build_opener()
opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
urllib.request.install_opener(opener)

#Types are movies and tv
type = "movies"
#Services are hulu,netflix,amazon,hbo
service = "hulu"
#Change the path to wherever and create image folder
imgpath = "/Users/kiran/OneDrive/Desktop/WT2_Project/images/"+service+"/"+type+"/"

file = open(service+"_"+type+".csv","w")
file.write("Name,Year,Rating,IMDB Rating,RottenTomato Score,Genre1,Genre2,Description\n")


for offset in range(0,500,50): 
	URL = "https://reelgood.com/"+type+"/source/"+service+"?offset="+str(offset)
	print(URL)
	r = requests.get(URL)
	soup = BeautifulSoup(r.content, 'html.parser')
	table = soup.findAll('tr', attrs = {'itemprop':'itemListElement'})

	for row in table:

		link = "https://reelgood.com" + row.find('td',attrs = {'class':'css-1n32qfq'}).a['href']
		req = requests.get(link)
		s = BeautifulSoup(req.content, 'html.parser')
		res = s.find('div', attrs = {'class': 'css-t6u4zk e126mwsw1'})
		try:
			pic_link = res.picture.img['src']
		except Exception as e:
			print("image not found")

		desc = s.find('p', attrs = {'itemprop': 'description'}).text
		desc = "\""+desc+"\""

		genre_meta = s.findAll('meta', attrs = {'itemprop': 'genre'})
		genre1 = genre_meta[0]["content"]
		if len(genre_meta)>=2:
			genre2 = genre_meta[1]["content"]
		genre2 = "N/A"

		movie = row.find('td',attrs = {'class':'css-78jh1y'}).a.text
		if "," in movie:
			continue
		
		movie.replace('?','')
		movie.replace('/','')
		movie.replace('\\','')
		movie.replace(':','')
		movie.replace('*','')
		movie.replace('"','')
		movie.replace('<','')
		movie.replace('>','')
		movie.replace('|','')

		path = imgpath + movie + ".jpg"
		try:
			urllib.request.urlretrieve(pic_link, path)
		except Exception as e:
			print("some error for {} {} \n".format(type,movie))
			continue

		print("saved {} {} \n".format(type,movie))

		meta = row.findAll('td',attrs = {'class':'css-1u11l3y'})
		list = []
		for item in meta:
			list.append(item.text)
		try:
			file.write("{},{},{},{},{},{},{},{}\n".format(movie,list[0],list[1],list[2],list[3],genre1,genre2,desc))
		except Exception as e:
			print("ERROR for " + movie)
			continue

file.close()