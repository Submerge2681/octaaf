from django.shortcuts import render
from .models import Articles
from bs4 import BeautifulSoup
import requests
import re

headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en"
    }

# PTI
pti_national_url = requests.get('https://www.ptinews.com/news/national/', headers = headers)

# ANI
ani_national_url = requests.get('https://aninews.in/category/national', headers = headers)

# CZM
czm_bangalore_url = requests.get('https://bengaluru.citizenmatters.in/', headers = headers)

# TNM
tnm_karnataka_url = requests.get('https://www.thenewsminute.com/section/Karnataka', headers = headers)

# RUT
rut_international_url = requests.get('https://www.reuters.com/world/', headers = headers)

# ALJ
alj_international_url = requests.get('https://www.aljazeera.com/news', headers = headers)


def home(request):

    Nat_Pti = request.GET.get('ptiNat')
    Nat_Ani = request.GET.get('aniNat')
    Loc_Czm = request.GET.get('czmLoc')
    Loc_Tnm = request.GET.get('tnmLoc')
    Int_Alj = request.GET.get('aljInt')
    Int_Rut = request.GET.get('rutInt')

    Nat_Pti = 'True'
    Nat_Ani = 'True'
    Loc_Czm = 'True'
    Loc_Tnm = 'True'
    Int_Alj = 'True'
    Int_Rut = 'True'

    # PTI National
    pulled_pti = BeautifulSoup(pti_national_url.content, 'html.parser')
    articles = pulled_pti.find_all('div', class_= 'section-news-list')
    for i in articles:
        articles_head = i.find('h3').string
        articles_disc = i.find('p').string
        articles_link = "https://www.ptinews.com" + i.find('a', href = True)['href']
        articles_imag = i.find('img', class_='news-list-img')
        if articles_imag == None:
            articles_imag = 'https://upload.wikimedia.org/wikipedia/en/thumb/5/5c/Press_Trust_of_India_logo.svg/601px-Press_Trust_of_India_logo.svg.png?20230227173431'
        else: articles_imag = articles_imag['src']
        test = Articles.objects.filter(Sauce = 'PTI')
        test = [i.Link for i in test]
        if articles_link not in test and len(articles_link) > 15:
            news = Articles(Title = articles_head, Discription = articles_disc, Link = articles_link, Sauce = 'PTI', Thumbnail = articles_imag,)# Favicon = 'https://www.ptinews.com/img/favicon.ico')
            news.save()
    # ANI National
    pulled_ani = BeautifulSoup(ani_national_url.content, 'html.parser' )
    articles = pulled_ani.find_all('figure', class_= 'bottom')
    for i in articles:
        articles_head = i.find('h6').string
        articles_disc = i.find('figcaption').text
        articles_disc = articles_disc.strip()
        articles_link = "https://aninews.in/" + i.find('a', class_= 'read-more', href = True)['href']
        articles_imag = i.find('img', class_="lazy img-responsive")['data-src']
        test = Articles.objects.filter(Sauce = 'ANI')
        test = [i.Link for i in test]
        if articles_link not in test:
            news = Articles(Title = articles_head, Discription = articles_disc, Link = articles_link, Sauce = 'ANI', Thumbnail = articles_imag,)# Favicon = 'https://d3lzcn6mbbadaf.cloudfront.net/static/img/icons/favicon-16x16.png')
            news.save()
    # Citizens Matter Bangalore
    pulled_czm = BeautifulSoup(czm_bangalore_url.content, 'html.parser')
    articles = pulled_czm.find_all('article')
    for i in articles:
        articles_head = i.select('h3 > a')
        articles_head = [j.text for j in articles_head]
        if len(articles_head) < 1:
            continue
        else: articles_head = articles_head[0]
        articles_disc = i.select('p')
        articles_disc = [j.text for j in articles_disc]
        articles_disc = articles_disc[0]
        articles_link = i.find('a', href = True)['href']
        articles_imag = i.find_all('img')
        articles_imag = [j['data-src'] for j in articles_imag]
        articles_imag = articles_imag[0]
        test = Articles.objects.filter(Sauce = 'CZM')
        test = [i.Link for i in test]
        if articles_link not in test:
            news = Articles(Title = articles_head.strip(), Discription = articles_disc, Link = articles_link, Sauce = 'CZM', Thumbnail = articles_imag,)# Favicon = 'https://images.citizenmatters.in/wp-content/uploads/sites/14/2020/07/21155731/cropped-CITIZEN-MATTERS-Bengaluru-Favicon.jpg?strip=all&lossy=1&ssl=1')
            news.save()
    # The News Minute Karnataka
    pulled_tnm = BeautifulSoup(tnm_karnataka_url.content, 'html.parser')
    articles = pulled_tnm.find_all('div', class_='row no-gutters')
    for i in articles:
        articles_head = i.select('h3 > a')
        articles_head = [j.text for j in articles_head]
        if len(articles_head) < 1:
            continue
        else: articles_head = articles_head[0] 
        articles_disc = i.find_all('span', class_='time')
        articles_disc = [j.text for j in articles_disc]
        articles_disc = articles_disc[0]
        articles_link = "https://www.thenewsminute.com" + i.find('a', href = True)['href']
        articles_imag = i.find_all('img')
        articles_imag = [j['src'] for j in articles_imag]
        articles_imag = articles_imag[0]
        test = Articles.objects.filter(Sauce = 'TNM')
        test = [i.Link for i in test]
        if articles_link not in test:
            news = Articles(Title = articles_head, Discription = articles_disc, Link = articles_link, Sauce = 'TNM', Thumbnail = articles_imag,)# Favicon = 'https://www.thenewsminute.com/sites/default/files/favicon.ico')
            news.save()
    # Al Jazeera International
    pulled_alj = BeautifulSoup(alj_international_url.content, 'html.parser')
    articles = pulled_alj.find_all('article')
    for i in articles:
        articles_head = i.select('a > span')
        articles_head = [j.text for j in articles_head]
        articles_head = articles_head[0]
        articles_disc = i.find_all('p')
        articles_disc = [j.text for j in articles_disc]
        articles_disc = articles_disc[0]
        articles_link = "https://www.aljazeera.com" + i.find('a', href = True)['href']
        articles_imag = "https://www.aljazeera.com" + i.find('img', class_='gc__image')['src']
        test = Articles.objects.filter(Sauce = 'ALJ')
        test = [i.Link for i in test]
        if articles_link not in test:
            news = Articles(Title = articles_head, Discription = articles_disc, Link = articles_link, Sauce = 'ALJ', Thumbnail = articles_imag,)# Favicon = 'https://www.aljazeera.com/favicon_aje.ico')
            news.save()
    # Reuters International
    pulled_rut = BeautifulSoup(rut_international_url.content, 'html.parser')
    articles = pulled_rut.find_all('li', class_='story-collection__story__LeZ29')
    for i in articles:
        articles_head = i.select('a')
        articles_head = [j.text for j in articles_head]
        articles_head = " ".join(articles_head)
        articles_disc = i.find_all('p')
        articles_disc = [j.text for j in articles_disc]
        if len(articles_disc) < 1:
            articles_disc = ''
        articles_link = i.select('a', href = True)
        articles_link = [j['href'] for j in articles_link]
        articles_link = "https://www.reuters.com" + articles_link[0]
        articles_imag = i.find_all('img')
        articles_imag  = [j['src'] for j in articles_imag]
        if len(articles_imag) < 1:
            articles_imag = 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/Reuters_Logo.svg/1920px-Reuters_Logo.svg.png'
            articles_disc = articles_disc[0]
        test = Articles.objects.filter(Sauce = 'RUT')
        test = [i.Link for i in test]
        if articles_link not in test:
            news = Articles(Title = articles_head, Discription = articles_disc, Link = articles_link, Sauce = 'RUT', Thumbnail = articles_imag[0],)# Favicon = 'https://www.reuters.com/pf/resources/images/reuters/favicon/favicon-32x32.png?d=144')
            news.save()
    
    #Step 2
    if Loc_Czm == "True" and Loc_Tnm == "True":
        loc_news = Articles.objects.filter(Sauce__in=['CZM','TNM']).order_by('-Tim')
    elif Loc_Czm == "True":
        loc_news = Articles.objects.filter(Sauce = 'CZM').order_by('Tim')
    elif Loc_Tnm == "True":
        loc_news = Articles.objects.filter(Sauce = 'TNM').order_by('Tim')
# 
    if Nat_Pti == "True" and Nat_Ani == "True":
        nat_news = Articles.objects.filter(Sauce__in=['PTI','ANI']).order_by('Tim')
    elif Nat_Pti == "True":
        nat_news = Articles.objects.filter(Sauce = 'PTI').order_by('Tim')
    elif Nat_Ani == "True":
        nat_news = Articles.objects.filter(Sauce = 'ANI').order_by('Tim')
# 
    if Int_Alj == "True" and Int_Rut == "True":
        int_news = Articles.objects.filter(Sauce__in=['ALJ','RUT']).order_by('-Tim')
    elif Int_Alj == "True":
        int_news = Articles.objects.filter(Sauce = 'ALJ').order_by('Tim')
    elif Int_Rut == "True":
        int_news = Articles.objects.filter(Sauce = 'RUT').order_by('Tim')
    
    return render(request, 'main.html', {'loc_news':loc_news, 'nat_news':nat_news, 'int_news': int_news})