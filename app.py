from flask import Flask

from model.Medico.controller_medico import app_medico

app = Flask(__name__)

app.register_blueprint(app_medico)

app.run()
