 // Toggle user menu
 const userMenuButton = document.getElementById('user-menu-button');
 const userMenu = document.getElementById('user-menu');

 userMenuButton.addEventListener('click', () => {
     userMenu.classList.toggle('hidden');
 });

 // Close user menu when clicking outside
 document.addEventListener('click', (event) => {
     if (!userMenuButton.contains(event.target) && !userMenu.contains(event.target)) {
         userMenu.classList.add('hidden');
     }
 });


// Update footer information
function updateFooterInfo() {
     const now = new Date();
     
     // Update time
     const timeElement = document.getElementById('current-time');
     timeElement.textContent = now.toLocaleTimeString();
     
     // Update day
     const dayElement = document.getElementById('current-day');
     const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
     dayElement.textContent = days[now.getDay()];
     
     // Update date
     const dateElement = document.getElementById('current-date');
     dateElement.textContent = now.toLocaleDateString();
 }

 // Initial call and set interval
 updateFooterInfo();
 setInterval(updateFooterInfo, 1000);








 function toggleSubmenu(menuId) {
    const submenu = document.getElementById(`${menuId}-submenu`);
    const arrow = document.getElementById(`${menuId}-arrow`);
    
    // Close all other submenus with animation
    const allSubmenus = document.querySelectorAll('[id$="-submenu"]');
    const allArrows = document.querySelectorAll('[id$="-arrow"]');
    
    allSubmenus.forEach(menu => {
      if (menu.id !== `${menuId}-submenu` && menu.classList.contains('submenu-expanded')) {
        menu.classList.add('submenu-collapsed');
        setTimeout(() => {
          menu.classList.remove('submenu-expanded', 'submenu-collapsed');
        }, 300);
      }
    });
    
    allArrows.forEach(arr => {
      if (arr.id !== `${menuId}-arrow`) {
        arr.classList.remove('arrow-rotated');
      }
    });
    
    // Toggle current submenu with animation
    if (!submenu.classList.contains('submenu-expanded')) {
      submenu.classList.add('submenu-expanded');
      arrow.classList.add('arrow-rotated');
    } else {
      submenu.classList.add('submenu-collapsed');
      arrow.classList.remove('arrow-rotated');
      setTimeout(() => {
        submenu.classList.remove('submenu-expanded', 'submenu-collapsed');
      }, 300);
    }
  }
  
  document.addEventListener('DOMContentLoaded', function() {
    const menuButtons = document.querySelectorAll('.sidebar-group button');
    menuButtons.forEach(button => {
      button.addEventListener('click', function(e) {
        e.preventDefault();
      });
    });
  });