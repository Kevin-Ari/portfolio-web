/* Datos de ejemplo: reemplaza por los tuyos o consume una API */
const projects = [
{id:1,title:"API de tareas con FastAPI",desc:"Una API REST para gestionar tareas con autenticación JWT.",tags:["python","fastapi","backend"],live:'#',code:'#'},
{id:2,title:"Pipeline ETL con Spark",desc:"ETL en PySpark que procesa logs y los exporta a BigQuery.",tags:["spark","etl","data"],live:'#',code:'#'},
{id:3,title:"Dashboard con Streamlit",desc:"Dashboard interactivo para métricas de negocio.",tags:["python","frontend"],live:'#',code:'#'},
{id:4,title:"Microservicio de autenticación",desc:"Servicio de auth con OAuth2 y OpenID Connect.",tags:["fastapi","security"],live:'#',code:'#'}
];


const grid = document.getElementById('grid');
const q = document.getElementById('q');
const empty = document.getElementById('empty');


function render(list){
grid.innerHTML = '';
if(list.length===0){ empty.style.display='block'; return }
empty.style.display='none';
for(const p of list){
const card = document.createElement('article'); card.className='card';
card.innerHTML = `
<h3>${p.title}</h3>
<p>${p.desc}</p>
<div class="tags">${p.tags.map(t=>`<span class="tag" onclick="filterTag('${t}')">${t}</span>`).join('')}</div>
<div class="actions">
<a class="live" href="${p.live}" target="_blank">Ver</a>
<a class="code" href="${p.code}" target="_blank">Código</a>
</div>
`;
grid.appendChild(card);
}
}


function filterTag(tag){
q.value=''; render(projects.filter(p=>p.tags.includes(tag)));
}


function resetFilters(){ q.value=''; render(projects); }


q.addEventListener('input', ()=>{
const term = q.value.trim().toLowerCase();
if(!term) return render(projects);
render(projects.filter(p=> (p.title+p.desc+p.tags.join(' ')).toLowerCase().includes(term)));
});


// Inicializar
render(projects);