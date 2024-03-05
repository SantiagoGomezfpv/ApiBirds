async function uploadAudio() {
    const form = document.getElementById('audioForm');
    const statusMessage = document.getElementById('statusMessage');
    const formData = new FormData(form);

    try {
        const response = await fetch('/Selecciona_tu_Audio', {
            method: 'POST',
            body: formData,
        });

        const result = await response.text();
        statusMessage.innerHTML = result;

        // Después de cargar el audio, actualiza automáticamente el elemento de audio
        await playAudio();
    } catch (error) {
        console.error('Error uploading audio:', error);
        statusMessage.innerHTML = 'Error al cargar el audio.';
    }
}

async function playAudio() {
    const audioPlayer = document.getElementById('audioPlayer');

    try {
        const response = await fetch('/Reproducir_tu_Audio');
        const audioBlob = await response.blob();

        const audioUrl = URL.createObjectURL(audioBlob);
        audioPlayer.src = audioUrl;
        audioPlayer.play();  // Inicia la reproducción automáticamente
    } catch (error) {
        console.error('Error playing audio:', error);
        alert('Error al reproducir el audio.');
    }
}

function calcularPorcentajeExponencial(arreglo) {
    const totalElementos = arreglo.length;
    let porcentajeBase = 0.7; // Porcentaje base del 70%

    if (totalElementos <= 5) {
        // Si el tamaño del arreglo es 5 o menor, simplemente multiplica por el 70%
        return porcentajeBase * 100; // Multiplica por 100 para obtener el porcentaje como número entero
    } else if (totalElementos <= 10) {
        // Si el tamaño del arreglo está entre 6 y 10, realiza un cálculo exponencial
        const baseExponencial = 0.95; // Puedes ajustar este valor según tus necesidades
        return (Math.pow(baseExponencial, totalElementos - 5) * porcentajeBase) * 100;
    } else {
        // Si el tamaño del arreglo es mayor que 10, utiliza una aproximación al 50%
        const porcentajeLimite = 0.5; // Porcentaje límite del 50%
        const porcentajeAproximado = porcentajeLimite + (totalElementos - 10) * 0.01; // Ajusta el valor 0.01 según tus necesidades
        return porcentajeAproximado * 100;
    }
}

function calcularPorcentajes(arreglo) {
    const frecuencias = {};
    
    // Contar la frecuencia de cada elemento en el arreglo
    arreglo.forEach(elemento => {
        frecuencias[elemento] = (frecuencias[elemento] || 0) + 1;
    });

    // Calcular el porcentaje para cada elemento
    const porcentajes = {};
    const totalElementos = arreglo.length;
    const PorcentajeArreglo = calcularPorcentajeExponencial(arreglo);
    const PorcentajeOtra = (100 - PorcentajeArreglo)

    Object.keys(frecuencias).forEach(elemento => {
        const frecuencia = frecuencias[elemento];
        
        const porcentaje = (frecuencia / totalElementos) * PorcentajeArreglo; // 70% del tamaño del arreglo
        porcentajes[elemento] = porcentaje.toFixed(0); // Redondear a dos decimales
    });
    return [porcentajes, PorcentajeOtra];
}

async function identificarEspecies() {
    const resultSection = document.getElementById('resultSection');

    try {
        const response = await fetch('/Ejecuta_El_Clasificador');
        const result = await response.text();

        
        if (result == 'Internal Server Error'){
            // Muestra el resultado en la interfaz
            resultSection.innerHTML = `<h3>Resultado del Clasificador:</h3><p>Audio no valido</p>`;
        }else{
            const arreglo = result.split(" - ");
            // console.log(arreglo);
            const [resultFinal, OtrasEspecies ] = calcularPorcentajes(arreglo);
            console.log(resultFinal);
            console.log(`Es un ${OtrasEspecies}% especie no identificada`);
            
            resultSection.innerHTML = '';
            resultSection.innerHTML = `<h2>Posibles especies encontradas: </h2>`;
            resultSection.innerHTML += `<li>${OtrasEspecies.toFixed(0)}% - <strong>Especie desconocida</strong></li>`;
            Object.keys(resultFinal).forEach(ave => {
                const porcentaje = resultFinal[ave];
                const elementoHTML = `<li>${porcentaje}% - <strong>${ave}</strong></li>`;
                resultSection.innerHTML += elementoHTML;
            });
        }
    } catch (error) {
        console.error('Error executing classifier:', error);
        alert('Error al ejecutar el clasificador.');
    }
}