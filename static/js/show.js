//게시글 상세 페이지 js

let currentPost = {};
let comments = [];

document.addEventListener("DOMContentLoaded", initPage);

function initPage() {
  const urlParams = new URLSearchParams(window.location.search);
  const postId = urlParams.get("id");
  if (!postId) {
    showError("게시글을 찾을 수 없습니다.");
    return;
  }
  fetchPostData(postId);
  fetchComments(postId);

  setupEventListeners();
}

function showError(message) {
  const container = document.querySelector(".post-body");
  container.innerHTML = `
    <div style="text-align:center; color:red; margin-top:20px;">
      ${message}
    </div>
  `;
}
function setupEventListeners() {
  const submitButton = document.querySelector(".submit-button");
  if (submitButton) {
    submitButton.addEventListener("click", submitComment);
  }
}
function fetchPostData(postId) {
  fetch(`/koring/community/post/${postId}`)
    .then((res) => res.json())
    .then((data) => {
      if (!data.success) {
        showError("게시글 정보를 가져올 수 없습니다.");
        return;
      }
      currentPost = {
        id: data.post.postID,
        username: data.post.userLoginID,
        date: data.post.postCreatedAt,
        title: data.post.postTitle,
        content: data.post.postContent,
      };

      renderPostData();
    })
    .catch((err) => {
      console.error(err);
      showError("서버 오류가 발생했습니다.");
    });
}
function renderPostData() {
  document.querySelector(".post-user").textContent = currentPost.username;
  document.querySelector(".post-date").textContent = currentPost.date;
  document.querySelector(".post-title").textContent = currentPost.title;
  document.querySelector(".show-post-content").textContent = 
  currentPost.content;
}
function fetchComments(postId) {
  fetch(`/koring/community/get_comments/${postId}`)
    .then((res) => res.json())
    .then((data) => {
      if (!data.success) return;

      comments = data.comments;
      renderComments();
    })
    .catch((err) => console.error(err));
}
function renderComments() {
  const commentsSection = document.querySelector(".comments");
  commentsSection.innerHTML = "";

  if (comments.length === 0) {
    commentsSection.innerHTML = 
    `<p class="no-comments">아직 댓글이 없습니다.</p>`;
    return;
  }

  comments.forEach((comment) => {
    commentsSection.appendChild(createCommentElement(comment));
  });
}
function createCommentElement(comment) {
  const div = document.createElement("div");
  div.className = "comment";

  div.innerHTML = `
    <div class="comment-profile">
      <img src="/static/images/profile.jpg" class="show-profile-img">
    </div>
    <div class="comment-bubble">
      <div class="comment-user">${comment.nickname}</div>
      <div class="comment-text">${comment.text}</div>
    </div>
  `;

  return div;
}

function submitComment() {
  const commentInput = document.getElementById("comment");
  const text = commentInput.value.trim();

  if (text === "") {
    alert("댓글 내용을 입력하세요.");
    return;
  }

  const postId = currentPost.id;

  fetch("/koring/community/add_comment", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ post_id: postId, text: text }),
  })
    .then((res) => res.json())
    .then((data) => {
      if (!data.success) {
        alert("댓글 등록 실패");
        return;
      }
      comments.push({
        nickname: "나",
        text: text,
      });

      renderComments();
      commentInput.value = "";
    })
    .catch((err) => console.error(err));
}
