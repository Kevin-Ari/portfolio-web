console.log('✅ Frontend JavaScript cargado correctamente');

// Cargar proyectos desde la API
async function loadProjects() {
    try {
        const response = await fetch('/api/projects');
        const projects = await response.json();
        
        const container = document.getElementById('projects');
        container.innerHTML = `
            <h2>Proyectos: ${projects.length}</h2>
            <pre>${JSON.stringify(projects, null, 2)}</pre>
        `;
    } catch (error) {
        console.error('Error cargando proyectos:', error);
    }
}

// Cargar al inicio
loadProjects();