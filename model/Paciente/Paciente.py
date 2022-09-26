class Pacientes:

    campos_validacao = ['nome', 'cpf']

    def __init__(self, nome, cpf, id=None):
        self.id = id
        self.nome = nome
        self.cpf = cpf

    def get_data_dict(self):
        return{
            'id': self.id,
            'Nome': self.nome,
            'CPF': self.cpf
        }

    def __str__(self):
        return f'Nome:{self.nome}, CPF:{self.cpf}'
