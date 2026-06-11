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

