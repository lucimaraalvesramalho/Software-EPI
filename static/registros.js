// Este arquivo controla os registros de entrega e devolução dos EPIs.
// Aqui é possível cadastrar, buscar, editar e excluir registros.

// Procura a barra de ferramentas da página.
const toolbar = document.getElementById("toolbar");

// Procura o botão de salvar.
const saveBtn = document.querySelector(".save-btn");

// Procura o formulário de registros.
const registrosForm = document.getElementById('registrosForm');

// Verifica se o formulário existe.
if (registrosForm) {

    // Escuta o envio do formulário.
    registrosForm.addEventListener('submit', async (event) => {

        // Impede que a página recarregue automaticamente.
        event.preventDefault();

        // Cria um objeto contendo os dados informados pelo usuário.
        const dados = {

            // Matrícula do funcionário.
            matricula_funcionario: document.getElementById('matricula').value,

            // Certificado de Aprovação (CA) do EPI.
            ca_EPI: document.getElementById('ca').value,

            // Data prevista para devolução.
            data_devolucao: document.getElementById('data-devolucao').value,

            // Inicialmente o EPI ainda não foi trocado.
            data_troca: null,

            // Inicialmente não existe motivo de devolução.
            motivo_devolucao: null
        };

        // Envia os dados para a API utilizando o método POST.
        const resposta = await fetch('/api/registro', {
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
        alert(resultado.message || 'Erro ao criar Registro');

        // Se o cadastro foi realizado com sucesso.
        if (resposta.ok) {

            // Limpa o formulário.
            registrosForm.reset();
        }
    });
}

// Função responsável por buscar todos os registros cadastrados.
async function buscarRegistros() {

    // Remove o estado ativo da barra de ferramentas.
    document
        .getElementById("toolbar")
        .classList.remove("ativo");

    // Remove o modo de edição.
    document
        .getElementById("toolbar")
        .classList.remove("editando");

    // Faz uma requisição para buscar todos os registros.
    const resposta = await fetch('/api/registro/');

    // Converte a resposta para JSON.
    const usuarios = await resposta.json();

    // Localiza o corpo da tabela.
    const tbody = document.getElementById('registrosBody');

    // Limpa todas as linhas existentes.
    tbody.innerHTML = "";

    // Percorre todos os registros recebidos.
    usuarios.forEach(usuario => {

        // Cria uma nova linha na tabela.
        tbody.innerHTML += `
        <tr>

            <!-- Botão de seleção -->
            <td>
                <input
                    type="radio"
                    name="registro"
                    value="${usuario.matricula_funcionario}/${usuario.ca_EPI}"
                >
            </td>

            <!-- Matrícula do funcionário -->
            <td>${usuario.matricula_funcionario}</td>

            <!-- CA do EPI -->
            <td>${usuario.ca_EPI}</td>

            <!-- Data de devolução -->
            <td>${usuario.data_devolucao}</td>

            <!-- Data da entrega -->
            <td>${usuario.data_entrega}</td>

            <!-- Data da troca ou mensagem padrão -->
            <td>${usuario.data_troca ?? "Não trocado"}</td>

            <!-- Motivo da devolução ou situação do EPI -->
            <td>${usuario.motivo_devolucao ?? "Em uso"}</td>

        </tr>`;
    });
}

// Função responsável por excluir um registro.
async function deletarRegistro() {

    // Procura o registro selecionado.
    const selecionado = document.querySelector(
        'input[name="registro"]:checked'
    );

    // Se nenhum registro foi selecionado.
    if (!selecionado) {

        // Exibe uma mensagem.
        alert("Selecione um registro");
        return;
    }

    // Guarda a identificação do registro.
    const matricula = selecionado.value;

    // Envia a requisição DELETE para a API.
    const resposta = await fetch(
        `/api/registro/${matricula}`,
        {
            method: 'DELETE'
        }
    );

    // Recebe a resposta da API.
    const resultado = await resposta.json();

    // Exibe uma mensagem de sucesso ou erro.
    alert(resultado.message || 'Erro ao deletar Registro');

    // Se a exclusão foi realizada com sucesso.
    if (resposta.ok) {

        // Atualiza novamente a tabela.
        buscarRegistros();
    }
}

// Função responsável por colocar um registro em modo de edição.
async function editarRegistro() {

    // Procura o registro selecionado.
    const selecionado = document.querySelector(
        'input[name="registro"]:checked'
    );

    // Se nenhum registro foi selecionado.
    if (!selecionado) {

        // Exibe uma mensagem.
        alert("Selecione um registro");
        return;
    }

    // Obtém a linha correspondente.
    const linha = selecionado.closest("tr");

    // Transforma a matrícula em campo editável.
    linha.cells[1].innerHTML =
        `<input value="${linha.cells[1].textContent}">`;

    // Transforma o CA em campo editável.
    linha.cells[2].innerHTML =
        `<input value="${linha.cells[2].textContent}">`;

    // Transforma a data de devolução em campo do tipo date.
    linha.cells[3].innerHTML =
        `<input type="date" value="${linha.cells[3].textContent}">`;

    // Transforma a data de troca em campo do tipo date.
    linha.cells[5].innerHTML =
        `<input type="date" value="${linha.cells[5].textContent}">`;

    // Transforma o motivo da devolução em campo editável.
    linha.cells[6].innerHTML =
        `<input value="${linha.cells[6].textContent}">`;

    // Ativa o modo de edição da barra de ferramentas.
    toolbar.classList.add("editando");
}

// Função responsável por salvar as alterações do registro.
async function salvarRegistro() {

    // Procura o registro selecionado.
    const selecionado = document.querySelector(
        'input[name="registro"]:checked'
    );

    // Se nenhum registro estiver selecionado.
    if (!selecionado) {

        // Exibe uma mensagem.
        alert("Selecione um registro");
        return;
    }

    // Obtém a linha correspondente.
    const linha = selecionado.closest("tr");

    // Pega todos os campos editáveis da linha.
    const inputs = linha.querySelectorAll("input");

    // Cria um objeto com os novos dados.
    const dados = {

        // Matrícula atualizada.
        matricula_funcionario: inputs[1].value,

        // CA atualizado.
        ca_EPI: inputs[2].value,

        // Nova data de devolução.
        data_devolucao: inputs[3].value || null,

        // Nova data de troca.
        data_troca: inputs[4].value || null,

        // Novo motivo da devolução.
        motivo_devolucao: inputs[5].value || null
    };

    // Divide o valor do botão de seleção para obter
    // a matrícula original e o CA original.
    const [matriculaOriginal, caOriginal] =
        selecionado.value.split("/");

    // Mostra os dados no console para testes.
    console.log(dados);

    // Envia as alterações para a API utilizando o método PUT.
    const resposta = await fetch(
        `/api/registro/${matriculaOriginal}/${caOriginal}`,
        {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },

            // Converte os dados para JSON.
            body: JSON.stringify(dados)
        }
    );

    // Recebe a resposta da API.
    const resultado = await resposta.json();

    // Exibe uma mensagem de sucesso ou erro.
    alert(
        resultado.message ||
        resultado.erro ||
        "Erro ao atualizar registro"
    );

    // Se a atualização foi realizada com sucesso.
    if (resposta.ok) {

        // Atualiza novamente a lista de registros.
        buscarRegistros();
    }
}