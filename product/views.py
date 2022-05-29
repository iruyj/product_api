import json

import xmltodict as xmltodict
from django.shortcuts import render, redirect
import requests
import xmltodict # Create your views here.
def getlist(keyword):
    key = "1f3540984e07f196b3f6fb67bc169e46"
    url = f"http://openapi.11st.co.kr/openapi/OpenApiService.tmall?key={key}&apiCode=ProductSearch&keyword={keyword}"
    req = requests.get(url)
    xmldata = req.content.decode('cp949')
    data = json.loads(json.dumps(xmltodict.parse(xmldata), indent=4))
    used = []
    # data = json.loads(jsonData)
    # print(data['ProductSearchResponse']['Products']['Product'])
    print('길이',len(data['ProductSearchResponse']['Products']['Product']))
    for product in data['ProductSearchResponse']['Products']['Product']:
        # ProductName , ProductImage300, ProductPrice, Seller, Rating(5점만점)
        temp = {}
        temp['ProductName'] = product['ProductName']
        temp['ProductImage'] = product['ProductImage300']
        temp['ProductPrice'] = product['ProductPrice'][:-3]+','+product['ProductPrice'][-3:]
        temp['ProductCode'] = product['ProductCode']
        temp['Seller'] = product['Seller']
        temp['Rating'] = product['Rating']
        used.append(temp)
        # print(product.keys())
        # print('\n\n')
    # data key 목록
   #  ['ProductCode', 'ProductName', 'ProductPrice', 'ProductImage', 'ProductImage100', 'ProductImage110',
   # 'ProductImage120', 'ProductImage130', 'ProductImage140', 'ProductImage150', 'ProductImage170',
   # 'ProductImage200', 'ProductImage250', 'ProductImage270', 'ProductImage300', 'Text1', 'Text2',
   # 'SellerNick', 'Seller', 'SellerGrd', 'Rating', 'DetailPageUrl', 'SalePrice', 'Delivery', 'ReviewCount',
   # 'BuySatisfy', 'MinorYn', 'Benefit']
   #  datas = data['ProductSearchResponse']['Products']['Product']
    return used

def getProduct(productCode):
    key = "1f3540984e07f196b3f6fb67bc169e46"
    url = f"http://openapi.11st.co.kr/openapi/OpenApiService.tmall?key={key}&apiCode=ProductInfo&productCode={productCode}&option=PdOption"
    req = requests.get(url)
    xmldata = req.content.decode('cp949')
    datas = json.loads(json.dumps(xmltodict.parse(xmldata), indent=4))
    data = datas['ProductInfoResponse']
    used = {}
    used['ProductCode'] = data['Product']['ProductCode']    # ProductCode
    used['ProductName'] = data['Product']['ProductName']    # ProductName
    used['ProductPrice'] = data['Product']['ProductPrice']  # {Price, LowestPrice}
    used['BasicImage'] = data['Product']['BasicImage']  # img url
    used['Point'] = data['Product']['Point']  # 적립 포인트
    used['Chip'] = data['Product']['Chip']  #
    used['Installment'] = data['Product']['Installment']  # 무이자 할부 정보
    used['ShipFee'] = data['Product']['ShipFee']  # 배송비 정보
    used['SellSatisfaction'] = data['Product']['SellSatisfaction']  # 판매 만족도 정보
    used['SellGrade'] = data['Product']['SellGrade']  # 판매 등급
    print(data.keys())
    used['OptionList'] = []
    status = ''
    if ('ProductOption' in data.keys()) and data['ProductOption']['Option'] == 'Y':
        used['OptionList'] = data['ProductOption']['OptionList']['Option']['ValueList']['Value']  # 옵션 리스트
        status = data['ProductOption']['status']    # 상품 품절 여부

    print('데이터길이' ,data['Product'].keys())
    print(data)
    # ['ProductCode', 'ProductName', 'ProductPrice', 'BasicImage', 'ImageL300', 'Point', 'Chip', 'Installment', 'ShipFee',
    #  'SellSatisfaction', 'SellGrade']
    # http://openapi.11st.co.kr/openapi/OpenApiService.tmall?key='open api key'&apiCode=ProductInfo&productCode='상품번호'&option=PdOption
    return used, status

def search(request):
    return redirect('product:list',"수분크림")
    # return redirect('product:info')


def index(request):
    kw = request.GET.get('kw','')

    datas = getlist(kw)
    # ProductName , ProductImage300, ProductPrice, Seller, Rating(5점만점)
    return render(request,'product/list.html',context={'datas': datas})


def detail(request, code):
    datas, status = getProduct(code)
    return render(request, 'product/detail.html',context={'datas':datas, 'status':status})
