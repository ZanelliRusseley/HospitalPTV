from flask import Flask, make_response, jsonify, request, Blueprint

from dao_medico import MedicoDao
from Medico import Medicos

app_medico = Blueprint('medico_blueprint', __name__)
app_name = 'medico'
dao_medico = MedicoDao()

@app_medico.route(f'/{app_name}/', methods=['GET'])
def get_medicos():
    medicos = dao_medico.get_all()
    data = [medico.get_data_dict() for medico in medicos]
    return make_response(jsonify(data))

@app_medico.route(f'/{app_name}/add/', methods=['POST'])
def add_medico():
    data = request.form.to_dict(flat = True)

    erros = []
    for key in Medicos.campos_validacao:
        if key not in data.keys():
            erros.append(
                {
                'coluna':key,
                'message':"Este campo é obrigatório"
                }
            )

        if data.get('cpf') != None:
            for i in data['cpf']:
                if i.isdigit() == False:
                    if i not in '.' or i not in '-':
                        erros.append({'field': 'cpf', 'mensage': 'Este campo só aceita números.'})
                        break

        if erros:
            return make_response({
                'erros': erros
            }, 400)

        medico = dao_medico.get_by_cpf(data.get('cpf'))

        if medico:
            return make_response('CPF do Médico já existe', 400)

        medico = Medicos(**data)
        medico = dao_medico.salvar(medico)
        return make_response({
            'id': medico.id,
            'cpf': medico.cpf,
            'nome': medico.nome
        })

@app_medico.route(f'/{app_name}/<int:id>', methods=['GET'])
def get_medico_by_id(id):
    medico = dao_medico.get_by_id(id)
    if not medico:
        return make_response({'Erro': 'Médico não encontrado'}, 404)
    data = medico.get_dict()
    return make_response(jsonify(data))

@app_medico.route(f'/{app_name}/delete/<int:id>', methods=['DELETE'])
def delete_medico(id):
    medico = dao_medico.get_by_id(id)

    if not medico:
        return make_response({'Erro': 'Id não existe!'})
    dao_medico.delete_Medico(id)
    return make_response({
        'Deletado com sucesso': True
    })

@app_medico.route(f'/{app_name}/update/<int:id>', methods=['PUT'])
def update_medico(id):
    data = request.form.to_dict(flat=True)
    erros = []
    for key in Medicos.campos_validacao:
        if key not in data.keys():
            erros.append({
                'coluna':key,
                'message': "Este campo é obrigatório!"
            })
        if erros:
            return make_response({
                'erros': erros
            }, 400)
        oldMedico = dao_medico.get_by_id(id)
        if not oldMedico:
            return make_response({'Erro': 'Id não existe!'})
        newMedico = Medicos(**data)
        dao_medico.update_Medico(newMedico, oldMedico)
        return make_response({'id': oldMedico.id})

