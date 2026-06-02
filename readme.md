O código está separado em pastas e em partes que executam uma unica função.

esquema de separação:

controller ⇒ (contém rotas e funções do sql)
modelsy ⇒ (contém as classes que referenciam as tabelas)
static ⇒ (codigo de javascript e css para a pagina web)
templates ⇒ ( contém o index da página)
app.py ⇒(script principal que executa tudo)
database.py ⇒ (possui as configurações de conexão com o sql)
