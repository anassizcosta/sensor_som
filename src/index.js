let ocorrenciasAnteriores = [];


async function carregarOcorrencias() {

    try {

        const resposta = await fetch("/api/ocorrencias");

        if (!resposta.ok) {
            throw new Error("Erro ao buscar ocorrências");
        }

        const ocorrencias = await resposta.json();


        document.getElementById("bolinha").style.background = "#32d583";

        document.getElementById("statusTexto").textContent =
            "Sistema conectado";


        document.getElementById("totalOcorrencias").textContent =
            ocorrencias.length;


        mostrarTabela(ocorrencias);


        if (ocorrencias.length > 0) {

            const ultima = ocorrencias[0];

            mostrarUltimaOcorrencia(ultima);


            if (ocorrenciasAnteriores.length > 0) {

                if (ultima.id !== ocorrenciasAnteriores[0].id) {

                    mostrarAlerta();

                }

            }

        }


        ocorrenciasAnteriores = ocorrencias;


    } catch (erro) {

        console.log(erro);

        document.getElementById("bolinha").style.background = "#d92d20";

        document.getElementById("statusTexto").textContent =
            "Sistema desconectado";
    }
}


function mostrarTabela(ocorrencias) {

    const tabela =
        document.getElementById("tabelaOcorrencias");


    if (ocorrencias.length === 0) {

        tabela.innerHTML = `
            <tr>
                <td colspan="6">
                    Nenhuma ocorrência registrada.
                </td>
            </tr>
        `;

        return;
    }


    tabela.innerHTML = "";


    ocorrencias.forEach(function (ocorrencia) {

        const linha = document.createElement("tr");


        const data = formatarData(ocorrencia.data_hora);


        linha.innerHTML = `

            <td>
                ${ocorrencia.id}
            </td>

            <td>
                ${ocorrencia.tipo}
            </td>

            <td>
                ${data}
            </td>

            <td>
                <span class="status-tabela">
                    ${ocorrencia.status}
                </span>
            </td>

        `;


        tabela.appendChild(linha);

    });

}


function mostrarUltimaOcorrencia(ocorrencia) {

    const data = new Date(ocorrencia.data_hora);


    document.getElementById("ultimaHora").textContent =
        data.toLocaleTimeString("pt-BR", {
            hour: "2-digit",
            minute: "2-digit"
        });


    document.getElementById("ultimaData").textContent =
        data.toLocaleDateString("pt-BR");

}


function formatarData(dataBanco) {

    const data = new Date(dataBanco);


    return data.toLocaleString("pt-BR", {
        day: "2-digit",
        month: "2-digit",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit"
    });

}


function mostrarAlerta() {

    const alerta =
        document.getElementById("alerta");

    const sensor =
        document.getElementById("sensorStatus");


    alerta.classList.remove("escondido");

    sensor.textContent = "MOVIMENTO";


    setTimeout(function () {

        alerta.classList.add("escondido");

        sensor.textContent = "MONITORANDO";

    }, 4000);

}


carregarOcorrencias();


setInterval(function () {

    carregarOcorrencias();

}, 2000);