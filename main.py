#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver 
from bs4 import BeautifulSoup
import pandas as pd
import time


# In[2]:


options = webdriver.ChromeOptions() 
options.add_argument("start-maximized")
browser1=webdriver.Chrome(options=options, executable_path='./chromedriver')

link="http://www.csa-ma.com.br/"
browser1.get(link)
xpath_botao='//*[@id="nav-item-1579"]/a'
link2=(browser1.find_element_by_xpath(xpath_botao).get_attribute('href'))
browser1.quit()
# print(link2)


# In[3]:



# abrindo o browser na aba de interesse,
# options = webdriver.ChromeOptions() 
# options.add_argument("start-maximized")
# options.add_argument('disable-infobars')
browser=webdriver.Chrome(options=options, executable_path='./chromedriver')

browser.get(link2)

# esperar carregar pag antes de peggar as informações
time.sleep(2)


# carregar mais elementos da pagina

cam='//*[@id="main"]/div[2]/div[1]/div/div[1]/div[1]/div[4]/div/a'
while True:
    try:
        carregar_mais=browser.find_element_by_xpath(cam)
        time.sleep(2)
        carregar_mais.click()
        time.sleep(2)
    except Exception as e:        
        print(e)
        break

# finalizando o browser

pagina=browser.page_source
browser.quit()        

# print(pagina)


# In[4]:


soup=BeautifulSoup(pagina, 'html.parser')
print(soup.prettify())
with open("arquivo.txt",'w' ) as file:
    file.write(soup.prettify())


# In[5]:



resumos=[i.text for i in soup.find_all('div', class_="post-excerpt")]
titulos=list()
datas=list()
links=list()
for artig in soup.find_all('div', class_='isotope-item post'):
        titulos.append(artig.h3.a.text)    
        datas.append(artig.p.text)
        try:
            links.append(artig.find('img')['src'])
        except Exception as e:
            links.append("sem imagem")


# In[6]:


df1 = pd.DataFrame(
        {
            "Titulo": titulos,
            "Data": datas,
            "Resumo": resumos,
            "URL": links
        })
df1.to_csv(r'df1.csv',index=False)


# In[7]:


# df1['URL']


# In[ ]:




