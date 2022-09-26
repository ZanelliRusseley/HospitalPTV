from flask import Flask

from model.Medico.controller_medico import app_medico
from model.Paciente.controller_paciente import app_paciente
from model.Motorista.controller_motorista import app_motorista
from model.Enfermeiro.controller_enfermeiro import app_enfermeiro
from model.Consulta.controller_consulta import app_consulta
from model.Ambulancia.controller_ambulancia import app_ambulancia
from model.Atendimento.controller_atendimento import app_atendimento
from model.Socorrer.controller_socorrer import app_socorrer

app = Flask(__name__)

app.register_blueprint(app_medico)
app.register_blueprint(app_paciente)
app.register_blueprint(app_motorista)
app.register_blueprint(app_enfermeiro)
app.register_blueprint(app_consulta)
app.register_blueprint(app_ambulancia)
app.register_blueprint(app_atendimento)
app.register_blueprint(app_socorrer)

app.run()
