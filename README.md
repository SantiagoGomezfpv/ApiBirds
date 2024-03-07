# 🐦🦉 Modelo basado en CNN para la identificación de especies de aves a partir de grabaciones de paisajes sonoros. 🦅🦜

<div align="center">
  <a href="https://apibirds.onrender.com">
    <img align="center" width="400" src="https://github.com/SantiagoGomezfpv/ApiBirds/blob/main/API-Birds.png">
  </a>
</div>
<br>
<div>
  <p>
    Se entrenó una red neuronal convolucional con una base de datos de sonidos de diferentes especies de aves y 
    se logró con esto implementar un modelo para la identificación automática de especies de aves a partir de 
    su paisaje sonoro. Esta API tiene como base el modelo mencionado anteriormente con capacidad de identificar 
    397 especies de aves a partir de su canto.
    <br>
    <li><strong>Santiago Gómez Ortega</strong> Ingeniero electrónico</li>
    <br>
    <strong>Asesores: </strong>
    <br> 
    <li><strong>Andrés Eduardo Castro Ospina,</strong> docente Facultad de Ingenierías, Instituto Tecnológico Metropolitano.</li>
    <li><strong>Juan David Martínez Vargas,</strong> docente Facultad de Ingenierías, Instituto Tecnológico Metropolitano.</li>
    <br>Instituto Tecnológico Metropolitano - ITM.
    <br>Medellín, Colombia.
  </p>
</div>

Actialmente la API se encuentra desplegada en una instancia gratuita de [Render](https://render.com) la que limita a 512MB(RAM) y 0.1CPU. 
Cuando la API hace el llamado a la IA para identificar la especie de ave se consume mas de la cantidad gratuita de recursos y se cae

[https://apibirds.onrender.com](https://apibirds.onrender.com)

>[!CAUTION]
> - Crashea al darle identificar especies 
> - Se queda sin memoria (usa más de 512 MB) 
> - Para ver el funcionamiento de la API es necesario clonar el repositorio y ejecutarlo local

## Instalación
1. Clona este repositorio:
`git clone https://github.com/SantiagoGomezfpv/ApiBirds.git`
2. Instalar requerimientos:
`pip install -r requirements.txt`
3. Ejecuta el proyecto:
`uvicorn main:app --reload`

- Pon `http://127.0.0.1:8000` en tu navegador para ver la aplicación en funcionamiento.
- Pon `http://127.0.0.1:8000/docs` en tu navegador para ver la funcionalidad e la aplicacion en FastApi.
