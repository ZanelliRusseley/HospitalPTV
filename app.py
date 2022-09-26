from flask import Flask

from model.Medico.controller_medico import app_medico
from model.Paciente.controller_paciente import app_paciente
from model.Motorista.controller_motorista import app_motorista
from model.Enfermeiro.controller_enfermeiro import app_enfermeiro
from model.Consulta.controller_consulta import app_consulta

app = Flask(__name__)

app.register_blueprint(app_medico)
app.register_blueprint(app_paciente)
app.register_blueprint(app_motorista)
app.register_blueprint(app_enfermeiro)
app.register_blueprint(app_consulta)

app.run()
