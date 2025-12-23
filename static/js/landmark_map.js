//명소 페이지 카카오맵 연결 js
window.onload = function () {
 kakao.maps.load(function() {
    const mapContainer = document.getElementById('map');
    const lat = parseFloat(mapContainer.dataset.lat);
    const lng = parseFloat(mapContainer.dataset.lng);

    const mapOption = {
      center: new kakao.maps.LatLng(lat, lng),
      level: 3
    };

    const map = new kakao.maps.Map(mapContainer, mapOption);

    const marker = new kakao.maps.Marker({
      position: new kakao.maps.LatLng(lat, lng)
    });

    marker.setMap(map);
  });
};