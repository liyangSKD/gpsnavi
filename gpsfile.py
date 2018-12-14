#!/usr/bin/python3
import socket 
from io import StringIO
from datetime import datetime
import shapefile
from shapely.geometry.point import Point 
from shapely.geometry import shape 
host = '127.0.0.1' #localhost
#host = '192.168.3.20' 
port = 52002
bufsize = 256
buff = StringIO()
#filepath = '/home/pi/rtklog/'
#shpfile = '/home/pi/SHP/2019utf_WGS84.shp'
shpfile = '‪D:/QGIS/2019utf_WGS84.shp'
filepath = 'D:/rtklog'
#座標取得
def getpoint():
    
    buff = StringIO()
    data = sock.recv(bufsize)
    #print(len(data))
    buff.write(data.decode('utf-8'))
    data = buff.getvalue().replace('\n', '')
    pointlist = data.split()
    buff.close()
    if  len(pointlist)  <15  :
        print("getpoint re-try")
        getpoint()
    return pointlist

def getshp(lon,lat):

    try : 
        point = ( lon , lat )#（経度lon、緯度lat）
        print(point)
        shp = shapefile.Reader(shpfile) #open the shapefile
        print(type(shp))
        all_shapes = shp.shapes() 
        all_records = shp.records()

        for i in range(len(all_shapes)):
            boundary = all_shapes[i] 
            if Point(point).within(shape(boundary)): 
               this_record= all_records[i] [:]
               print( "圃場データ",this_record[9:11] ) #[9]:圃場コード　[10]:地番名
               return this_record
        print("NO SHP DATA")
        return 0
    except :
        print("getshp error")
        return 0
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    while True:
        nowpoint = getpoint()
        shprecord = getshp(float(nowpoint[3]),float(nowpoint[2]))
        while shprecord == 0:
            nowpoint = getpoint()
            shprecord = getshp(float(nowpoint[3]),float(nowpoint[2]))
            
        now = datetime.now()
        file = '{}_{0:%Y%m%d%H%M}.csv'.format(shprecord[9],now)
        print(file)
        while getshp(float(nowpoint[3]),float(nowpoint[2])) != 0 :
            for i in range(3000):
                fileobj = open(filepath + file, "a", encoding = "utf-8")
                savepoint = " ".join(getpoint())
                fileobj.write(savepoint + "\n")
                fileobj.close()
                #print("PointSave")
except socket.error:
    print('socket error')

except KeyboardInterrupt:
    pass
sock.close()
