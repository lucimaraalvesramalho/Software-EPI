const form = document.getElementById('funcionarioForm');
        form.addEventListener('submit', async (event) => {
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
                form.reset();
            }
        });