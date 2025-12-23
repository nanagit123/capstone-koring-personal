/*본 파일은 팀 프로젝트 내에서
다른 팀원이 구현한 기능이다.
본인은 해당 모듈을 기반으로 다른 기능과 연동 및 테스트를 진행하였다.*/

import { getPosts } from './api.js';

function renderCommunityPreview(posts) {
  const listEl = document.getElementById('post-list'); 
  listEl.innerHTML = '';

  posts.forEach(post => {
    const li = document.createElement('li');
    const link = document.createElement('a');
    link.href = `/koring/community/posts/${post.id}`;
    link.textContent = post.title;
    li.appendChild(link);
    listEl.appendChild(li);
  });
}

document.addEventListener('DOMContentLoaded', () => {
  getPosts()
    .then(data => { console.log('게시글 데이터:', data); renderCommunityPreview(data); })
    .catch(err => console.error('게시글 불러오기 실패', err));
});