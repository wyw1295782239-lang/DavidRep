import requests
import csv
import json

headers = {
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "content-type": "application/json",
    "cookieorigin": "https://you.ctrip.com",
    "dnt": "1",
    "origin": "https://you.ctrip.com",
    "priority": "u=1, i",
    "referer": "https://you.ctrip.com/",
    "sec-ch-ua": "\"Not:A-Brand\";v=\"99\", \"Microsoft Edge\";v=\"145\", \"Chromium\";v=\"145\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36 Edg/145.0.0.0",
    "x-ctx-ubt-pageid": "10650142842",
    "x-ctx-ubt-pvid": "6",
    "x-ctx-ubt-sid": "7",
    "x-ctx-ubt-vid": "1750687440581.27c8JaTrbuHt",
    "x-ctx-wclient-req": "334107c4197b9cf8065194bf0fdd3343"
}
cookies = {
    "GUID": "09031123416958489774",
    "UBT_VID": "1750687440581.27c8JaTrbuHt",
    "_RF1": "61.144.19.214",
    "_RSG": "S3q2_P3lDy1uQy5SFrsc8A",
    "_RDG": "28704d09e38bce2af9325a3be4c5f0089f",
    "_RGUID": "1f0dbc36-7f0b-40dc-a226-db53dc17c6b8",
    "MKT_CKID": "1771681489697.y25ao.lar0",
    "_ga": "GA1.1.1438030392.1771681490",
    "MKT_Pagesource": "PC",
    "nfes_isSupportWebP": "1",
    "Hm_lvt_a8d6737197d542432f4ff4abc6e06384": "1771681489,1772269453,1772337608",
    "HMACCOUNT": "74734FC930825B65",
    "_abtest_userid": "87822216-78d5-4e01-bff1-7df5e2573598",
    "cticket": "1A93B550E9090E11D0104AFC1EAD76A9D4FF9AB0C4E53EB7DA330A1CEB49417A",
    "login_type": "0",
    "login_uid": "FD3D65927FF3B3ADC33378FE612537D22173D7ABDD0318F145ABBF6BBDF10BE0",
    "DUID": "u=D8B61EAB627848045E01FB2CBFD3C099&v=0",
    "IsNonUser": "F",
    "AHeadUserInfo": "VipGrade=5&VipGradeName=%B0%D7%D2%F8%B9%F3%B1%F6&UserName=&NoReadMessageCount=1",
    "_udl": "708D70C2B179E2F91CC5ED1C2CCE362D",
    "Hm_lpvt_a8d6737197d542432f4ff4abc6e06384": "1772351993",
    "Session": "smartlinkcode=U130727&smartlinklanguage=zh&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=",
    "Union": "AllianceID=4902&SID=130727&OUID=&createtime=1772351993&Expires=1772956792913",
    "_ga_9BZF483VNQ": "GS2.1.s1772351992$o6$g1$t1772351994$j58$l0$h0",
    "_ga_5DVRDQD429": "GS2.1.s1772351993$o6$g1$t1772351994$j59$l0$h2066156698",
    "_ga_B77BES1Z8Z": "GS2.1.s1772351993$o6$g1$t1772351994$j59$l0$h0",
    "_bfa": "1.1750687440581.27c8JaTrbuHt.1.1772351998050.1772352075153.7.6.10650142842",
    "_jzqco": "%7C%7C%7C%7C1772269453788%7C1.1664719815.1771681489700.1772351999923.1772352075757.1772351999923.1772352075757.undefined.0.0.24.24"
}
url = "https://m.ctrip.com/restapi/soa2/18109/json/getAttractionList"
params = {
    "_fxpcqlniredt": "09031123416958489774",
    "x-traceID": "09031123416958489774-1772352094190-8135880"
}
data = '{"head":{"cid":"09031123416958489774","ctok":"","cver":"1.0","lang":"01","sid":"8888","syscode":"999","auth":"","xsid":"","extension":[]},"scene":"online","districtId":1,"index":2,"sortType":1,"count":10,"filter":{"filterItems":[]},"coordinate":{"latitude":22.740120929228908,"longitude":114.11666700942612,"coordinateType":"WGS84"},"returnModuleType":"product"}^:^\\^product^^^}^'.encode('unicode_escape')
response = requests.post(url, headers=headers, cookies=cookies, params=params, data=data)



def get_json(k,y,page):
    data = {
        "head": {
            "cid": "09031123416958489774",
            "ctok": "",
            "cver": "1.0",
            "lang": "01",
            "sid": "8888",
            "syscode": "999",
            "auth": "",
            "xsid": "",
            "extension": []
        },
        "scene": "online",
        "districtId": y,
        "index":pages,
        "sortType": 1,
        "count": 10,
        "filter": {
            "filterItems": []
        },
        "coordinate": {
            "latitude": 22.740003800985107,
            "longitude": 114.1166136872802,
            "coordinateType": "WGS84"
        },
        "returnModuleType": "product"
    }
    data = json.dumps(data, separators=(',', ':'))
    response = requests.post(url, headers=headers, cookies=cookies, params=params, data=data)


    return response.json()


def get_data_info(resp,k, visited_poi_ids):
    feeds = resp.get("attractionList",[])

    with open('data.csv','a',newline='',encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        rows = []
        for feed in feeds:
            card = feed.get("card",{})
            coordinate =card.get("coordinate",{})

            zoneName = card.get('zoneName','')#景点区域
            poiId = card.get("poiId",'')#景点id

            # 检查poiId是否已存在，避免重复
            if poiId and poiId not in visited_poi_ids:
                visited_poi_ids.add(poiId)
                poiName = card.get("poiName",'')#景点名称
                commentCount = card.get("commentCount",'')#评论数量
                CommentScore = card.get("commentScore",'')#评分
                isAdvertisement = card.get("isAdvertisement",'')#是否为广告内容
                isRecommand = card.get("isRecommend",'')#是否被推荐
                districtName = card.get("districtName",'')#城市名称
                CoverImageUrl = card.get("coverImageUrl",'')#图片
                distanceStr = card.get("distanceStr",[])#与市中心的距离
                tagNameList = card.get("tagNameList",[])#标签
                detailUrl = card.get("detailUrl",[])#详情页链接
                MarketPrice = card.get("marketPrice",'')#市场票价
                marketDiscountPrice=card.get("marketDiscountPrice",[])
                preferentialDesc = card.get("preferentialDesc",'')#优惠描述
                price =card.get("price",[])#价格
                priceType = card.get("priceType",'')#价格类型
                priceTypeDesc = card.get("priceTypeDesc",'')#价格类型描述
                isFree = card.get("isFree",'')#是否免费
                latitude = coordinate.get("latitude")#精度
                longitude=coordinate.get("longitude")#纬度
                heatScore = card.get("heatScore",'')#热度评分

                rows.append(
                [poiId,zoneName,poiName,commentCount,CommentScore,isAdvertisement,
                isRecommand,districtName,CoverImageUrl,distanceStr,tagNameList,detailUrl,MarketPrice,marketDiscountPrice,preferentialDesc,price,priceType,
                priceTypeDesc,isFree,latitude,longitude,heatScore,k])
                print(zoneName)
        csvwriter.writerows(rows)

if __name__ == '__main__':
        # 清空data.csv文件
        with open('data.csv','w',newline='',encoding='utf-8') as csvfile:
            pass
        # 创建一个集合来存储已访问的poiId，用于去重
        visited_poi_ids = set()

        citydic = {
            "北京": 1,
            "上海":2,
            "天津":3,
            "重庆":4,
            "海南":100001,
            "西藏":100003,
            "云南":100007,
            "新疆":100008,
            "四川":100009,
            "福建":100038,
            "山东":100039,
            "广东":100051,
            "广西":100052,
            "湖南":100053,
            "江西":100054,
            "黑龙江":100055,
            "山西":100056,
            "内蒙古":100062,
            "甘肃":100060,
            "宁夏":100063,
            "贵州":100064,
            "浙江":100065,
            "河南":100058,
            "河北":100059,
            "辽宁":100061,
            "江苏":100066,
            "湖北": 100067,
            "安徽":100068,
            "台湾":100076,
            "吉林":100031,
            "青海":100032,
            "陕西":100057,
        }
        for k ,y in citydic.items():
            for pages in range(1,16):
                resp = get_json(k,y,pages)
                get_data_info(resp,k, visited_poi_ids)
