import requests

def fetch(url, params):
    headers = params['headers']
    body = params['body']
    method = params['method']
    if method == 'GET':
        return requests.get(url, headers=headers)
    if method == 'POST':
        return requests.post(url,headers=headers, data=body)
    
amulets = fetch("https://auto.ru/-/ajax/desktop/listing/", {
  "headers": {
    "accept": "*/*",
    "accept-language": "ru,en;q=0.9",
    "content-type": "application/json",
    "sec-ch-ua": "\"Chromium\";v=\"106\", \"Google Chrome\";v=\"106\", \"Not;A=Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "same-origin",
    "sec-fetch-site": "same-origin",
    "x-client-app-version": "174.0.10149016",
    "x-client-date": "1665517847387",
    "x-csrf-token": "388241e60529a8789a3b65535e1e19fba20afa5445419e4c",
    "x-page-request-id": "945c5f1f0af598a28e174db1ab034936",
    "x-requested-with": "XMLHttpRequest",
    "x-retpath-y": "https://auto.ru/moskva/cars/chery/amulet/all/",
    "x-yafp": "{\"a1\":\"Ot/3OQ==;0\",\"a2\":\"C8UtLNrtIqPOfuf4qz0ZB3Nd4+ICCA==;1\",\"a3\":\"4K4YOVb/ZLa3sLScPDHl9g==;2\",\"a4\":\"aet/FfWsEZ2zlg==;3\",\"a5\":\"JUlKbFnZrpPOZw==;4\",\"a6\":\"Os4=;5\",\"a7\":\"VAgQ7vMn/voelA==;6\",\"a8\":\"5j/qvvXSLdA=;7\",\"a9\":\"uOkaLqfSrpATKQ==;8\",\"b1\":\"zQ6z0zPwIrU=;9\",\"b2\":\"5Mps9D9PfWKMTw==;10\",\"b3\":\"QFaZ+21Yjnphew==;11\",\"b4\":\"nLumEJG1keU=;12\",\"b5\":\"cT2Y1fAmEYej2Q==;13\",\"b6\":\"ZgXjxb4cFYm0BQ==;14\",\"b7\":\"7W4n15pQQZAkQA==;15\",\"b8\":\"7VKIusfc1MhCKA==;16\",\"b9\":\"J2BMdiWPEkuvVA==;17\",\"c1\":\"jlO92Q==;18\",\"c2\":\"Bd8yne09V0S7+5rtO31cUa6T;19\",\"c3\":\"xKVMh3A1e7SMzBCdFYOn2VMk;20\",\"c4\":\"uJsUtI0Iypw=;21\",\"c5\":\"gRnNg0sGaDQ=;22\",\"c6\":\"V7jG+Q==;23\",\"c7\":\"fKs8LigDDwc=;24\",\"c8\":\"N5Q=;25\",\"c9\":\"OfrCwbBZJJU=;26\",\"d1\":\"QioM0Xd+i/o=;27\",\"d2\":\"Ios=;28\",\"d3\":\"v4biHkj4hOcslg==;29\",\"d4\":\"Lu6oeoZxaTU=;30\",\"d5\":\"Gs13PIC6g4g=;31\",\"d7\":\"PnkiNJUz4BM=;32\",\"d8\":\"3JfSEXInldsuVKi5IXRp3yuIvsrwuYwjA0E=;33\",\"d9\":\"hJInct8//O4=;34\",\"e1\":\"HH3e0JtvJYegUg==;35\",\"e2\":\"jiwp5DFMlFQ=;36\",\"e3\":\"xTuRXXvzHYQ=;37\",\"e4\":\"S48H7DZDwy4=;38\",\"e5\":\"/LRDne8jdP0IAg==;39\",\"e6\":\"ETYp7zy0caY=;40\",\"e7\":\"hgSmshEitfsPeQ==;41\",\"e8\":\"btYw1z7nTrM=;42\",\"e9\":\"BSzYdtU1qz4=;43\",\"f1\":\"qeGzTo06Bxos+g==;44\",\"f2\":\"iaEJX5vNyCI=;45\",\"f3\":\"Jhbe5xGUzUSfiw==;46\",\"f4\":\"1XYGjB6wnbA=;47\",\"f5\":\"HVxEx3C4jVxfvg==;48\",\"f6\":\"1YwNQaaUCeSlFg==;49\",\"f7\":\"uJOoqNXHcjR00g==;50\",\"f8\":\"I+620z1eprwUrQ==;51\",\"f9\":\"XVN8QqQJjRI=;52\",\"g1\":\"LdMKItNoQrQHqw==;53\",\"g2\":\"QqB69WAZmiRznA==;54\",\"g3\":\"jjg70ZvVQ38=;55\",\"g4\":\"Qc7gn5Kyjv09dw==;56\",\"g5\":\"FCHWBa/Yiqs=;57\",\"g6\":\"FiqAz3KvVTQ=;58\",\"g7\":\"nCNpgdT079c=;59\",\"g8\":\"BRFPC805Rds=;60\",\"g9\":\"jwrH6VftcbY=;61\",\"h1\":\"oF2iXKInGBSNFg==;62\",\"h2\":\"fvJII2Zmfcdpkw==;63\",\"h3\":\"pJhvMlAx8jyyKQ==;64\",\"h4\":\"0TBwn6YXTefnqQ==;65\",\"h5\":\"D4wvBmcnuWc=;66\",\"h6\":\"8ZoqKLMllG0J4g==;67\",\"h7\":\"MxPKohVhs32eDm5/sWCufgCl+/Nb/VKZk2WOBzI/n+jfFfr9;68\",\"h8\":\"3nE+wtQQ8oP0iw==;69\",\"h9\":\"/po0LJMkq/q3DA==;70\",\"i1\":\"6r27Np253Vg=;71\",\"i2\":\"4onwy3YcfdPTgg==;72\",\"i3\":\"/R6OSQakQPdVlg==;73\",\"i4\":\"PXzFrCJc1P6V6w==;74\",\"i5\":\"xM0yY8mVLcCNCw==;75\",\"z1\":\"M8FEHp/2K6KTkQqFF47SFj2vtrPmEoJzi7SiHwnx2wnPfSrsqbOmsdXWPOjDijm7TC99Lk8R37YCMJ/MRZ5ltw==;76\",\"z2\":\"n60AgP00320jdjkD/wF+o9iSntYLkSVB2g5Yamd6K7W/V17gjDjMql8UkwNX4znoKHF6p0syQdLwUcIbCV9MCA==;77\",\"y2\":\"EVVYsw/Cx004cg==;78\",\"y3\":\"3k9BsRuMhyK4Ow==;79\",\"y6\":\"qJqpE+mwHFe0SQ==;80\",\"y8\":\"j9ktDJemQtqVRQ==;81\",\"x4\":\"tnPoQuwzbCAIeg==;82\",\"z5\":\"1+a/h+v6YHU=;83\",\"z4\":\"Ufk5z4hjh+mw4w==;84\",\"z6\":\"GGT9pr0VRg7GS6aq;85\",\"z7\":\"8OTydAGE5TB0Mt9t;86\",\"z8\":\"8M6pCebrjog9/xUn9r8=;87\",\"z9\":\"zi/Vt/tOoDzvIwa6;88\",\"y1\":\"GOoFoJGQW3bpkcBy;89\",\"y4\":\"qAbLFPKbOjjiGef5;90\",\"y5\":\"Qyp4p1cEqmx8X28uLtM=;91\",\"y7\":\"+jvXduaLg9PdUqkt;92\",\"y9\":\"N/joWiTdmOCvDXyGWCo=;93\",\"y10\":\"2pkscHYgD18qGuHtGOE=;94\",\"x1\":\"MREA/7NYBSWYSqKB;95\",\"x2\":\"SCwP1GrNi59TrBYte2I=;96\",\"x3\":\"bWdL7VWq/CITJVAr;97\",\"x5\":\"7Oa/tYOUnx05YSL+;98\",\"z3\":\"1YaYFEelql7ct4c9Xi6cTi5cE6VHcP6oQ3wLArCB+6M=;99\",\"v\":\"6.3.1\",\"pgrdt\":\"REvMvJNHti9lzKHKA6y7W2trDiI=;100\",\"pgrd\":\"pwNA1kV9VxMLeisj3JHeRV0Cxfe6x8xzQfHiQmKWLwG4slZUmQzDk90Vbvii9076l0VgXj3TpKj/qpFMQy4JpXkClz2SFzLUKNZWlHH/Mw4vvhTIwKPde6+wuueV/GyJzYOdzsqAvXEp4InRUf7ctH1/mXg6v87ZSS+bR9CmsxyPGaQf6h/oP7d4Vds1MYq3lUE/pVthfqx8Ur6QgjAkns8uuu8=\"}",
    "cookie": "suid=9e523ee95f261abc1814ce21181f9348.abcf5fdbc881d84e293cda7d1eb4b56f; _csrf_token=388241e60529a8789a3b65535e1e19fba20afa5445419e4c; autoru_sid=a%3Ag6345c8d629no7na7qernibpovrm5jpl.edc069b71b0a5327e1070f2500adb1f2%7C1665517782364.604800.e8YiDMtxeU6VMc-DP5ruMg.7hQz-CTUFGI859rFYSDGOPNgwN5iXcKQ3Mz3YK0hPik; autoruuid=g6345c8d629no7na7qernibpovrm5jpl.edc069b71b0a5327e1070f2500adb1f2; from=google-search; counter_ga_all7=1; yuidlt=1; yandexuid=3146661541573414476; my=YwA%3D; crookie=dqcCd7A9cvkhdX4Q/mrvQV/vUS9C1MxIwDMYDxljDSU1a6Q7EaFDqa+EwUyrXFr1l0mBLlrRAfMIavl/O80EdxwQgbo=; cmtchd=MTY2NTUxNzc4NTAyOA==; Session_id=3:1665517786.5.0.1616179603925:JSrBsA:4.1.2:1|363564353.0.2|61:10008044.333649.-c3VlvBsy-3vcwmB76MW860THQU; yandex_login=onebackoff; ys=udn.cDpvbmViYWNrb2Zm#c_chck.1225019817; i=3LGf/vQ1XZ53G6kXgCbDM3ytPDF3+vMKhg3kZofACDEmy2DBW1v3jjepS2o8+TlrpnPDH2LI8MbYyjRJ6v3ulD3v7Rg=; mda2_beacon=1665517786129; sso_status=sso.passport.yandex.ru:synchronized; gdpr=0; _ym_uid=1665517788858190801; _ym_isad=1; _yasc=hx6EDJg9mqt46iaajyU2TvlaYCC3OQc2NekGj2k6urFz9Cx4; from_lifetime=1665517814176; _ym_d=1665517817; layout-config={\"win_width\":839,\"win_height\":930}",
    "Referer": "https://auto.ru/moskva/cars/chery/amulet/all/",
    "Referrer-Policy": "no-referrer-when-downgrade"
  },
  "body": "{\"catalog_filter\":[{\"mark\":\"CHERY\",\"model\":\"AMULET\"}],\"section\":\"all\",\"category\":\"cars\",\"output_type\":\"list\",\"geo_radius\":200,\"geo_id\":[213]}",
  "method": "POST"
})



offers = amulets.json()["offers"]
print(amulets.json())

for offer in offers:
    price = offer["price_info"]["USD"]
    name = offer["vehicle_info"]["model_info"]["name"]
    mileage = offer["state"]["mileage"]
    print(f"Найден {name} всего за ${price}, пробег всего {mileage} км")