"use strict";

let latitude = 0;
let longitude = 0;
let leaf_map;
let start_markers;
let end_markers;
let short_line;
let safe_line;

$(document).ready(function () {
    $('.route-wrap').hide();

    getLocation().then(location => {
        latitude = location.latitude;
        longitude = location.longitude;

        initializeMap(latitude, longitude);

        // 이제 leaf_map이 초기화되었으므로 이벤트 핸들러를 등록할 수 있습니다.
        // 출발지 마커 찍기
        leaf_map.on('click', function (e) {
            addStartMarker(e.latlng.lat, e.latlng.lng);
        });
    });

    $('#StartAddr').click(function () {
        openAddressSearchModal('StartAddr');
    });

    $('#EndAddr').click(function () {
        openAddressSearchModal('EndAddr');
    });

    $("#find_botton").click(function () {
        findRoutes();
    });
});

function initializeMap(lat, lng) {
    leaf_map = L.map('map').setView([lat, lng], 15);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 18 }).addTo(leaf_map);

    L.control.locate({
        position: 'topleft',
        strings: {
            title: "Show me where I am, yo!"
        }
    }).addTo(leaf_map);
}

function addStartMarker(lat, lng) {
    console.log(lat, lng);
    if (start_markers) {
        leaf_map.removeLayer(start_markers);
    }
    start_markers = L.marker([lat, lng]).addTo(leaf_map);
    $('#StartAddr').val(lat + ' ' + lng); // 좌표를 입력창에 넣기
}

function openAddressSearchModal(inputId) {
    new daum.Postcode({
        oncomplete: function (data) {
            $('#' + inputId).val(data.roadAddress);
        }
    }).open();
}

function findRoutes() {
    let startAddr = $('#StartAddr').val();
    let endAddr = $('#EndAddr').val();

    if (!startAddr || !endAddr) {
        console.log('출발지 또는 목적지 주소를 입력하세요.');
        return;
    }

    let resultArray = {};

    $.ajax({
        type: 'POST',
        url: setpointpage,
        data: {
            'StartAddr': startAddr,
            'EndAddr': endAddr,
            'csrfmiddlewaretoken': csrftoken,
        }
    }).done(function (result) {
        resultArray = result;
        console.log(resultArray);
        findShortestRoute(resultArray);
        findSafeRoute(resultArray);
    }).fail(function (error) {
        console.log('주소 변환 실패:', error);
    });
}

function findShortestRoute(resultArray) {
    $.ajax({
        method: "POST",
        url: "https://apis.openapi.sk.com/tmap/routes/pedestrian?version=1&format=json&callback=result",
        data: {
            "appKey": "l7xxa033eab75a3a4ab38dd11a74fb8b87c6",
            "startX": resultArray['startaddr'][1],
            "startY": resultArray['startaddr'][0],
            "endX": resultArray['endaddr'][1],
            "endY": resultArray['endaddr'][0],
            "reqCoordType": "WGS84GEO",
            "resCoordType": "EPSG3857",
            "startName": "출발지",
            "endName": "도착지"
        }
    }).done(function (result) {
        let resultData = result.features;
        if (resultData && resultData.length > 0 && resultData[0].properties) {
            let totalDistance = (resultData[0].properties.totalDistance / 1000).toFixed(1);  // 소수점 이하 한 자리까지 표시
            let totalTime = (resultData[0].properties.totalTime / 60).toFixed(0);  // 소수점 이하 버림 처리

            let tDistance = "총 거리 : " + totalDistance + "km";
            let tTime = " 총 시간 : " + totalTime + "분";

            console.log(tDistance + " " + tTime);

            $('#short-route').text(tDistance);
            $('#short-time').text(tTime);

            drawShortestRoute(resultData);
        } else {
            console.log('결과 데이터가 비어 있거나 예상과 다른 구조입니다.');
            // 데이터가 비어 있는 경우에 대한 처리를 여기에 추가
        }
    }).fail(function (error) {
        console.log('최단 경로 탐색 실패:', error);
    });
}

function findSafeRoute(resultArray) {
    $.ajax({
        method: "POST",
        url: saferoute,
        traditional: true,
        data: {
            "startX": resultArray['startaddr'][1],
            "startY": resultArray['startaddr'][0],
            "endX": resultArray['endaddr'][1],
            "endY": resultArray['endaddr'][0],
            'csrfmiddlewaretoken': csrftoken,
        }
    }).done(function (response) {
        console.log('Response from saferoute API:', response);
        let safeRoute = response['result'];
        console.log('Received safeRoute:', safeRoute);

        if (safeRoute && Array.isArray(safeRoute) && safeRoute.length > 0) {
            let safeDistance = "총 거리 : " + parseFloat(response['totalDistance']).toFixed(1) + "km";
            let safeTime = " 총 시간 : " + parseInt(response['totalTime']).toFixed(0) + "분";

            $('#safe-route').text(safeDistance);
            $('#safe-time').text(safeTime);

            $('.route-wrap').show();

            drawSafeRoute(safeRoute);
        } else {
            console.log('Invalid safeRoute data:', safeRoute);
            // 대체 경로 제공
            $('#safe-route').text('안전 경로를 찾을 수 없습니다.');
            $('#safe-time').text('');
            $('.route-wrap').show();
        }
    }).fail(function (error) {
        console.log('안전 경로 탐색 실패:', error);
        // 대체 경로 제공
        $('#safe-route').text('안전 경로를 찾을 수 없습니다.');
        $('#safe-time').text('');
        $('.route-wrap').show();
    });
}


function drawShortestRoute(resultData) {
    if (short_line) {
        leaf_map.removeLayer(short_line);
    }

    let shortestRoute = [];
    for (let i in resultData) {
        let geometry = resultData[i].geometry;
        if (geometry.type == "LineString") {
            for (let j in geometry.coordinates) {
                let latlng = new Tmapv2.Point(geometry.coordinates[j][0], geometry.coordinates[j][1]);
                let convertPoint = new Tmapv2.Projection.convertEPSG3857ToWGS84GEO(latlng);
                let convertChange = new Tmapv2.LatLng(convertPoint._lat, convertPoint._lng);
                shortestRoute.push([convertChange['_lat'], convertChange['_lng']]);
            }
        }
    }
    console.log('최단경로', shortestRoute);

    short_line = L.polyline(shortestRoute, {
        color: "red",
        weight: 5
    }).addTo(leaf_map);
}

function drawSafeRoute(safeRoute) {
    if (safe_line) {
        leaf_map.removeLayer(safe_line);
    }

    let safeRouteLatLngs = [];

    for (let i = 0; i < safeRoute.length; i++) {
        if (Array.isArray(safeRoute[i]) && safeRoute[i].length === 2) {
            let latlng = L.latLng(safeRoute[i][0], safeRoute[i][1]);
            safeRouteLatLngs.push(latlng);
        } else {
            console.log('Invalid coordinate pair:', safeRoute[i]);
        }
    }

    if (safeRouteLatLngs.length > 0) {
        safe_line = L.polyline(safeRouteLatLngs, {
            weight: 5,
            color: 'blue'
        }).addTo(leaf_map);
    } else {
        console.log('No valid coordinates to draw the route.');
    }
}

// 현재 위치 정보를 가져오는 함수
function getLocation() {
    return new Promise(resolve => {
        navigator.geolocation.getCurrentPosition(function (position) {
            resolve({
                latitude: position.coords.latitude,
                longitude: position.coords.longitude,
            });
        });
    });
}

// CSRF 토큰 가져오기
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

let csrftoken = getCookie('csrftoken');