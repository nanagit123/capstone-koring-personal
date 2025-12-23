/*본 파일은 팀 프로젝트 내에서
다른 팀원이 구현한 기능이다.
본인은 해당 모듈을 기반으로 다른 기능과 연동 및 테스트를 진행하였다.*/

import { recommend } from '../js/api.js';

function renderRestaurants(restaurants = []) {
  const container = document.getElementById('restaurant-list');
  if (!container) return;

  if (!restaurants.length) {
    container.innerHTML = '<p class="empty">추천 맛집이 없습니다.</p>';
    return;
  }

  container.innerHTML = '';

  restaurants.forEach((restaurant) => {
    const item = document.createElement('div');
    item.className = 'restaurant-item';

    item.innerHTML = `
      <div class="restaurant-info">
        <div class="restaurant-name">${restaurant.name}</div>
        <div class="restaurant-address">${
          restaurant.address || '주소 정보 없음'
        }</div>
      </div>
    `;

    item.addEventListener('click', () => {
      if (restaurant.latitude && restaurant.longitude) {
        const lat = parseFloat(restaurant.latitude);
        const lng = parseFloat(restaurant.longitude);
        const name = encodeURIComponent(restaurant.name || '맛집');
        const url = `https://map.kakao.com/link/map/${name},${lat},${lng}`;
        window.open(url, '_blank');
      }
    });

    container.appendChild(item);
  });
}

document.addEventListener('DOMContentLoaded', async () => {
  const container = document.getElementById('restaurant-list');
  if (container) {
    container.innerHTML = '<p class="loading">로딩중...</p>';
  }

 let payload = {};
  try {
    payload = JSON.parse(sessionStorage.getItem('recommendPayload')) || {};
  } catch (e) {
    payload = {};
  }

   try {
    const res = await recommend(payload);
    const data = res?.data || res || {};
    const items = Array.isArray(data.results) ? data.results : [];

    renderRestaurants(items);
  } catch (error) {
    console.error('추천 요청 중 오류 발생:', error);
    if (container) {
      container.innerHTML =
        "<p class='error'>추천 요청 중 오류가 발생했습니다. 나중에 다시 시도해 주세요.</p>";
    }
  }
});
  