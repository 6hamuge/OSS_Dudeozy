"use strict";
console.log('관리관리');
// csrf token
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

var resultArray = []; // 출발지, 목적지 좌표
var shortestRoute = []; // 최단거리 좌표 정보

var input = document.getElementById("start_input");
input.onclick = function () {
    new daum.Postcode({
        oncomplete: function (data) {
            var roadAddr = data.roadAddress;
            var extraRoadAddr = '';

            if (data.bname !== '' && /[동|로|가]$/g.test(data.bname)) {
                extraRoadAddr += data.bname;
            }
            if (data.buildingName !== '' && data.apartment === 'Y') {
                extraRoadAddr += (extraRoadAddr !== '' ? ', ' + data.buildingName : data.buildingName);
            }
            if (extraRoadAddr !== '') {
                extraRoadAddr = ' (' + extraRoadAddr + ')';
            }

            document.getElementById("StartAddr").value = roadAddr;
        }
    }).open();
};

var output = document.getElementById("end_input");
output.onclick = function () {
    new daum.Postcode({
        oncomplete: function (data) {
            var roadAddr = data.roadAddress;
            var extraRoadAddr = '';

            if (data.bname !== '' && /[동|로|가]$/g.test(data.bname)) {
                extraRoadAddr += data.bname;
            }
            if (data.buildingName !== '' && data.apartment === 'Y') {
                extraRoadAddr += (extraRoadAddr !== '' ? ', ' + data.buildingName : data.buildingName);
            }
            if (extraRoadAddr !== '') {
                extraRoadAddr = ' (' + extraRoadAddr + ')';
            }

            document.getElementById("EndAddr").value = roadAddr;
        }
    }).open();
};

// 길찾기 버튼 클릭
$("#find_botton").click(function () {
    shortestRoute = []; // 초기화

    $.ajax({
        type: 'POST',
        url: Mpathfinder,
        data: {
            'StartAddr': $('#StartAddr').val(),
            'EndAddr': $('#EndAddr').val(),
            'csrfmiddlewaretoken': csrftoken,
        },
        success: (result) => {
            console.log(result);
            document.getElementById('pathForm').submit();
        },
        error: (error) => {
            console.log(error);
        }
    });
});

