const funcionarioForm = document.getElementById('funcionarioForm');
if (funcionarioForm) {
    funcionarioForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const dados = {
            matricula_funcionario: document.getElementById('matricula').value,
            nome_funcionario: document.getElementById('nome').value,
            cpf_funcionario: document.getElementById('cpf').value,
            setor_funcionario: document.getElementById('setor').value,
            funcao_funcionario: document.getElementById('funcao').value,
            data_admissao_funcionario: document.getElementById('data_admissao').value
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

const epiForm = document.getElementById('epiForm');
if (epiForm) {
    epiForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const dados = {
            nome_epi: document.getElementById('nome').value,
            tipo_epi: document.getElementById('tipo').value,
            certificado_aprovacao_epi: document.getElementById('ca').value,
            validade_certificado_aprovacao: document.getElementById('validade_ca').value
        };

        const resposta = await fetch('/api/epi', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dados)
        });

        const resultado = await resposta.json();
        alert(resultado.message || 'Erro ao cadastrar EPI');
        if (resposta.ok) {
            epiForm.reset();
        }
    });
}

const registrosForm = document.getElementById('registrosForm');
if (registrosForm) {
    registrosForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        
        const dados = {
            matricula_funcionario: document.getElementById('matricula').value,
            ca_EPI: document.getElementById('ca').value,
            data_devolucao: document.getElementById('data-devolucao').value,
            data_troca: null,
            motivo_devolucao: null
        };

        const resposta = await fetch('/api/registro', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dados)
        });

        const resultado = await resposta.json();
        alert(resultado.message || 'Erro ao criar Registro');
        if (resposta.ok) {
            registrosForm.reset()
        }
    });
}