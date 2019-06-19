import os
import sys
import urllib.request
import datetime
import time
import json
from config import *
import pandas as pd


def get_request_url(url,client_id='vabkyzx1im', client_secret='NZttREt7fWJ4jat98knMXWcYjGSnNiy468I7rh7x'):
    req = urllib.request.Request(url)
    req.add_header("X-NCP-APIGW-API-KEY-ID", client_id)
    req.add_header("X-NCP-APIGW-API-KEY", client_secret)
    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            print("[%s] Url Request Success" % datetime.datetime.now())
            return response.read().decode('utf-8')
    except Exception as e:
        print(e)
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
        return None


# [CODE 1]

def getGeoData(address):
    base = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode"
    node = ""
    parameters = "?query=%s" % urllib.parse.quote(address)
    url = base + node + parameters

    retData = get_request_url(url)

    if (retData == None):
        return None
    else:
        return json.loads(retData)


def main():
    # 엑셀 읽기
    df = pd.read_csv('주소API 테스트데이터.csv')
    df['위도'] = 0
    df['경도'] = 0
    i = 0
    for id, address,y,x in df.values:
        try:
            jsonResult = getGeoData(address)
        except:
            i = i +1
            continue
        print('index, %d ,검색 주소 : %s'%(i,address))

        if 'addresses' in jsonResult.keys():
            print('총 검색 결과: ', jsonResult['addresses'].__len__())
            if jsonResult['addresses'].__len__() >=1:
                item = jsonResult['addresses'][0]
                print('=======================')
                print('위도: ', str(item['y']))
                print('경도: ', str(item['x']))
                print('=======================')
                #df.iloc[i] = {'ID':id,'주소':address,'위도': float(item['y']), '경도': float(item['x'])}
                y_update = pd.Series([float(item['y'])],name='위도', index=[i])
                x_update = pd.Series([float(item['x'])], name='경도', index=[i])
                df.update(y_update)
                df.update(x_update)

        i = i +1



    df.to_csv('주소_API_결과_데이터.csv')
if __name__ == '__main__':
    main()