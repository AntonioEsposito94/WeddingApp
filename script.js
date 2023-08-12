// Codice JavaScript come descritto nei passaggi precedenti

// Funzione per attivare la fotocamera e scattare una foto
async function takePhoto(objective) {
    console.log('Avvio della funzione takePhoto...');
    const constraints = {
        video: { facingMode: 'environment' },
    };

    try {
        const stream = await navigator.mediaDevices.getUserMedia(constraints);
        const videoElement = document.getElementById('video');
        videoElement.srcObject = stream;
        videoElement.play();

        videoElement.onloadedmetadata = () => {
            console.log('Fotocamera attivata con successo.');
            const canvasElement = document.getElementById('canvas');
            const context = canvasElement.getContext('2d');

            canvasElement.width = videoElement.videoWidth;
            canvasElement.height = videoElement.videoHeight;

            context.drawImage(videoElement, 0, 0, canvasElement.width, canvasElement.height);
            stream.getTracks().forEach(track => track.stop());

            const photo = canvasElement.toDataURL('image/jpeg', 1.0);
            photos[objective] = photo;
            console.log(`Foto scattata per l'obiettivo: ${objective}`);
            console.log('Foto salvata in photos:', photos);

            const allPhotosTaken = Object.keys(photos).length === objectives.length;
            const uploadBtn = document.querySelector('button[type="button"]');
            uploadBtn.disabled = !allPhotosTaken;

            // Mostra la miniatura della foto appena scattata
            const objectiveDiv = document.getElementById(objective);
            objectiveDiv.innerHTML = `<img src="${photo}" alt="${objective}" style="width: 150px; height: 150px;">`;
            const takePhotoBtn = objectiveDiv.previousElementSibling;
            takePhotoBtn.style.display = 'none';

            // Mostra l'input del file per l'obiettivo
            const fileInput = document.getElementById(objective);
            fileInput.style.display = 'block';
        };
    } catch (error) {
        console.error('Errore nell\'acquisizione della fotocamera:', error);
    }
}

// Inizializza la generazione dinamica degli obiettivi
generateObjectivesList();
