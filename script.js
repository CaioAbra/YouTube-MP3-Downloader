function updateQuality() {
    var link = document.getElementById("youtube-link").value;
    if (!link) {
        alert("Insira um link do YouTube!");
        return;
    }

    window.pywebview.api.validate_quality(link);
    document.getElementById("quality-select").innerHTML = "<option>Atualizando...</option>";
}

function download() {
    var link = document.getElementById("youtube-link").value;
    var quality = document.getElementById("quality-select").value;
    var downloadFolder = document.getElementById("selected-folder").value;

    if (!link) {
        alert("Insira um link do YouTube!");
        return;
    }

    if (quality === "Escolha uma opção...") {
        alert("Selecione uma qualidade para baixar.");
        return;
    }

    if (!downloadFolder || downloadFolder === "Nenhuma pasta selecionada") {
        alert("Selecione uma pasta de destino válida.");
        return;
    }

    updateProgress("Iniciando download...");

    window.pywebview.api.download(link, quality, downloadFolder).then(function () {
        updateProgress("Download concluído!");
    }).catch(function (error) {
        updateProgress(`Erro durante o download: ${error}`);
    });
}

function validateQuality() {
    var link = document.getElementById("youtube-link").value;
    if (!link) {
        alert("Insira um link do YouTube!");
        return;
    }

    if (!isValidYoutubeLink(link)) {
        alert("O link do YouTube inserido não é válido.");
        return;
    }

    window.pywebview.api.validate_quality(link);
    document.getElementById("quality-select").innerHTML = "<option>Verificando...</option>";
}

function isValidYoutubeLink(link) {
    return link.startsWith("https://www.youtube.com/");
}

function chooseFolder() {
    window.pywebview.api.choose_folder().then(function (folder) {
        if (folder) {
            document.getElementById("selected-folder").value = folder;
        } else {
            document.getElementById("selected-folder").value = "Nenhuma pasta selecionada";
        }
    }).catch(function (error) {
        console.error('Erro ao selecionar a pasta:', error);
    });
}

function clearFields() {
    document.getElementById("youtube-link").value = "";
    var qualitySelect = document.getElementById("quality-select");
    qualitySelect.innerHTML = "";
    var defaultOption = document.createElement("option");
    defaultOption.text = "Escolha uma opção...";
    qualitySelect.add(defaultOption);
    document.getElementById("selected-folder").value = "";
    document.getElementById("progress-label").innerText = "";
}

function updateProgress(message) {
    var progressLabel = document.getElementById("progress-label");
    progressLabel.innerHTML = message;
}
