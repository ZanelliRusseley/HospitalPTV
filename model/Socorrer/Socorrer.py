from model.Motorista.dao_motorista import MotoristaDao
from model.Ambulancia.dao_ambulancia import AmbulanciaDao

dao_motorista = MotoristaDao()
dao_ambulancia = AmbulanciaDao()

class Socorros:
    campos_Validacao = ['motorista_id', 'ambulancia_id']

    def __init__(self, motorista_id, ambulancia_id, id=None):
        self.id = id
        self.motorista_id = motorista_id
        self.ambulancia_id = ambulancia_id

    def get_data_dict(self):
        return({
            'id': self.id,
            'Motorista': dao_motorista.get_by_id(self.motorista_id).get_data_dict(),
            'Ambulancia': dao_ambulancia.get_by_id(self.ambulancia_id).get_data_dict()
        })

    def __str__(self):
        return f'Motorista_id: {self.motorista_id}, Ambulancia_id: {self.ambulancia_id}'
