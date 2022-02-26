import random
import database as db
from random import uniform

y1 = 40.2151558052675
x1 = -88.12527531155014
y2 = 40.20073530692846
x2 = -88.10517555332925


year = "2022"
month = "02"
day = 14

for i in range(0, 12):
    str_day = str(day + i)
    str_date = year + month + str_day
    for j in range(0, 100):
        x = uniform(x1, x2)
        y = uniform(y1, y2)
        classification = random.randint(0, 5)
        print(i)
        db.add_object(classification, x, y, str_date)