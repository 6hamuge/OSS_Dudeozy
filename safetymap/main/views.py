from typing import Iterable
from django.http.response import HttpResponse
from django.shortcuts import render
from folium import plugins
import folium
import geocoder     #import geojson
import json, requests

from . import RouteSearch   
from haversine import haversine #거리측정

from django.shortcuts import render
from django.http import HttpResponse

def set_spot_view(request):
    return HttpResponse("This is the SetSpot view.")

g = geocoder.ip('me')   #현재 내위치
# Create your views here.
def home(request) :
    map = folium.Map(location=g.latlng,zoom_start=15, width='100%', height='100%',)
    plugins.LocateControl().add_to(map)
    plugins.Geocoder().add_to(map)

    maps=map._repr_html_()  #지도를 템플릿에 삽입하기위해 iframe이 있는 문자열로 반환 (folium)
    
    return render(request,'../templates/home.html',{'map' : maps})

def saferoute(request):
    SafePath = []
    totalDistance = 0

    startx, starty = float(request.POST.get('startX')), float(request.POST.get('startY'))
    endx, endy = float(request.POST.get('endX')), float(request.POST.get('endY'))
    
    Hmap, path, TileValue_Map, grid_object = RouteSearch.startSetting((startx, starty), (endx, endy))

    # Retrieve necessary information from grid_object
    grid_size = grid_object['grid_size']
    start_corner = grid_object['start_corner']
    end_corner = grid_object['end_corner']
    neighbor = grid_object['neighbor']
    path = grid_object['path']

    if not path:
        return HttpResponse(json.dumps({'error': 'No path found'}), content_type="application/json")

    # Loop through the path to calculate SafePath and totalDistance
    for idx, HexPoint in enumerate(path):
        if idx == 0:
            # First node
            center_q = (HexPoint.q + 0.5) * grid_size[0] + start_corner[0]
            center_r = (HexPoint.r + 0.5) * grid_size[1] + start_corner[1]
        else:
            # Subsequent nodes
            prev_q, prev_r = path[idx - 1].q, path[idx - 1].r
            center_q = (HexPoint.q + 0.5) * grid_size[0] + start_corner[0]
            center_r = (HexPoint.r + 0.5) * grid_size[1] + start_corner[1]
            # Calculate distance between previous and current points
            distance = haversine((prev_q, prev_r), (HexPoint.q, HexPoint.r), unit=Unit.METERS)
            totalDistance += distance
        
        SafePath.append([center_q, center_r])

    # Calculate total time
    if totalDistance > 0:
        soc = 1 / 16  # Assuming speed of 16 meters per second
        totalTime = totalDistance / soc
    else:
        totalTime = 0
    
    print('토탈 거리:', totalDistance)
    print('토탈 시간:', totalTime)
    
    # Return JSON response
    return HttpResponse(json.dumps({'result': SafePath, 'totalDistance': totalDistance, 'totalTime': totalTime}), content_type="application/json")
        

def PathFinder(request) :
    shortData=[]
    SafePath=[]
    SPoint =[]

    # ------------------------- 최단 루트 (SPoint) -----------------------------------------
    start_coordinate = getLatLng(request.POST.get('StartAddr'))
    end_coordinate = getLatLng(request.POST.get('EndAddr'))

    shortData = request.POST.get('shortestRoute').split(",")

    '''
    for i in shortData :
        if(shortData.index(i)%2==0) :
            lat =i; #위도
            lon = shortData[(shortData.index(i))+1]  #경도
            point=[float(lat), float(lon)]
            SPoint.append(point)
    '''
    for i in range(0, len(shortData), 2):
        lat = shortData[i]
        lon = shortData[i + 1]
        point = [float(lat), float(lon)]
        SPoint.append(point)


    #-----------------------------맵핑-----------------------------------------
    map = folium.Map(location=start_coordinate,zoom_start=15, width='100%', height='100%',) 

    print("Shortest Path Points:", SPoint)  # 디버깅 출력을 추가합니다.

    folium.PolyLine(locations=SPoint, weight = 4, color='red').add_to(map)
    
    folium.Marker(
        location=start_coordinate,
        popup=request.POST.get('StartAddr'),
        icon=folium.Icon(color="red"),
    ).add_to(map)

    folium.Marker(
        location=end_coordinate,
        popup=request.POST.get('EndAddr'),
        icon=folium.Icon(color="red"),
    ).add_to(map)
    
    plugins.LocateControl().add_to(map)
    
    # ---------------------------안전 루트--------------------------------------
    #type : list(Hmap), grid(Hex), list
    Hexlist, path, TitleValue_map, grid_object = RouteSearch.startSetting(start_coordinate, end_coordinate)
    Before_Hex = path[0]
    increase=[0,0]      #q,r 증가율
    count=1
    
    for idx, HexPoint in enumerate(path) :
        if Before_Hex is not HexPoint :
            #첫 노드 증가율 기록 - 두번째 노드
            if increase[0]==0 and increase[1]==0:
                x = int(HexPoint[0])-int(Before_Hex[0])
                y = int(HexPoint[1])-int(Before_Hex[1])
                increase=[x,y]
                Before_Hex =HexPoint

                continue
            #증가율 비교
            else :
                x = int(HexPoint[0])-int(Before_Hex[0])
                y = int(HexPoint[1])-int(Before_Hex[1])
                if increase[0]==x and increase[1]==y:
                    Before_Hex =HexPoint
                    continue
                else:
                    increase=[x,y]


        print(count,' ',HexPoint)
        count+=1
        Before_Hex =HexPoint
        geo_center = grid_object.hex_center(HexPoint)
        SafePath.append([geo_center.y,geo_center.x])

        increase=[0,0]
    print("Safe Path Points:", SafePath)  # 디버깅 출력을 추가합니다.
    folium.PolyLine(locations=SafePath, weight = 4, color='blue').add_to(map)


    maps=map._repr_html_()  #지도를 템플릿에 삽입하기위해 iframe이 있는 문자열로 반환 (folium)

     
    return render(request,'../templates/home.html',{'map' : maps})
        
def GetSpotPoint(request) :

    start_coordinate = getLatLng(request.POST.get('StartAddr'))
    end_coordinate = getLatLng(request.POST.get('EndAddr'))

    context = {'startaddr' : start_coordinate, 'endaddr' : end_coordinate}    

    return HttpResponse(json.dumps(context), content_type='application/json')

def getLatLng(addr):
    url = 'https://dapi.kakao.com/v2/local/search/address.json?query='+addr
    headers = {"Authorization": "KakaoAK 894cfd738b31d10baba806317025d155"}
    result = json.loads(str(requests.get(url,headers=headers).text))
    match_first = result['documents'][0]['address']

    return float(match_first['y']),float(match_first['x'])