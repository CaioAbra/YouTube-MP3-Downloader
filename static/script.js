function updateQualityOptions(qualities) {
    var qualityMenu = document.getElementById("quality-select");
    qualityMenu.innerHTML = "";  // Limpa as opções atuais

    for (var i = 0; i < qualities.length; i++) {
        var option = document.createElement("option");
        option.text = qualities[i];
        qualityMenu.add(option);
    }
}

function updateProgress(message) {
    var progressLabel = document.getElementById("progress-label");
    progressLabel.innerHTML = message;
}

function handleError(error) {
    console.error('Erro:', error);
}

function validateQuality() {
    var link = document.getElementById("youtube-link").value;
    if (!link) {
        alert("Insira um link do YouTube!");
        return;
    }

    window.pywebview.api.validate_quality(link);
    document.getElementById("quality-select").innerHTML = "<option>Verificando...</option>";
}

function chooseFolder() {
    window.pywebview.api.choose_folder().then(function (folder) {
        if (folder) {
            document.getElementById("selected-folder").value = folder;
        } else {
            document.getElementById("selected-folder").value = "Nenhuma pasta selecionada";
        }
    }).catch(function (error) {
        handleError(error);
    });
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
        handleError(error);
        updateProgress(`Erro durante o download: ${error}`);
    });
}

function clearFields() {
    document.getElementById("youtube-link").value = "";
    var qualitySelect = document.getElementById("quality-select");
    qualitySelect.innerHTML = ""; // Remove todas as opções
    var defaultOption = document.createElement("option");
    defaultOption.text = "Escolha uma opção...";
    qualitySelect.add(defaultOption); // Adiciona a opção padrão
    document.getElementById("selected-folder").value = "";
    document.getElementById("progress-label").innerText = "";
}
