from flask import Flask, make_response, jsonify, request, Blueprint

from model.Paciente.dao_paciente import PacienteDao
from model.Paciente.Paciente import Pacientes

app_paciente = Blueprint('paciente_blueprint', __name__)
app_name = 'pacientes'
dao_paciente = PacienteDao()

@app_paciente.route(f'/{app_name}/', methods=['GET'])
def get_pacientes():
    pacientes = dao_paciente.get_all()
    data = [paciente.get_data_dict() for paciente in pacientes]
    return make_response(jsonify(data))

@app_paciente.route(f'/{app_name}/add/', methods=['POST'])
def add_paciente():
    data = request.form.to_dict(flat=True)

    erros = []
    for key in Pacientes.campos_validacao:
        if key not in data.keys():
            erros.append({
                'coluna': key,
                'message': "Este campo é obrigatório"
            })

        if erros:
            return make_response({
                'erros': erros
            }, 400)

    paciente = dao_paciente.get_by_cpf(data.get('cpf'))

    if paciente:
        return make_response('CPF do Paciente já existe!', 400)

    paciente = Pacientes(**data)
    paciente = dao_paciente.salvar(paciente)
    return make_response({
        'id': paciente.id,
        'cpf': paciente.cpf,
        'nome': paciente.nome
    })

@app_paciente.route(f'/{app_name}/<int:id>', methods=['GET'])
def get_paciente_by_id(id):
    paciente = dao_paciente.get_by_cpf(id)
    if not paciente:
        return make_response({'erro': 'Paciente não encontrado'}, 404)
    data = paciente.get_data_dict()
    return make_response(jsonify(data))

@app_paciente.route(f'/{app_name}/delete/<int:id>', methods=['DELETE'])
def delete_paciente(id):
    paciente = dao_paciente.get_by_id(id)

    if not paciente:
        return make_response({'Erro': 'Id não existe!'})
    dao_paciente.delete_Paciente(id)
    return make_response({
        'Deletado com sucesso': True
    })

@app_paciente.route(f'/{app_name}/update/<int:id>', methods=['PUT'])
def update_paciente(id):
    data = request.form.to_dict(flat=True)
    erros = []
    for key in Pacientes.campos_validacao:
        if key not in data.keys():
            erros.append({
                'coluna': key,
                'message': "Este campo é obrigatório!"
            })
        if erros:
            return make_response({
                'erros': erros
            }, 400)
        oldPaciente = dao_paciente.get_by_id(id)
        if not oldPaciente:
            return make_response({'Erro': 'Id não existe!'})
        newPaciente = Pacientes(**data)
        dao_paciente.update_Paciente(newPaciente, oldPaciente)
        return make_response({'id': oldPaciente.id})
