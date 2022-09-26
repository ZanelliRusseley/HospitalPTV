from flask import Flask, make_response, jsonify, request, Blueprint

from model.Consulta.dao_consulta import ConsultaDao
from model.Consulta.Consulta import Consultas
from model.Medico.dao_medico import MedicoDao
from model.Paciente.dao_paciente import PacienteDao

app_consulta = Blueprint('consulta_blueprint', __name__)
app_name = 'consulta'
dao_consulta = ConsultaDao()
dao_medico = MedicoDao()
dao_paciente = PacienteDao()

@app_consulta.route(f'/{app_name}/', methods=['GET'])
def get_consultas():
    consultas = dao_consulta.get_all()
    data = [consulta.get_data_dict() for consulta in consultas]
    return make_response(jsonify(data))

@app_consulta.route(f'/{app_name}/add/', methods=['POST'])
def add_consulta():
    data = request.form.to_dict(flat=True)

    erros = []
    for key in Consultas.campos_validacao:
        if key not in data.keys():
            erros.append({
                'coluna': key,
                'message': "Este campo é obrigatório"
            })

        if erros:
            return make_response({
                'erros': erros
            }, 400)

        medico = dao_medico.get_by_id(data.get('medico_id'))
        paciente = dao_paciente.get_by_id(data.get('paciente_id'))

        if not medico:
            return make_response({'Erro': 'Id do Médico não existe!'}, 400)

        if not paciente:
            return make_response({'Erro': 'Id do Paciente não existe!'}, 400)

        consulta = Consultas(**data)
        consulta = dao_consulta.salvar(consulta)
        return make_response({
            'id': consulta.id,
            'medico_id': consulta.medico_id,
            'paciente_id': consulta.paciente_id
        })

@app_consulta.route(f'/{app_name}/<int:id>', methods=['GET'])
def get_consulta_by_id(id):
    consulta = dao_consulta.get_by_id(id)
    if not consulta:
        return make_response({'Erro': 'Consulta não encontrada'}, 404)
    data = consulta.get_data_dict()
    return make_response(jsonify(data))

@app_consulta.route(f'/{app_name}/delete/<int:id>', methods=['DELETE'])
def delete_consulta(id):
    consulta = dao_consulta.get_by_id(id)

    if not consulta:
        return make_response({'Erro': 'Id não existe!'})
    dao_consulta.delete_Consulta(id)
    return make_response({'Deletado com sucesso': True})

@app_consulta.route(f'/{app_name}/update/<int:id>', methods=['PUT'])
def update_consulta(id):
    data = request.form.to_dict(flat=True)
    erros = []

    for key in Consultas.campos_validacao:
        if key not in data.keys():
            erros.append({
                'coluna': key,
                'message': "Este campo é obrigatório!"
            })
        if erros:
            return make_response({'Erro': erros}, 400)

        medico = dao_medico.get_by_id(data.get('medico_id'))
        if not medico:
            return make_response({'Erro': 'Id do Médico não existe!'}, 400)

        paciente = dao_paciente.get_by_id(data.get('paciente_id'))
        if not paciente:
            return make_response({'Erro': 'Id do Paciente não existe!'}, 400)

        oldConsulta = dao_consulta.get_by_id(id)
        if not oldConsulta:
            return make_response({'Erro': 'Este id não existe'})
        newConsulta = Consultas(**data)
        dao_consulta.update_Consulta(newConsulta, oldConsulta)
        return make_response({'id': oldConsulta.id})
