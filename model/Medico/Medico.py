class Medicos:

    campos_validacao = ['nome', 'cpf', 'crm']

    def __init__(self, nome, cpf, crm, id=None):
        self.id = id
        self.nome = nome
        self.cpf = cpf
        self.crm = crm

    def get_data_dict(self):
        return{
            'id': self.id,
            'nome': self.nome,
            'cpf': self.cpf,
            'crm': self.crm
        }

    def __str__(self):
        return f'Nome:{self.nome}, CPF:{self.cpf}, CRM:{self.crm}'
