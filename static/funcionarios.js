// Este arquivo controla o cadastro e o gerenciamento dos funcionários.
// Aqui é possível cadastrar, buscar, editar e excluir funcionários.

// Procura o formulário de cadastro de funcionário.
const funcionarioForm = document.getElementById('funcionarioForm');

// Verifica se o formulário existe na página.
if (funcionarioForm) {

    // Escuta o envio do formulário.
    funcionarioForm.addEventListener('submit', async (event) => {

        // Impede que a página recarregue automaticamente.
        event.preventDefault();

        // Cria um objeto com todos os dados preenchidos pelo usuário.
        const dados = {

            // Matrícula do funcionário convertida para letras maiúsculas.
            matricula_funcionario: document.getElementById('matricula').value.toUpperCase(),

            // Nome do funcionário.
            nome_funcionario: document.getElementById('nome').value,

            // CPF do funcionário.
            cpf_funcionario: document.getElementById('cpf').value,

            // Setor onde o funcionário trabalha.
            setor_funcionario: document.getElementById('setor').value,

            // Função exercida pelo funcionário.
            funcao_funcionario: document.getElementById('funcao').value,

            // Data de admissão.
            data_admissao_funcionario: document.getElementById('data_admissao').value,

            // Telefone do funcionário.
            telefone: document.getElementById('telefone').value,

            // E-mail do funcionário.
            email: document.getElementById('email').value,

            // WhatsApp do funcionário.
            whatsapp: document.getElementById('whatsapp').value
        };

        // Envia os dados para a API utilizando o método POST.
        const resposta = await fetch('/api/funcionario', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },

            // Converte o objeto para JSON antes de enviar.
            body: JSON.stringify(dados)
        });

        // Recebe a resposta da API.
        const resultado = await resposta.json();

        // Exibe uma mensagem de sucesso ou erro.
        alert(resultado.message || 'Erro ao cadastrar funcionário');

        // Se o cadastro foi realizado com sucesso.
        if (resposta.ok) {

            // Limpa todos os campos do formulário.
            funcionarioForm.reset();
        }
    });
}

// Função responsável por formatar automaticamente o CPF.
function formatarCPF(input) {

    // Remove qualquer caractere que não seja número.
    let v = input.value.replace(/\D/g, "");

    // Coloca o primeiro ponto.
    v = v.replace(/(\d{3})(\d)/, "$1.$2");

    // Coloca o segundo ponto.
    v = v.replace(/(\d{3})(\d)/, "$1.$2");

    // Coloca o traço final.
    v = v.replace(/(\d{3})(\d{1,2})$/, "$1-$2");

    // Atualiza o campo formatado.
    input.value = v;
}

// Função responsável por formatar automaticamente o telefone.
function formatarTelefone(input) {

    // Remove tudo que não for número.
    let v = input.value.replace(/\D/g, "");

    // Coloca os parênteses do DDD.
    v = v.replace(/(\d{2})(\d)/, "($1) $2");

    // Coloca o traço no número.
    v = v.replace(/(\d{5})(\d)/, "$1-$2");

    // Atualiza o campo.
    input.value = v;
}

// Espera toda a página carregar.
document.addEventListener('DOMContentLoaded', () => {

    // Busca todos os funcionários cadastrados.
    buscarFuncionarios();
});

// Escuta alterações na página.
document.addEventListener("change", (e) => {

    // Quando um funcionário for selecionado.
    if (e.target.name === "registro") {

        // Mostra a barra de ferramentas.
        document.getElementById("toolbar").classList.add("ativo");
    }
});

// Função que busca todos os funcionários cadastrados.
async function buscarFuncionarios() {

    // Procura a barra de ferramentas.
    const toolbar = document.getElementById("toolbar");

    // Se existir.
    if (toolbar) {

        // Remove o estado ativo.
        toolbar.classList.remove("ativo");

        // Remove o modo de edição.
        toolbar.classList.remove("editando");
    }

    // Faz uma requisição para buscar os funcionários.
    const resposta = await fetch('/api/funcionario/');

    // Converte a resposta para JSON.
    const funcionarios = await resposta.json();

    // Localiza o corpo da tabela.
    const tbody = document.getElementById('funcBody');

    // Limpa todas as linhas existentes.
    tbody.innerHTML = "";

    // Percorre todos os funcionários recebidos.
    funcionarios.forEach(funcionario => {

        // Cria uma nova linha na tabela.
        tbody.innerHTML += `
            <tr>

                <!-- Botão de seleção -->
                <td>
                    <input
                        type="radio"
                        name="registro"
                        value="${funcionario.matricula_funcionario}"
                    >
                </td>

                <!-- Matrícula -->
                <td>${funcionario.matricula_funcionario}</td>

                <!-- Nome -->
                <td>${funcionario.nome_funcionario}</td>

                <!-- CPF -->
                <td>${funcionario.cpf_funcionario}</td>

                <!-- Setor -->
                <td>${funcionario.setor_funcionario}</td>

                <!-- Função -->
                <td>${funcionario.funcao_funcionario}</td>

                <!-- Data de admissão -->
                <td>${funcionario.data_admissao_funcionario}</td>

                <!-- Telefone -->
                <td>${funcionario.telefone}</td>

                <!-- E-mail -->
                <td>${funcionario.email}</td>

                <!-- WhatsApp -->
                <td>${funcionario.whatsapp}</td>

            </tr>
        `;
    });
}

// Função que coloca o funcionário selecionado em modo de edição.
function editarFuncionario() {

    // Procura o funcionário selecionado.
    const selecionado = document.querySelector(
        'input[name="registro"]:checked'
    );

    // Se nenhum funcionário foi selecionado.
    if (!selecionado) {

        // Exibe uma mensagem.
        alert("Selecione um funcionário");
        return;
    }

    // Obtém a linha correspondente.
    const linha = selecionado.closest("tr");

    // Transforma o nome em campo editável.
    linha.cells[2].innerHTML = `<input class="edit" value="${linha.cells[2].textContent}">`;

    // Transforma o CPF em campo editável.
    linha.cells[3].innerHTML = `<input class="edit" value="${linha.cells[3].textContent}">`;

    // Transforma o setor em campo editável.
    linha.cells[4].innerHTML = `<input class="edit" value="${linha.cells[4].textContent}">`;

    // Transforma a função em campo editável.
    linha.cells[5].innerHTML = `<input class="edit" value="${linha.cells[5].textContent}">`;

    // Transforma a data em campo do tipo date.
    linha.cells[6].innerHTML = `<input class="edit" type="date" value="${linha.cells[6].textContent}">`;

    // Transforma o telefone em campo editável.
    linha.cells[7].innerHTML = `<input class="edit" value="${linha.cells[7].textContent}">`;

    // Transforma o e-mail em campo editável.
    linha.cells[8].innerHTML = `<input class="edit" value="${linha.cells[8].textContent}">`;

    // Transforma o WhatsApp em campo editável.
    linha.cells[9].innerHTML = `<input class="edit" value="${linha.cells[9].textContent}">`;

    // Ativa o modo de edição na barra de ferramentas.
    document
        .getElementById("toolbar")
        .classList.add("editando");
}

// Função responsável por salvar as alterações.
async function salvarFuncionario() {

    // Procura o funcionário selecionado.
    const selecionado = document.querySelector(
        'input[name="registro"]:checked'
    );

    // Se nenhum funcionário estiver selecionado.
    if (!selecionado) {

        // Exibe uma mensagem.
        alert("Selecione um funcionário");
        return;
    }

    // Obtém a linha da tabela.
    const linha = selecionado.closest("tr");

    // Pega todos os campos de edição.
    const inputs = linha.querySelectorAll("input");

    // Cria um objeto com os novos dados.
    const dados = {

        // Novo nome.
        nome_funcionario: inputs[1].value,

        // Novo CPF.
        cpf_funcionario: inputs[2].value,

        // Novo setor.
        setor_funcionario: inputs[3].value,

        // Nova função.
        funcao_funcionario: inputs[4].value,

        // Nova data de admissão.
        data_admissao_funcionario: inputs[5].value,

        // Novo telefone.
        telefone: inputs[6].value,

        // Novo e-mail.
        email: inputs[7].value,

        // Novo WhatsApp.
        whatsapp: inputs[8].value
    };

    // Guarda a matrícula original.
    const matriculaOriginal = selecionado.value;

    // Envia os dados atualizados utilizando o método PUT.
    const resposta = await fetch(
        `/api/funcionario/${matriculaOriginal}`,
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

    // Exibe a mensagem retornada.
    alert(
        resultado.message ||
        resultado.erro ||
        "Erro ao atualizar funcionário"
    );

    // Se a atualização foi realizada com sucesso.
    if (resposta.ok) {

        // Atualiza novamente a tabela.
        buscarFuncionarios();
    }
}

// Função responsável por excluir um funcionário.
async function deletarFuncionario() {

    // Procura o funcionário selecionado.
    const selecionado = document.querySelector(
        'input[name="registro"]:checked'
    );

    // Se nenhum funcionário foi selecionado.
    if (!selecionado) {

        // Exibe uma mensagem.
        alert("Selecione um funcionário");
        return;
    }

    // Guarda a matrícula.
    const matricula = selecionado.value;

    // Confirma se o usuário realmente deseja excluir.
    if (!confirm(`Excluir funcionário ${matricula}?`)) {

        // Se cancelar, encerra a função.
        return;
    }

    // Envia a requisição DELETE para a API.
    const resposta = await fetch(
        `/api/funcionario/${matricula}`,
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
        "Erro ao excluir funcionário"
    );

    // Se a exclusão foi realizada com sucesso.
    if (resposta.ok) {

        // Atualiza novamente a lista de funcionários.
        buscarFuncionarios();
    }
}