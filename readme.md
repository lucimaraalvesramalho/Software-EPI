O código está separado em pastas e em partes que executam uma unica função.

esquema de separação:

controller ⇒ (contém rotas e funções do sql)
    ↳ routes.py

modelsy ⇒ (contém as classes que referenciam as tabelas)
    ↳ tables.py

static ⇒ (codigo de javascript e css para a pagina web)
    ↳ script.js
      style.css

templates ⇒ ( contém o index da página)
    ↳ index.html

app.py ⇒(script principal que executa tudo)
database.py ⇒ (possui as configurações de conexão com o sql)