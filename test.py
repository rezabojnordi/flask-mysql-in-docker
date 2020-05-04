import numpy as np
import json
a =  [(
    "softgrand.ir/banner1",
    "double click",
    "20",
    "1"
),
  (
    "softgrand.ir/banner2",
    "double click",
    "21",
    "1"
  )]


res =[]
for x in a:
	res.append({
		"link":x[0],
		"click":x[1],
		"time":x[2],
		"enable":x[3]
	})

print(res)





print(tuple("reza","bojnordi"))