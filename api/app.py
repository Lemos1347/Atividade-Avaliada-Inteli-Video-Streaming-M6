from sanic import Sanic

from video.routes import video

# Função que criará o servidor
def create_server() -> Sanic:
    app = Sanic(__name__)
    app.config.CORS_ORIGINS = "*"
    return app


app = create_server()

# Importando as rotas e estabelecendo um prefixo
app.blueprint(video, url_prefix='/video')

# Ponte de entrada da aplicação
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3001)
