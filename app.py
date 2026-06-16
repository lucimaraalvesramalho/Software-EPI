from flask import Flask, render_template
from database import get_db_connection

app = Flask(__name__)


def get_dashboard_stats():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT COUNT(*) AS total FROM epi")
        total_epi = cursor.fetchone()['total']

        cursor.execute("SELECT COUNT(*) AS total FROM funcionarios")
        total_funcionarios = cursor.fetchone()['total']

        cursor.execute("SELECT COUNT(*) AS total FROM registros WHERE data_entrega = CURDATE()")
        registros_hoje = cursor.fetchone()['total']

        cursor.execute(
            "SELECT COUNT(*) AS total FROM notificacoes_vencimento WHERE enviado = FALSE AND dias_para_vencimento <= 7"
        )
        vencendo_7_dias = cursor.fetchone()['total']

        return {
            'total_epi': total_epi,
            'total_funcionarios': total_funcionarios,
            'registros_hoje': registros_hoje,
            'vencendo_7_dias': vencendo_7_dias,
        }
    finally:
        cursor.close()
        conn.close()


@app.route('/')
def home():
    dashboard = get_dashboard_stats()
    return render_template('index.html', dashboard=dashboard)


from controller.routes import api_routes
app.register_blueprint(api_routes)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)