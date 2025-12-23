/*본 파일은 팀 프로젝트 내에서
다른 팀원이 구현한 기능이다.
본인은 해당 모듈을 기반으로 다른 기능과 연동 및 테스트를 진행하였다.*/

function setupLanguageSelector() {
  const langSelect = document.querySelector('.page-restaurant .lang-select');
  if (langSelect) {
    langSelect.addEventListener('change', function() {
      changeLanguage(this.value);
    });
  }
}

/**
 * 언어 변경 처리 함수
 * @param {string} lang 
 */
function changeLanguage(lang) {
  console.log(`언어가 ${lang}로 변경되었습니다.`);
}


const selected = {
  age: [],
  mood: [],
  cuisine: []
};

document.addEventListener('DOMContentLoaded', () => {
  setupLanguageSelector();

  const buttons = document.querySelectorAll('.page-restaurant .filter-btn');
  const submitBtnContainer = document.querySelector('.page-restaurant .submit-btn');
  const submitBtn = document.getElementById('go-recommend'); 
  
  buttons.forEach((btn) => {
    btn.addEventListener("click", () => {
      const category = btn.dataset.category;
      const value = btn.textContent.trim();

      btn.classList.toggle("selected");

      if (!selected[category]) {
        selected[category] = [];
      }

      if (btn.classList.contains("selected")) {
        if (!selected[category].includes(value)) {
          selected[category].push(value);
        }
      } else {
        selected[category] = selected[category].filter((v) => v !== value);
      }
      const anySelected =
        (selected.age && selected.age.length > 0) ||
        (selected.mood && selected.mood.length > 0) ||
        (selected.cuisine && selected.cuisine.length > 0);

      if (anySelected) {
        submitBtnContainer.classList.add("enabled");
      } else {
        submitBtnContainer.classList.remove("enabled");
      }
    });
  });
  if (submitBtn) {
    submitBtn.addEventListener("click", () => {
      if (!submitBtnContainer.classList.contains("enabled")) {
        alert("최소 한 개 이상 선택해 주세요.");
        return;
      }

      const payload = {
        age: selected.age,
        mood: selected.mood,
        cuisine: selected.cuisine,
        page: 1,
        size: 10,
      };
      sessionStorage.setItem("recommendPayload", JSON.stringify(payload));
      window.location.href = "/restaurant/result";
    });
  }
});
