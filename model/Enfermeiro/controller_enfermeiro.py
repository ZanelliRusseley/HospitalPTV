from flask import Flask, make_response, jsonify, request, Blueprint

from model.Enfermeiro.dao_enfermeiro import EnfermeiroDao
from model.Enfermeiro.Enfermeiro import Enfermeiros

app_enfermeiro = Blueprint('enfermeiro_blueprint', __name__)
app_name = 'enfermeiros'
dao_enfermeiro = EnfermeiroDao()

@app_enfermeiro.route(f'/{app_name}/', methods=['GET'])
def get_enfermeiros():
    enfermeiros = dao_enfermeiro.get_all()
    data = [enfermeiro.get_data_dict() for enfermeiro in enfermeiros]
    return make_response(jsonify(data))

@app_enfermeiro.route(f'/{app_name}/add/', methods=['POST'])
def add_enfermeiro():
    data = request.form.to_dict(flat=True)

    erros = []
    for key in Enfermeiros.campos_validacao:
        if key not in data.keys():
            erros.append(
                {
                'coluna':key,
                'message':"Este campo é obrigatório"
                }
            )

        if erros:
            return make_response({
                'erros': erros
            }, 400)

        enfermeiro = dao_enfermeiro.get_by_cpf(data.get('cpf'))

        if enfermeiro:
            return make_response('CPF do Enfermeiro já existe', 400)

        enfermeiro = Enfermeiros(**data)
        enfermeiro = dao_enfermeiro.salvar(enfermeiro)
        return make_response({
            'id': enfermeiro.id,
            'cpf': enfermeiro.cpf,
            'nome': enfermeiro.nome
        })

@app_enfermeiro.route(f'/{app_name}/<int:id>', methods=['GET'])
def get_enfermeiro_by_id(id):
    enfermeiro = dao_enfermeiro.get_by_id(id)
    if not enfermeiro:
        return make_response({'Erro': 'Enfermeiro não encontrado'}, 404)
    data = enfermeiro.get_data_dict()
    return make_response(jsonify(data))

@app_enfermeiro.route(f'/{app_name}/delete/<int:id>', methods=['DELETE'])
def delete_enfermeiro(id):
    enfermeiro = dao_enfermeiro.get_by_id(id)

    if not enfermeiro:
        return make_response({'Erro': 'Id não existe!'})
    dao_enfermeiro.delete_Enfermeiro(id)
    return make_response({'Deletado com sucesso': True})

@app_enfermeiro.route(f'/{app_name}/update/<int:id>', methods=['PUT'])
def update_enfermeiro(id):
    data = request.form.to_dict(flat=True)
    erros= []

    for key in Enfermeiros.campos_validacao:
        if key not in data.keys():
            erros.append({
                'coluna':key,
                'message': "Este campo é obrigatório!"
            })
        if erros:
            return make_response({
                'erros': erros
            }, 400)
        oldEnfermeiro = dao_enfermeiro.get_by_id(id)
        if not oldEnfermeiro:
            return make_response({'Erro': 'Id não existe!'})
        newEnfermeiro = Enfermeiros(**data)
        dao_enfermeiro.update_Enfermeiro(newEnfermeiro, oldEnfermeiro)
        return make_response({'id': oldEnfermeiro.id})
