class Motoristas:

    campos_validacao = ['nome', 'cpf', 'cnh']

    def __init__(self, nome, cpf, cnh, id=None):
        self.id = id
        self.nome = nome
        self.cpf = cpf
        self.cnh = cnh

    def get_data_dict(self):
        return{
            'id': self.id,
            'Nome': self.nome,
            'CPF': self.cpf,
            'CNH': self.cnh
        }

    def __str__(self):
        return f'Nome:{self.nome}, CPF:{self.cpf}, CNH:{self.cnh}'
