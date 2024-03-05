# source env/Scripts/activate
# uvicorn main:app --reload

import uvicorn
from fastapi import FastAPI, Request, Response, UploadFile, File
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from mangum import Mangum
from os import getcwd
from CNN import Modelo

description = """
Se entrenó una red neuronal convolucional con una base de datos de sonidos de diferentes especies de aves y 
se logró con esto implementar un modelo para la identificación automática de especies de aves a partir de 
su paisaje sonoro. Esta API tiene como base el modelo mencionado anteriormente con capacidad de identificar 
397 especies de aves a partir de su canto.

## Santiago Gómez Ortega (Estudiante de Ingeniería Electrónica)

### Asesores
* **Andrés Eduardo Castro Ospina**, docente Facultad de Ingenierías, Instituto Tecnológico Metropolitano. \n
* **Juan David Martínez Vargas**, docente Facultad de Ingenierías, Instituto Tecnológico Metropolitano.

Instituto Tecnológico Metropolitano - ITM.\n
Medellín, Colombia.
"""
app = FastAPI(title="🐦🦉 Modelo basado en CNN para la identificación de especies de aves a partir de grabaciones de paisajes sonoros. 🦅🦜",
            version="0.0.1",
            description= description,)
app.mount("/static", StaticFiles(directory="./public/static"), name="static")

@app.get('/', response_class=HTMLResponse)
def root():
    htmlAddress = "./public/static/html/index.html"
    return FileResponse(htmlAddress, status_code=200)

@app.post('/Selecciona_tu_Audio', tags=["Audio"])
async def Cargar_Archivo(file:UploadFile=File(...)):
    with open(getcwd() + "/" + "AudioModelo.ogg", "wb") as myfile:
        content = await file.read()           
        myfile.write(content)
        myfile.close()
    return "Audio Cargado con Exito"

@app.get('/Reproducir_tu_Audio', tags=["Audio"])
def Mostrar_Archivo():
    return FileResponse(getcwd() + "/" + "AudioModelo.ogg")

@app.get('/Ejecuta_El_Clasificador', tags=["Audio"])
def Identificar_Especies():
    prediction = Modelo()
    return Response(content=prediction, media_type="application/xml")

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)