/*본 파일은 팀 프로젝트 내에서
다른 팀원이 구현한 기능이다.
본인은 해당 모듈을 기반으로 다른 기능과 연동 및 테스트를 진행하였다.*/


(function () {
  function qs(sel) { return document.querySelector(sel); }
  const sidebar = qs('#globalSidebar');
  const overlay = qs('#sidebarOverlay');
  const toggle = qs('#sidebarToggle');
  const closeBtn = qs('#sidebarClose');

  if (!sidebar || !overlay || !toggle || !closeBtn) return;

  function openSidebar() {
    sidebar.hidden = false;
    overlay.hidden = false;
    // allow transition
    requestAnimationFrame(() => {
      sidebar.classList.add('open');
      document.body.classList.add('sidebar-open');
      toggle.setAttribute('aria-expanded', 'true');
    });
  }

  function closeSidebar() {
    sidebar.classList.remove('open');
    document.body.classList.remove('sidebar-open');
    toggle.setAttribute('aria-expanded', 'false');
    // wait for transition to end, then hide
    setTimeout(() => {
      sidebar.hidden = true;
      overlay.hidden = true;
    }, 240);
  }

  toggle.addEventListener('click', () => {
    const expanded = toggle.getAttribute('aria-expanded') === 'true';
    if (expanded) closeSidebar(); else openSidebar();
  });

  closeBtn.addEventListener('click', closeSidebar);
  overlay.addEventListener('click', closeSidebar);

  // Close on ESC
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeSidebar();
  });

  // Close when navigating via links inside the sidebar
  sidebar.addEventListener('click', (e) => {
    const link = e.target.closest('a');
    if (link && link.getAttribute('href')) closeSidebar();
  });
})();
