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

 // Smooth animation for sidebar submenus
 const sidebarButtons = document.querySelectorAll('.sidebar-button');
 sidebarButtons.forEach(button => {
     button.addEventListener('click', () => {
         const submenu = button.nextElementSibling;
         submenu.classList.toggle('open');
     });
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