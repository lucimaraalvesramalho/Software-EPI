from flask import Flask, render_template
from database import get_db_connection

app = Flask(__name__)

# Rota principal que retorna a página HTML de cadastro
@app.route('/')
def home():
    return render_template('index.html')


# Registra o blueprint de rotas após a criação do app e da função de conexão
from controller.routes import api_routes
app.register_blueprint(api_routes)


if __name__ == '__main__':
    app.run(debug=True)