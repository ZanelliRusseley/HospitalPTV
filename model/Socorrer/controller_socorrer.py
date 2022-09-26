from flask import Flask, make_response, jsonify, request, Blueprint

from model.Motorista.dao_motorista import MotoristaDao
from model.Ambulancia.dao_ambulancia import AmbulanciaDao
from model.Socorrer.dao_socorrer import SocorrerDao
from model.Socorrer.Socorrer import Socorros

app_socorrer = Blueprint('socorrer_blueprint', __name__)
app_name = 'socorrer'
dao_socorrer = SocorrerDao()
dao_motorista = MotoristaDao()
dao_ambulancia = AmbulanciaDao()

@app_socorrer.route(f'/{app_name}/', methods=['GET'])
def get_socorros():
    socorros = dao_socorrer.get_all()
    data = [socorrer.get_data_dict() for socorrer in socorros]
    return make_response(jsonify(data))

@app_socorrer.route(f'/{app_name}/add/', methods=['POST'])
def add_socorrer():
    data = request.form.to_dict(flat=True)

    erros = []
    for key in Socorros.campos_Validacao:
        if key not in data.keys():
            erros.append({
                'coluna': key,
                'message': "Este campo é obrigatório"
            })

        if erros:
            return make_response({
                'erros': erros
            }, 400)

    motorista = dao_motorista.get_by_id(data.get('motorista_id'))
    ambulancia = dao_ambulancia.get_by_id(data.get('ambulancia_id'))

    if not motorista:
        return make_response({'Erro': 'Id do motorista não existe!'}, 400)

    if not ambulancia:
        return make_response({'Erro': 'Id da ambulância não existe!'}, 400)

    socorrer = Socorros(**data)
    socorrer = dao_socorrer.salvar(socorrer)
    return make_response({
        'id': socorrer.id,
        'motorista_id': socorrer.motorista_id,
        'ambulancia_id': socorrer.ambulancia_id
    })

@app_socorrer.route(f'/{app_name}/<int:id>', methods=['GET'])
def get_socorrer_by_id(id):
    socorrer = dao_socorrer.get_by_id(id)
    if not socorrer:
        return make_response({'Erro': 'Atendimento não encontrado'}, 404)
    data = socorrer.get_data_dict()
    return make_response(jsonify(data))

@app_socorrer.route(f'/{app_name}/delete/<int:id>', methods=['DELETE'])
def delete_socorrer(id):
    socorrer = dao_socorrer.get_by_id(id)

    if not socorrer:
        return make_response({'Erro': 'Id não existe!'})
    dao_socorrer.delete_Socorrer(id)
    return make_response({'Deletado com sucesso': True})

@app_socorrer.route(f'/{app_name}/update/<int:id>', methods=['PUT'])
def update_socorrer(id):
    data = request.form.to_dict(flat=True)

    erros = []

    for key in Socorros.campos_Validacao:
        if key not in data.keys():
            erros.append({
                'coluna': key,
                'message': "Este campo é obrigatório!"
            })
        if erros:
            return make_response({'Erro': erros}, 400)

        motorista = dao_motorista.get_by_id(data.get('motorista_id'))
        if not motorista:
            return make_response({'Erro': 'Id do Motorista não existe!'}, 400)

        ambulancia = dao_ambulancia.get_by_id(data.get('ambulancia_id'))
        if not ambulancia:
            return make_response({'Erro': 'Id da Ambulância não existe'}, 400)

        oldSocorrer = dao_socorrer.get_by_id(id)
        if not oldSocorrer:
            return make_response({'Erro': 'Este id não existe!'})