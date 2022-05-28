import json

import xmltodict as xmltodict
from django.shortcuts import render, redirect
import requests
import xmltodict # Create your views here.
def getlist(request, keyword):
    key = "1f3540984e07f196b3f6fb67bc169e46"
    url = f"http://openapi.11st.co.kr/openapi/OpenApiService.tmall?key={key}&apiCode=ProductSearch&keyword={keyword}"
    req = requests.get(url)
    xmldata = req.content.decode('cp949')
    jsonData = json.dumps(xmltodict.parse(xmldata), indent=4)
    data = json.loads(jsonData)
    print(data['ProductSearchResponse']['Products']['Product'])
    for product in data['ProductSearchResponse']['Products']['Product']:
        print(product)
        print('\n\n')
    return data

def getProduct(request, productCode):
    key = "1f3540984e07f196b3f6fb67bc169e46"
    url = f"http://openapi.11st.co.kr/openapi/OpenApiService.tmall?key={key}&apiCode=ProductInfo&productCode={productCode}&option=PdOption"
    req = requests.get(url)
    xmldata = req.content.decode('cp949')
    jsonData = json.dumps(xmltodict.parse(xmldata), indent=4)
    data = json.loads(jsonData)
    # print(data)
    # http://openapi.11st.co.kr/openapi/OpenApiService.tmall?key='open api key'&apiCode=ProductInfo&productCode='상품번호'&option=PdOption
    return data

def search(request):
    # return redirect('product:list',"수분크림")
    return redirect('product:info')