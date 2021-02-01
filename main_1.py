#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver 
# from bs4 import BeautifulSoup
import pandas as pd
import time


# In[2]:


# link="http://www.csa-ma.com.br/"
link2='http://www.csa-ma.com.br/blog-2/'

# abrindo o browser na aba de interesse,
options_ = webdriver.ChromeOptions() 
options_.add_argument("start-maximized")
options_.add_argument('disable-infobars')
browser=webdriver.Chrome(options=options_, executable_path='./chromedriver')

browser.get(link2)

# algumas vezes é necessario esperar carregar tudo na pagina antes de peggar as informações
time.sleep(2)

# pagina=browser.page_source


# loop para carregar mais elementos da pagina
# caminho do botão de carregar mais elementos
cam='//*[@id="main"]/div[2]/div[1]/div/div[1]/div[1]/div[4]/div/a'
while True:
    try:
        # o loop procura elementos até que não exista mais a opção
        carregar_mais=browser.find_element_by_xpath(cam)
        time.sleep(2)
        carregar_mais.click()
        time.sleep(2)
    except Exception as e:        
        print(e)
        break
        
# finalizando o browser
# browser.quit()
# print(pagina)


# In[3]:


# Pegar as informações de título, data de postagem, resumo e url da imagem de forma programática;
# xpath do titulo, se altera apenas no div do caracter de posição 60
titulo ='//*[@id="main"]/div[2]/div[1]/div/div[1]/div[1]/div[2]/div[1]/div/div[2]/div/div[1]/h3/a'
# xpath da data, se altera apenas no div do caracter de posição 60
data ='//*[@id="main"]/div[2]/div[1]/div/div[1]/div[1]/div[2]/div[1]/div/div[2]/div/div[2]/div/p'
# xpath do resumo, se altera apenas no div do caracter de posição 60
resumo='//*[@id="main"]/div[2]/div[1]/div/div[1]/div[1]/div[2]/div[7]/div/div[2]/div/div[4]/p[2]'
# a partir do resumo de numero 7 o xpath muda, logo foi necessario colocar essa possibilidade de acesso
resumo_alt='//*[@id="main"]/div[2]/div[1]/div/div[1]/div[1]/div[2]/div[7]/div/div[2]/div/div[4]/p'
# xpath da url da imagem, se altera apenas no div do caracter de posição 60
url= '//*[@id="main"]/div[2]/div[1]/div/div[1]/div[1]/div[2]/div[1]/div/div[1]/div/img'


# In[4]:




# pegamos os elementos para serem capturados
# elementos=[titulo_a, data_a, resumo_a,url_a]
def pega_elementos(a,b,c,d):
    elementos=[a,b,c,d]
    aux=list()
    for i in elementos:
        if elementos.index(i)!=3:
            # os tres primeiros elementos podem ser acessados de maneira simplificada, 
            txt=aux.append(browser.find_element_by_xpath(i).text)
        else:
            # a url da imagem é acessada de maneira diferente 
            try:
                # foi necessario colocar dois tipos de modos de acesso,aqui, pois em algumas situações a noticia não possui imagem, logo não retorna nada
                txt=aux.append(browser.find_element_by_xpath(i).get_attribute('src'))
            except Exception as e:
                print(e)
                txt=aux.append("Sem imagem")
                
    return aux


# In[5]:


# criar uma função que corta a string, e retorna com o valor atualizado 

def string_atualizada(string_completa, posicao, num):
    # string completa é a string que sera alterada
    # posicao que o sistema sera atualizado
    # num é o numero a ser inseriod
    return (string_completa[:posicao-1]+str(num+1)+string_completa[posicao:])


# In[6]:



aux2=list()
for i in range(120):
    tit=string_atualizada(titulo,60,i)
    dat=string_atualizada(data,60,i)
    res=string_atualizada(resumo,60,i)
    res2=string_atualizada(resumo_alt,60,i)
    ur=string_atualizada(url,60,i)
    
    try:
        teste_loop= pega_elementos(tit, dat, res,ur)
        print(i,'norm')
    except Exception as e:
        
        print(i, "res_alt")
        teste_loop= pega_elementos(tit, dat, res2,ur)
#         colocar um except aqui para ver qaul foi o ultimo que deu certo

    if i:
        # fazer coisas normais
        
        df2 = pd.DataFrame(
        {
            "titulo": teste_loop[0],
            "data": teste_loop[1],
            "resumo": teste_loop[2],
            "url": teste_loop[3]
        },
        index=[i], 
        )
        df1=pd.concat([df1,df2])

#         print("top")
#         print(res)
    
    else:
#         elementos=['titulo', 'data', 'resumo','url']
        df1 = pd.DataFrame(
        {
            "titulo": teste_loop[0],
            "data": teste_loop[1],
            "resumo": teste_loop[2],
            "url": teste_loop[3]
        },
        index=[i], 
        )
    
browser.quit()


# In[7]:


# transformar o dataframe em um arquivo no formato csv
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_csv.html
# df.to_csv(r'Path where you want to store the exported CSV file\File Name.csv', index = False)
df1.to_csv(r'df2.csv',index=False)


# In[8]:


# df1


# In[ ]:




