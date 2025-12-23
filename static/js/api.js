//API 기본 경로(배포 환경에 따라 설정)
const API_BASE = '';

//인증/사용자 관련 APi

//로그인&회원가입 +인증 상태 확인
export function login(data) {
  return fetch(`${API_BASE}/api/restaurant/recommend`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  }).then(res => res.json());
}

export function register(data) {
  return fetch(`${API_BASE}/api/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  }).then(res => res.json());
}

export function logout() {
  return fetch(`${API_BASE}/api/logout`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' }
  }).then(res => res.json());
}

export function checkAuth() {
  return fetch(`${API_BASE}/api/check-auth`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' }
  }).then(res => res.json());
}

//맛집추천
//*추천 로직은 서버 내부 DB 기반으로 처리됨
export function recommend(data) {
  return fetch(`${API_BASE}/api/restaurant/recommend`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  }).then(res => res.json());
}

export function getRestaurant(id) {
  return fetch(`${API_BASE}/api/restaurant/${id}`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' }
  }).then(res => res.json());
}

//지도(카카오맵)
export function search(data) {
  return fetch(`${API_BASE}/api/search`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  }).then(res => res.json());
}

export function searchAddress(data) {
  return fetch(`${API_BASE}/api/search-address`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  }).then(res => res.json());
}

export function getMap(data) {
  return fetch(`${API_BASE}/api/get-map`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  }).then(res => res.json());
}