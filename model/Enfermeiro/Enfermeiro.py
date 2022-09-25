class Enfermeiros:

    campos_validacao = ['nome', 'cpf', 'crm']

    def __int__(self, nome, cpf, crm, id=None):
        self.id = id
        self.nome = nome
        self.cpf = cpf

    def get_dict(self):
        return{
            'id': self.id,
            'nome': self.nome,
            'cpf': self.cpf,
        }

    def __str__(self):
        return f'Nome:{self.nome}, CPF:{self.cpf}'
