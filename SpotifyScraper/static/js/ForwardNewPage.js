// script.js
function downloadZip(url) {
    // Crea un link temporaneo per avviare il download
    var link = document.createElement("a");
    link.href = url;
    link.download = "songs.zip";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}



function runningScraping() {
    $('#loadingModal').modal('show');

    // Ottieni i dati dal form
    var url = document.getElementById('url').value;
    console.log("Button_pressed"); 
    console.log(url); 
    console.log(" IL JSON ")
    console.log(JSON.stringify({
            "url": url
                }))
    // Esegui la chiamata API
    fetch('/scrapingDownload', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            "url": url
        }),
    }).then(response => response.blob())
    .then(blob => {
        // Ricevuto il blob del file ZIP dal server
        hideLoadingModal();
        // Mostra il pulsante di download e gestisci il click
        var downloadButtonContainer = document.getElementById("downloadButtonContainer");
        downloadButtonContainer.style.display = "block";
        var downloadButton = document.getElementById("downloadButton");
        downloadButton.onclick = function() {
            // Crea un URL temporaneo per il blob e passalo alla funzione downloadZip
            var url = window.URL.createObjectURL(blob);
            downloadZip(url);
        };
    })
    
    .catch((error) => {
        console.error('Errore durante la chiamata API:', error);
        // Gestisci eventuali errori qui
    });
};

// Funzione per nascondere il modal di caricamento
function hideLoadingModal() {
    $('#loadingModal').modal('hide');
}
