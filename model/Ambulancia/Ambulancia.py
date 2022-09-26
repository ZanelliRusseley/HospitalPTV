class Ambulancias:

    campos_validacao = ['nome', 'placa']

    def __init__(self, nome, placa, id=None):
        self.id = id
        self.nome = nome
        self.placa = placa

    def get_data_dict(self):
        return {
            'id': self.id,
            'Nome': self.nome,
            'Placa': self.placa
        }

    def __str__(self):
        return f'Nome:{self.nome}, Placa:{self.placa}'
