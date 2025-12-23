//게시글 작성 페이지 js

//페이지 로드 후 폼 이벤트 초기화
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("postForm");
  if (!form) return; //폼 없는 경우 오류 방지

  form.addEventListener("submit", handleSubmit);
});

//게시글 작성 처리
async function handleSubmit(e) {
  e.preventDefault(); 

  const title = document.getElementById("postTitle").value.trim();
  const content = document.getElementById("postContent").value.trim();

  //내용 검증
  if (!title || !content) {
    alert("제목과 내용을 모두 입력하세요.");
    return;
  }

  //community.py의 게시글 작성 api 호출
  try {
    const response = await fetch("/koring/community/posts", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        postTitle: title,
        postContent: content
      })
    });

    const data = await response.json();

    
    if (data.success) {
      //작성 성공 시 목록 페이지로 이동
      window.location.href = "/koring/community/";
    } else {
      alert(data.message || "글 작성에 실패했습니다.");
    }
  } catch (err) {
    console.error("글 작성 중 오류:", err);
    alert("서버 오류가 발생했습니다.");
  }
}
