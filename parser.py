# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

f = open('/home/madker4/Документы/курсы пам/Дети и наука/standalone.html','r')
soup = BeautifulSoup(f, 'html.parser')
body = soup.body
store_area = body.find('div', id='storeArea')
wr = open('test', 'w')
wr.write(str(store_area))



