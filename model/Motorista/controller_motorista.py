from flask import Flask, make_response, jsonify, request, Blueprint

from model.Motorista.dao_motorista import MotoristaDao
from model.Motorista.Motorista import Motoristas

app_motorista = Blueprint('motorista_blueprint', __name__)
app_name = 'motoristas'
dao_motorista = MotoristaDao()

@app_motorista.route(f'/{app_name}/', methods=['GET'])
def get_motoristas():
    motoristas = dao_motorista.get_all()
    data = [motorista.get_data_dict() for motorista in motoristas]
    return make_response(jsonify(data))

@app_motorista.route(f'/{app_name}/add/', methods=['POST'])
def add_motorista():
    data = request.form.to_dict(flat=True)

    erros = []
    for key in Motoristas.campos_validacao:
        if key not in data.keys():
            erros.append(
                {
                    'coluna': key,
                    'message': "Este campo é obrigatório"
                }
            )

        if erros:
            return make_response({
                'erros': erros
            }, 400)

        motorista = dao_motorista.get_by_cpf(data.get('cpf'))

        if motorista:
            return make_response('CPF do Motorista já existe', 400)

        motorista = Motoristas(**data)
        motorista = dao_motorista.salvar(motorista)
        return make_response({
            'id': motorista.id,
            'cpf': motorista.cpf,
            'nome': motorista.nome
        })

@app_motorista.route(f'/{app_name}/<int:id>', methods=['GET'])
def get_motorista_by_id(id):
    motorista = dao_motorista.get_by_id(id)
    if not motorista:
        return make_response({'Erro': 'Médico não encontrado'}, 404)
    data = motorista.get_data_dict()
    return make_response(jsonify(data))

@app_motorista.route(f'/{app_name}/delete/<int:id>', methods=['DELETE'])
def delete_motorista(id):
    motorista = dao_motorista.get_by_id(id)

    if not motorista:
        return make_response({'Erro': 'Id não existe!'})
    dao_motorista.delete_Motorista(id)
    return make_response({
        'Deletado com sucesso': True
    })

@app_motorista.route(f'/{app_name}/update/<int:id>', methods=['PUT'])
def update_motorista(id):
    data = request.form.to_dict(flat=True)
    erros = []
    for key in Motoristas.campos_validacao:
        if key not in data.keys():
            erros.append({
                'coluna':key,
                'message': "Este campo é obrigatório!"
            })
        if erros:
            return make_response({
                'erros': erros
            }, 400)
        oldMotorista = dao_motorista.get_by_id(id)
        if not oldMotorista:
            return make_response({'Erro': 'Id não existe!'})
        newMotorista = Motoristas(**data)
        dao_motorista.update_Motorista(newMotorista, oldMotorista)
        return make_response({'id': oldMotorista.id})
