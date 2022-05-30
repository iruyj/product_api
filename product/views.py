import json

import xmltodict as xmltodict
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
import requests
import xmltodict # Create your views here.

# 전역변수
datalist = []   # 검색 후 가져온 데이터 임시저장
chklist = []    # 스타일 현재목록 저장

# 전체 리스트 가져오기
def getlist(keyword):
    global datalist
    key = "1f3540984e07f196b3f6fb67bc169e46"    # api 연동키
    url = f"http://openapi.11st.co.kr/openapi/OpenApiService.tmall?key={key}&apiCode=ProductSearch&keyword={keyword}"
    req = requests.get(url)
    xmldata = req .content.decode('cp949')
    data = json.loads(json.dumps(xmltodict.parse(xmldata), indent=4))
    used = []
    # 사용하는 값만 따로 저장하기
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
    datalist = used

# 필터링 후 렌더링
def filtering(request, type):   # 0:이름순, 1:인기순, 2:낮은가격순, 3:높은가격순
    global datalist,chklist
    # 체크표시를 해줄 클래스 지정
    getChecklist(type)
    page = request.GET.get('page', '1')
    paginator = Paginator(datalist, '9')
    page_obj = paginator.page(page)
    return render(request,'product/list.html',context={'datas': page_obj, 'chkclass':chklist })

# 필터링 기준에 따른 정렬&스타일 가져오기
def getChecklist(type):
    checklist = {'rating': '', 'name': '', 'pricedown': '', 'priceup': ''}
    if type == 0:
        checklist['rating'] = 'check'
        datalist.sort(key=lambda x: int(x['Rating']), reverse=True)
    elif type == 1:
        checklist['name'] = 'check'
        datalist.sort(key=lambda x: x['ProductName'])
    elif type == 2:
        checklist['pricedown'] = 'check'
        datalist.sort(key=lambda x: int(x['ProductPrice'][:-4]+x['ProductPrice'][-3:]))
    elif type == 3:
        checklist['priceup'] = 'check'
        datalist.sort(key=lambda x: int(x['ProductPrice'][:-4]+x['ProductPrice'][-3:]), reverse=True)
    global chklist
    chklist = checklist

# 개별 항목 가져오기
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
    used['AddImage1'] = data['Product']['AddImage1'] if 'AddImage1' in data['Product'].keys() else None # img url
    used['AddImage2'] = data['Product']['AddImage2'] if 'AddImage2' in data['Product'].keys() else None # img url
    used['AddImage3'] = data['Product']['AddImage3'] if 'AddImage3' in data['Product'].keys() else None # img url
    used['Point'] = data['Product']['Point']  # 적립 포인트
    used['Chip'] = data['Product']['Chip']  #
    used['Installment'] = data['Product']['Installment']  # 무이자 할부 정보
    used['ShipFee'] = data['Product']['ShipFee']  # 배송비 정보
    used['SellSatisfaction'] = data['Product']['SellSatisfaction']  # 판매 만족도 정보
    used['SellGrade'] = data['Product']['SellGrade']  # 판매 등급
    # print(data.keys())
    used['OptionList'] = []
    status = ''
    if ('ProductOption' in data.keys()) and data['ProductOption']['Option'] == 'Y':
        used['OptionList'] = data['ProductOption']['OptionList']['Option']['ValueList']['Value']  # 옵션 리스트
        status = data['ProductOption']['status']    # 상품 품절 여부

    # ['ProductCode', 'ProductName', 'ProductPrice', 'BasicImage', 'ImageL300', 'Point', 'Chip', 'Installment', 'ShipFee',
    #  'SellSatisfaction', 'SellGrade']
    # http://openapi.11st.co.kr/openapi/OpenApiService.tmall?key='open api key'&apiCode=ProductInfo&productCode='상품번호'&option=PdOption
    return used, status

# main 화면으로 이동하는 함수
def index(request):
    global datalist, chklist
    kw = request.GET.get('kw','')
    getlist(kw) # 데이터 가져오기
    page = request.GET.get('page', '1')
    paginator = Paginator(datalist, '9')
    page_obj = paginator.page(page)
    # ProductName , ProductImage300, ProductPrice, Seller, Rating(5점만점)
    return render(request,'product/list.html',context={'datas': page_obj, 'chkclass':chklist })

# 디테일 화면으로 이동하는 함수
def detail(request, code):
    datas, status = getProduct(code)
    return render(request, 'product/detail.html',context={'datas':datas, 'status':status})
