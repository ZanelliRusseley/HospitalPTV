from flask import Flask, make_response, jsonify, request, Blueprint

from model.Ambulancia.dao_ambulancia import AmbulanciaDao
from model.Ambulancia.Ambulancia import Ambulancias

app_ambulancia = Blueprint('ambulancia_blueprint', __name__)
app_name = 'ambulancias'
dao_ambulancia = AmbulanciaDao()

@app_ambulancia.route(f'/{app_name}/', methods=['GET'])
def get_ambulancias():
    ambulancias = dao_ambulancia.get_all()
    data = [ambulancia.get_data_dict() for ambulancia in ambulancias]
    return make_response(jsonify(data))

@app_ambulancia.route(f'/{app_name}/add/', methods=['POST'])
def add_ambulancia():
    data = request.form.to_dict(flat=True)

    erros = []
    for key in Ambulancias.campos_validacao:
        if key not in data.keys():
            erros.append({
                'coluna': key,
                'message': "Este campo é obrigatório"
            })

        if erros:
            return make_response({
                'erros': erros
            }, 400)

    ambulancia = dao_ambulancia.get_by_placa(data.get('placa'))

    if ambulancia:
        return make_response('Placa da Ambulancia já existe!', 400)

    ambulancia = Ambulancias(**data)
    ambulancia = dao_ambulancia.salvar(ambulancia)
    return make_response({
        'id': ambulancia.id,
        'nome': ambulancia.nome,
        'placa': ambulancia.placa
    })

@app_ambulancia.route(f'/{app_name}/<int:id>', methods=['GET'])
def get_ambulancia_by_id(id):
    ambulancia = dao_ambulancia.get_by_id(id)
    if not ambulancia:
        return make_response({'Erro': 'Ambulância não encontrada'}, 404)
    data = ambulancia.get_data_dict()
    return make_response(jsonify(data))

@app_ambulancia.route(f'/{app_name}/delete/<int:id>', methods=['DELETE'])
def delete_ambulancia(id):
    ambulancia = dao_ambulancia.get_by_id(id)

    if not ambulancia:
        return make_response({'Erro': 'Id Não existe!'})
    dao_ambulancia.delete_Ambulancia(id)
    return make_response({'Deletado com sucesso': True})

@app_ambulancia.route(f'/{app_name}/update/<int:id>', methods=['PUT'])
def update_ambulancia(id):
    data = request.form.to_dict(flat=True)
    erros = []

    for key in Ambulancias.campos_validacao:
        if key not in data.keys():
            erros.append({
                'coluna': key,
                'message': 'Este campo é obrigatório!'
            })
        if erros:
            return make_response({
                'erros': erros
            }, 400)

        oldAmbulancia = dao_ambulancia.get_by_id(id)
        if not oldAmbulancia:
            return make_response({'Erro': 'Id não existe!'})
        newAmbulancia = Ambulancias(**data)
        dao_ambulancia.update_Ambulancia(newAmbulancia, oldAmbulancia)
        return make_response({'id': oldAmbulancia.id})
