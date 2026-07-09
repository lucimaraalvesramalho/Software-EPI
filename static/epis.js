// Este arquivo controla a parte dos EPIs na tela.
// Aqui temos ações para inserir, buscar, editar e apagar EPIs.

// Espera a página carregar completamente.
document.addEventListener('DOMContentLoaded', () => {

    // Chama a função que busca todos os EPIs cadastrados.
    buscarEpi();
});

// Escuta qualquer alteração feita na página.
document.addEventListener("change", (e) => {

    // Verifica se a alteração foi em um botão de seleção (radio) chamado "registro".
    if (e.target.name === "registro") {

        // Mostra a barra de ferramentas quando um registro é selecionado.
        document.getElementById("toolbar").classList.add("ativo");
    }
});

// Procura o formulário de cadastro de EPI.
const epiForm = document.getElementById('epiForm');

// Verifica se o formulário existe na página.
if (epiForm) {

    // Escuta quando o formulário for enviado.
    epiForm.addEventListener('submit', async (event) => {

        // Impede que a página recarregue automaticamente.
        event.preventDefault();

        // Cria um objeto contendo os dados digitados pelo usuário.
        const dados = {

            // Nome do EPI.
            nome_epi: document.getElementById('nome').value,

            // Tipo do EPI.
            tipo_epi: document.getElementById('tipo').value,

            // Certificado de Aprovação (CA) convertido para letras maiúsculas.
            certificado_aprovacao_epi: document.getElementById('ca').value.toUpperCase(),

            // Data de validade do certificado.
            validade_certificado_aprovacao: document.getElementById('validade_ca').value
        };

        // Envia os dados para a API utilizando o método POST.
        const resposta = await fetch('/api/epi', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },

            // Converte o objeto para JSON.
            body: JSON.stringify(dados)
        });

        // Recebe a resposta da API.
        const resultado = await resposta.json();

        // Exibe uma mensagem de sucesso ou erro.
        alert(resultado.message || 'Erro ao cadastrar EPI');

        // Se o cadastro deu certo.
        if (resposta.ok) {

            // Limpa todos os campos do formulário.
            epiForm.reset();
        }
    });
}

// Função responsável por buscar todos os EPIs cadastrados.
async function buscarEpi() {

    // Procura a barra de ferramentas.
    const toolbar = document.getElementById("toolbar");

    // Se ela existir.
    if (toolbar) {

        // Remove o estado ativo.
        toolbar.classList.remove("ativo");

        // Remove o modo de edição.
        toolbar.classList.remove("editando");
    }

    // Faz uma requisição para buscar os EPIs.
    const resposta = await fetch('/api/epi/');

    // Converte a resposta em JSON.
    const funcionarios = await resposta.json();

    // Localiza o corpo da tabela.
    const tbody = document.getElementById('epiBody');

    // Limpa todas as linhas existentes.
    tbody.innerHTML = "";

    // Percorre cada EPI recebido da API.
    funcionarios.forEach(epi => {

        // Adiciona uma nova linha na tabela.
        tbody.innerHTML += `
            <tr>

                <!-- Coluna com botão de seleção -->
                <td>
                    <input
                        type="radio"
                        name="registro"
                        value="${epi.certificado_aprovacao_epi}"
                    >
                </td>

                <!-- Número do Certificado de Aprovação -->
                <td>${epi.certificado_aprovacao_epi}</td>

                <!-- Nome do EPI -->
                <td>${epi.nome_epi}</td>

                <!-- Tipo do EPI -->
                <td>${epi.tipo_epi}</td>

                <!-- Data de validade -->
                <td>${epi.validade_certificado_aprovacao}</td>

            </tr>
        `;
    });
}

// Função que permite editar um EPI.
function editarEpi() {

    // Procura o EPI selecionado.
    const selecionado = document.querySelector(
        'input[name="registro"]:checked'
    );

    // Se nenhum EPI foi selecionado.
    if (!selecionado) {

        // Exibe uma mensagem de aviso.
        alert("Selecione um funcionário");
        return;
    }

    // Obtém a linha correspondente ao EPI selecionado.
    const linha = selecionado.closest("tr");

    // Transforma a célula do nome em um campo de texto.
    linha.cells[2].innerHTML =
        `<input class="edit" value="${linha.cells[2].textContent}">`;

    // Transforma a célula do tipo em um campo de texto.
    linha.cells[3].innerHTML =
        `<input class="edit" value="${linha.cells[3].textContent}">`;

    // Transforma a validade em um campo de data.
    linha.cells[4].innerHTML =
        `<input class="edit" type="date" value="${linha.cells[4].textContent}">`;

    // Coloca a barra de ferramentas em modo de edição.
    document
        .getElementById("toolbar")
        .classList.add("editando");
}

// Função responsável por salvar as alterações.
async function salvarEpi() {

    // Procura o EPI selecionado.
    const selecionado = document.querySelector(
        'input[name="registro"]:checked'
    );

    // Se nenhum EPI estiver selecionado.
    if (!selecionado) {

        // Exibe um aviso.
        alert("Selecione um funcionário");
        return;
    }

    // Obtém a linha da tabela.
    const linha = selecionado.closest("tr");

    // Pega todos os campos de edição da linha.
    const inputs = linha.querySelectorAll("input");

    // Monta um objeto com os novos dados.
    const dados = {

        // Novo nome.
        nome_epi: inputs[1].value,

        // Novo tipo.
        tipo_epi: inputs[2].value,

        // Nova validade.
        validade_certificado_aprovacao: inputs[3].value,
    };

    // Guarda o número do CA.
    const ca = selecionado.value;

    // Envia as alterações utilizando o método PUT.
    const resposta = await fetch(
        `/api/epi/${ca}`,
        {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },

            // Envia os novos dados.
            body: JSON.stringify(dados)
        }
    );

    // Recebe a resposta da API.
    const resultado = await resposta.json();

    // Exibe a mensagem retornada.
    alert(
        resultado.message ||
        resultado.erro ||
        "Erro ao atualizar epi"
    );

    // Se a atualização deu certo.
    if (resposta.ok) {

        // Atualiza novamente a lista de EPIs.
        buscarEpi();
    }
}

// Função responsável por excluir um EPI.
async function deletarEpi() {

    // Procura o EPI selecionado.
    const selecionado = document.querySelector(
        'input[name="registro"]:checked'
    );

    // Se nenhum EPI foi selecionado.
    if (!selecionado) {

        // Exibe uma mensagem de aviso.
        alert("Selecione um Epi");
        return;
    }

    // Guarda o número do CA.
    const ca = selecionado.value;

    // Pergunta se o usuário realmente deseja excluir.
    if (!confirm(`Excluir funcionário ${ca}?`)) {

        // Se cancelar, encerra a função.
        return;
    }

    // Envia a requisição DELETE para a API.
    const resposta = await fetch(
        `/api/epi/${ca}`,
        {
            method: "DELETE"
        }
    );

    // Recebe a resposta da API.
    const resultado = await resposta.json();

    // Exibe a mensagem retornada.
    alert(
        resultado.message ||
        resultado.erro ||
        "Erro ao excluir epi"
    );

    // Se a exclusão foi realizada com sucesso.
    if (resposta.ok) {

        // Atualiza a tabela de EPIs.
        buscarEpi();
    }
}