document.addEventListener('DOMContentLoaded', function() {
    let nav = document.querySelectorAll('.sidenav');
    M.Sidenav.init(nav);
  });

  document.addEventListener('DOMContentLoaded', function() {
    let records= document.querySelectorAll('.collapsible');
    M.Collapsible.init(records);
  });