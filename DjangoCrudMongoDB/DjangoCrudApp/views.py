from bson import ObjectId
from django.http import HttpResponse
from django.shortcuts import render
import json

# Create your views here.
from DjangoCrudApp.models import Posts
from django.views.decorators.csrf import csrf_exempt
import requests
from bs4 import BeautifulSoup
import re
import html as ihtml
import time
import threading

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36' }

pagesUrls = []

pageNumbers = []

materialInfos = []

domainName = 'https://www.migros.com.tr'

def getCategory():
    r = requests.get(domainName, headers=headers)

    soup = BeautifulSoup(r.text, 'html.parser')

    categories = soup.find('div', {'class': 'header-menu-bar'}).find('ul', {'class': 'header-menu-bar-list'}).find_all(
        'li', {'class': 'category-list-item category-title'})

    #Domain namede catgory isimlerini cekip her katergori sayfalarini geziyor.
    for item in categories:
        # Kaategori urli olusturuldu.
        ctgUrl = domainName + item.find('a')['href']
        # Kateri urlnden veriler cekilmek uzere fonksiyona gitti
        getMaterialInfos(ctgUrl)
        print(materialInfos)
        materialInfos.clear()

    return


def getMaterialInfos(searchMaterial):
    time.sleep(1)
    url2 = searchMaterial
    r = requests.get(url2, headers=headers)

    soup = BeautifulSoup(r.text, 'html.parser')

    pagePaginationInfos = soup.find('nav', {'class': 'page-nav'}).find('ul', {'class': 'pagination'}).find_all('li')

    sayac = 0
    # Alinan kategrinin kac sayfa malzemeden olustugu bulunuyor.
    for item in pagePaginationInfos:
        sayac = sayac + 1
        if len(pagePaginationInfos) > sayac:
            if item.find('a'):
                if item.find('a').find('span'):
                    spanRemove = item.find('a')
                    spanRemove.span.decompose()
                urlsInfo = {
                    int(item.find('a').text)
                }
                pagesUrls.append(urlsInfo)
                #print(urlsInfo)

    sayfaSayisi = 1
    loopValue = True
    # Sayfa sayilarinin urlleri olusturulup malzeme bilgileri alinmak uzere fonksiyon cagiriliyor
    while loopValue:
        if len(pagesUrls) > 1:
            pageNumbers.append({sayfaSayisi})
            if pageNumbers[len(pageNumbers) - 1] == pagesUrls[len(pagesUrls) - 1]:
                tempPageUrl = url2 + '?sayfa=' + str(sayfaSayisi)
                getInfo(tempPageUrl)
                loopValue = False
            else:
                if len(pagesUrls) == 1:
                    getInfo(url2)
                else:
                    tempPageUrl = url2 + '?sayfa=' + str(sayfaSayisi)
                    getInfo(tempPageUrl)
                    sayfaSayisi = sayfaSayisi + 1

        else:
            loopValue = False
            getInfo(url2)

    pageNumbers.clear()
    pagesUrls.clear()

    return


def getInfo(url):
    tempUrl = url
    r = requests.get(tempUrl, headers=headers)

    soup = BeautifulSoup(r.text, 'html.parser')
    generalInfo = soup.find_all('div', {'class': 'product-card product-action'})

    # Html kodlarindan malzeme modelleri olusturuluyor
    for item in generalInfo:
        post = Posts(
            product_name=item.find('h5', {'class': 'title product-card-title'}).find('a', {}).text,
        )
        post.save()

    time.sleep(2)

@csrf_exempt
def add_post(request):
    url = 'http://193.53.98.38:8310/oauth/token'
    authInfo = {"username": "ADMIN", "password": "KALEM1453!@" }
    connectUrl = requests.post(url, data= json.dumps(authInfo), headers = {'Authorization': 'Basic UFJPVklERVI6MTIzNDU2Nzg='})

    return print(connectUrl.json())

def update_post(request, id):
    post = Posts.objects.get(_id=ObjectId(id))
    post.price = request.POST.get('price')
    post.save()
    return HttpResponse("Post Updated")

def delete_post(request):
    return HttpResponse('Inserted')

def read_post(request, id):
    post=Posts.objects.get(_id=ObjectId(id))
    stringVal = "Baslik : " + post.title + "Price : " + post.price +"Img : " + post.img + "<br>"
    return HttpResponse(stringVal)

def read_post_all(request):
    posts = Posts.objects.all()
    stringVal = ""
    for post in posts:
        stringVal = "Baslik : " + post.title + "Price : " + post.price + " URL :  " + post.img + "<br>"

    return HttpResponse(stringVal)
