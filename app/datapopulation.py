import random
import database as db
import math
from random import randint, uniform

x = -88.1628361172767
y = 40.17099055738766

x1 = -88.14431320938505
y1 = 40.15687392660523

year = "2022"
month = "02"
day = 15

arr = []

img_1 = "http://soham.catgirl.pw/c4ed8131-ecd3-4a2e-a22d-2cf519fceeef.jpg"
img_2 = "http://soham.catgirl.pw/a6796bab-9c03-4421-819e-c26f30f3151e.jpg"
img_3 = "http://soham.catgirl.pw/c4ed8131-ecd3-4a2e-a22d-2cf519fceeef.jpg"
def generate_cluster(disease, i):
    x_cluster = [-88.1474915415203, -88.15833276840198, -88.15881208460543]
    disease_cluster_x = x_cluster[i]
    y_cluster = [40.16465611817094, 40.16816354920241, 40.159340590197196]
    disease_cluster_y = y_cluster[i]
    radius = 0.001

    day = 20220215
    count = 0

    arr = []
    count = 0
    day = 20220215
    for i in range(0, 14):
        scale = (i) ** 1.2
        day_arr = []
        for i in range(0, int(scale)):
            x = uniform(disease_cluster_x - radius, disease_cluster_x + radius)
            y = uniform(disease_cluster_y - radius, disease_cluster_y + radius)
            day_arr.append([x, y, day])
        yester_arr = db.get_objects_by_date(str(day - 1))
        for arr in yester_arr:
            db.add_object(arr["image"], arr["classification"], arr["x_coordinate"], arr["y_coordinate"], str(day), 1)
        for arr in day_arr:
            img = random.choice([img_1, img_2, img_3])
            db.add_object(img, disease, arr[0], arr[1], str(day), 1)
        day += 1

def generate_thru():
    day = 20220215
    for i in range(0, 14):
        for j in range(0, 15):
            img = random.choice([img_1, img_2, img_3])
            xx = uniform(x1, x)
            yy = uniform(y1, y)
            db.add_object(img, random.choice(["Mosaic Disease", "Bacterial Blight", "Green Mite", "Brown Streak Disease"]), xx, yy, str(day), 1)
        day += 1

random.choice(["Mosaic Disease", "Bacterial Blight", "Green Mite", "Brown Streak Disease"])
#generate_cluster("Green Mite")

generate_cluster("Mosaic Disease", 0)
generate_cluster("Bacterial Blight", 1)
generate_cluster("Green Mite", 2)
generate_thru()