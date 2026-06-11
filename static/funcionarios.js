const funcionarioForm = document.getElementById('funcionarioForm');
if (funcionarioForm) {
    funcionarioForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const dados = {
            matricula_funcionario: document.getElementById('matricula').value.toUpperCase(),
            nome_funcionario: document.getElementById('nome').value,
            cpf_funcionario: document.getElementById('cpf').value,
            setor_funcionario: document.getElementById('setor').value,
            funcao_funcionario: document.getElementById('funcao').value,
            data_admissao_funcionario: document.getElementById('data_admissao').value,
            telefone: document.getElementById('telefone').value,
            email: document.getElementById('email').value,
            whatsapp: document.getElementById('whatsapp').value
        };

        const resposta = await fetch('/api/funcionario', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dados)
        });

        const resultado = await resposta.json();
        alert(resultado.message || 'Erro ao cadastrar funcionário');
        if (resposta.ok) {
            funcionarioForm.reset();
        }
    });
}

function formatarCPF(input) {
    let v = input.value.replace(/\D/g, "");

    v = v.replace(/(\d{3})(\d)/, "$1.$2");
    v = v.replace(/(\d{3})(\d)/, "$1.$2");
    v = v.replace(/(\d{3})(\d{1,2})$/, "$1-$2");

    input.value = v;
}

function formatarTelefone(input) {
  let v = input.value.replace(/\D/g, "");

  v = v.replace(/(\d{2})(\d)/, "($1) $2");
  v = v.replace(/(\d{5})(\d)/, "$1-$2");

  input.value = v;
}