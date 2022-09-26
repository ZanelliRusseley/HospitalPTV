from flask import Flask, make_response, jsonify, request, Blueprint

from model.Atendimento.dao_atendimento import AtendimentoDao
from model.Atendimento.Atendimento import Atendimentos
from model.Enfermeiro.dao_enfermeiro import EnfermeiroDao
from model.Paciente.dao_paciente import PacienteDao

app_atendimento = Blueprint('atendimento_blueprint', __name__)
app_name = 'atendimento'
dao_atendimento = AtendimentoDao()
dao_enfermeiro = EnfermeiroDao()
dao_paciente = PacienteDao()

@app_atendimento.route(f'/{app_name}/', methods=['GET'])
def get_atendimentos():
    atendimentos = dao_atendimento.get_all()
    data = [atendimento.get_data_dict() for atendimento in atendimentos]
    return make_response(jsonify(data))

@app_atendimento.route(f'/{app_name}/add/', methods=['POST'])
def add_atendimento():
    data = request.form.to_dict(flat=True)

    erros = []
    for key in Atendimentos.campos_Validacao:
        if key not in data.keys():
            erros.append({
                'coluna': key,
                'message': "Este campo é obrigatório"
            })

        if erros:
            return make_response({
                'erros': erros
            }, 400)

    enfermeiro = dao_enfermeiro.get_by_id(data.get('enfermeiro_id'))
    paciente = dao_paciente.get_by_id(data.get('paciente_id'))

    if not enfermeiro:
        return make_response({'Erro': 'Id do Enfermeiro não existe!'}, 400)

    if not paciente:
        return make_response({'Erro': 'Id do Paciente não existe!'}, 400)

    atendimento = Atendimentos(**data)
    atendimento = dao_atendimento.salvar(atendimento)
    return make_response({
        'id': atendimento.id,
        'enfermeiro_id': atendimento.enfermeiro_id,
        'paciente_id': atendimento.paciente_id
    })

@app_atendimento.route(f'/{app_name}/<int:id>', methods=['GET'])
def get_atendimento_by_id(id):
    atendimento = dao_atendimento.get_by_id(id)
    if not atendimento:
        return make_response({'Erro': 'Atendimento não encontrado'}, 404)
    data = atendimento.get_data_dict()
    return make_response(jsonify(data))

@app_atendimento.route(f'/{app_name}/delete/<int:id>', methods=['DELETE'])
def delete_atendimento(id):
    atendimento = dao_atendimento.get_by_id(id)

    if not atendimento:
        return make_response({'Erro': 'Id não existe!'})
    dao_atendimento.delete_Atendimento(id)
    return make_response({'Deletado com sucesso': True})

@app_atendimento.route(f'/{app_name}/update/<int:id>', methods=['PUT'])
def update_consulta(id):
    data = request.form.to_dict(flat=True)
    erros = []

    for key in Atendimentos.campos_Validacao:
        if key not in data.keys():
            erros.append({
                'coluna': key,
                'message': "Este campo é obrigatório!"
            })
        if erros:
            return make_response({'Erro': erros}, 400)

        enfermeiro = dao_enfermeiro.get_by_id(data.get('enfermeiro_id'))
        if not enfermeiro:
            return make_response({'Erro': 'Id do Enfermeiro não existe!'}, 400)

        paciente = dao_paciente.get_by_id(data.get('paciente_id'))
        if not paciente:
            return make_response({'Erro': 'Id do Paciente não existe!'}, 400)

        oldAtendimento = dao_atendimento.get_by_id(id)
        if not oldAtendimento:
            return make_response({'Erro': 'Este id não existe!'})
        newAtendimento = Atendimentos(**data)
        dao_atendimento.update_Atendimento(newAtendimento, oldAtendimento)
        return make_response({'id': oldAtendimento.id})
