from hashlib import md5


def Sign(timestamp,json_data):
    secret="p8hbc7zvurx6ckyzu5hxteyf6ykhky9w"
    s = secret+"json"+json_data+"timestamp"+timestamp+secret
    s_md5 = md5(s.encode('utf8'))
    r_s = s_md5.hexdigest()
    return r_s


if __name__ == "__main__":
    Sign("1583856367" ,"""{"Platform":"TAOBAO","PlatformUserId":"234234234","ReceiverName":null,"ReceiverMobile":null,"ReceiverPhone":null,"ReceiverAddress":null,"BuyerArea":null,"ExtendedFields":{},"Tid":2067719225654838,"Status":"WAIT_BUYER_CONFIRM_GOODS","SellerNick":"测试的店铺","BuyerNick":"西门吹雪","Type":null,"BuyerMessage":null,"Price":"3.00","Num":1,"TotalFee":"3.00","Payment":"3.00","PayTime":"2016-07-11 11:20:20","PicPath":null,"PostFee":null,"Created":"2016-07-11 11:20:09","TradeFrom":null,"Orders":[{"Oid":2067719225654838,"NumIid":45533870790,"OuterIid":"ALDS_1000","OuterSkuId":"ALDS_SKU_1000","Title":"宝贝标题","Price":"3.00","Num":1,"TotalFee":"3.00","Payment":"3.00","PicPath":null,"SkuId":null,"SkuPropertiesName":null,"DivideOrderFee":null,"PartMjzDiscount":null}],"SellerMemo":null,"SellerFlag":0,"CreditCardFee":null}""")



