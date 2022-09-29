import googlemaps
import csv
import time

googleapikey = 'API keyを設定する'
gmaps = googlemaps.Client(key=googleapikey)

with open("./mylist1.txt", "r", encoding="utf-8_sig") as f:
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
        print(row[0])
        result = gmaps.geocode(row[0])
        lat = result[0]["geometry"]["location"]["lat"]
        lng = result[0]["geometry"]["location"]["lng"]
        print (lat,lng)
        time.sleep(0.5)