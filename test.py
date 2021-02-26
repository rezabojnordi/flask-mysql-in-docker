import time
a = [
        [
            1,
            "softgrand.ir/banner2",
            "double click",
            "3",
            "Mozilla/5.0 (platform; rv:geckoversion) Gecko/geckotrail Firefox/firefoxversion"
        ],
        [
            2,
            "google.com/banner2",
            "click",
            "18",
            " Mozilla/6.0 (platform; rv:geckoversion) Gecko/geckotrail Firefox/firefoxversion"
        ]
    ]



arry_app = []
ip_id = "254"
expire = time.time()
for i in range(len(a)):
    for j in range(len(a[i])):
        pass
    arry_app.append((ip_id,a[i][0],expire,ip_id,a[i][3],"pending"))
print(arry_app)