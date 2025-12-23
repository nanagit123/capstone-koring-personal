//커뮤니티 게시글 목록 페이지 js

//페이지 로드 완료 후 초기화 처리
document.addEventListener("DOMContentLoaded", () => {
  initializeCommunityPage();
});

//페이지 초기화
function initializeCommunityPage() {
  console.log("community.js: 페이지 로딩 완료");

  //언어 선택 기능 초기화
  //현재 html에는 요소가 없어도 오류 없이 동작하도록 처리
  setupLanguageSelector();

  // 게시글 링크 클릭 이벤트 등록(실제 이동은 a 태그 기본 동작)
  registerPostClickEvents();
}

// 언어 선택 박스 처리
function setupLanguageSelector() {
  const langSelect = document.querySelector(".language-select");
  if (!langSelect) return; //요소가 없을 경우 예외 방지

  langSelect.addEventListener("change", function () {
    console.log("언어 변경:", this.value);
  });
}

// 게시글 클릭 로깅
function registerPostClickEvents() {
  const links = document.querySelectorAll(".post-link");
  if (!links) return; //게시글 없는 경우 처리

  links.forEach(link => {
    link.addEventListener("click", () => {
      console.log("게시글 클릭:", link.href);
    });
  });
}
