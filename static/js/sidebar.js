document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.getElementById('sidebar');
    const toggleBtn = document.getElementById('toggleSidebar');
    const menuLinks = document.querySelectorAll('.menu-links a, .bottom-content a');

    let isMobile = window.innerWidth <= 768;
    const isClosed = localStorage.getItem('isSidebarClosed') === 'true';
    
    if (isClosed || isMobile) sidebar.classList.add('close');

    ajustarContenedor();

    toggleBtn.addEventListener('click', () => {
        sidebar.classList.toggle('close');
        localStorage.setItem('isSidebarClosed', sidebar.classList.contains('close'));
        
        ajustarContenedor();
        actualizarIcono();
    });

    menuLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (isMobile) {
                sidebar.classList.add('close');
                localStorage.setItem('isSidebarClosed', true);
                ajustarContenedor();
            }
        });
    });

    function actualizarIcono() {
        if (isMobile) {
            toggleBtn.className = sidebar.classList.contains('close') ? 'bx toggle botonDesplegable bx-chevron-up' : 'bx toggle botonDesplegable bx-chevron-down';
        } else {
            
            toggleBtn.className = sidebar.classList.contains('close') ? 'bx toggle botonDesplegable bx-chevron-left' : 'bx toggle botonDesplegable bx-chevron-right';
        }

        
    }

    function ajustarContenedor() {
        
        isMobile = window.innerWidth <= 768;
        if (isMobile) {
            //Agregamos la clase sidebar la clase isMobile para que el contenedor se ajuste a la pantalla
            sidebar.classList.add('isMobile');
            document.documentElement.style.setProperty('--left', '0px');
            document.documentElement.style.setProperty('--top', '78px');
        } else {
            sidebar.classList.remove('isMobile');
            document.documentElement.style.setProperty('--left', sidebar.classList.contains('close') ? '88px' : '250px');
            document.documentElement.style.setProperty('--top', '0px');
        }
        actualizarIcono();
    }

    window.addEventListener('resize', ajustarContenedor);
});
