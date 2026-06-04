# Software-EPI

Aplicativo web simples para cadastro de funcionários e gerenciamento de EPIs.

## Visão geral

- `app.py`: ponto de entrada do Flask.
- `database.py`: configuração da conexão com o banco de dados.
- `controller/routes.py`: rotas e lógica de CRUD.
- `models/tables.py`: definição das tabelas do banco.
- `static/`: arquivos estáticos (CSS e JavaScript).
- `templates/`: páginas HTML renderizadas pelo Flask.

## Estrutura do projeto

```
controller/        # rotas e funções do SQL
├── routes.py

models/            # classes que representam tabelas
├── tables.py

static/            # JS e CSS da página
├── script.js
├── style.css

templates/         # HTML principal e layouts
├── base.html
├── index.html
├── cadastrar-funcionario.html
├── cadastrar-epi.html
├── criar-registro.html
├── atualizar-cadastros.html
├── atualizar-registros.html
├── components/
│   └── header.html

app.py             # script principal
database.py        # configuração da conexão SQL
```

## Requisitos

- Python 3.10+ (ou compatível)
- Flask
- SQLAlchemy ou outra biblioteca usada no `database.py`

## Instalação

1. Crie e ative um ambiente virtual:

```bash
python -m venv venv
venv\Scripts\activate
```

2. Instale as dependências:

```bash
pip install flask
```

> Se o projeto usar SQLAlchemy, instale também:
> ```bash
> pip install sqlalchemy
> ```

## Execução

```bash
python app.py
```

Então acesse `http://127.0.0.1:5000` no navegador.

## Observações

- O formulário de cadastro de funcionário usa JavaScript para enviar os dados via `fetch`.
- Se o JS não carregar, confirme se o caminho do script em `templates/base.html` está correto.
- Ajuste as rotas e a configuração do banco conforme necessário.

