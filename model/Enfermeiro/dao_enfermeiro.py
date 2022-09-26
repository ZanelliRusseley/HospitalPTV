from DataBase.connect import ConexaoBD
from model.Enfermeiro.Enfermeiro import Enfermeiros

class EnfermeiroDao:
    _TABLE_NAME = 'ENFERMEIROS'

    _INSERT_INTO = f'INSERT INTO {_TABLE_NAME}(nome, cpf)' \
                   'values(%s, %s) RETURNING id'
    _SELECT_ALL = f'SELECT * FROM {_TABLE_NAME}'
    _SELECT_BY_CPF = "SELECT * FROM {} WHERE CPF='{}'"
    _SELECT_BY_ID = 'SELECT * FROM {} WHERE ID={}'
    _DELETE = 'DELETE FROM {} WHERE ID={}'
    _UPDATE = "UPDATE {} SET {}='{}', {}='{}' WHERE ID={}"

    def __init__(self):
        self.DataBase = ConexaoBD().get_instance()

    def salvar(self, enfermeiro):
        if enfermeiro.id is None:
            cursor = self.DataBase.cursor()
            cursor.execute(self._INSERT_INTO, (enfermeiro.nome, enfermeiro.cpf))
            id = cursor.fetchone()[0]
            self.DataBase.commit()
            cursor.close()
            enfermeiro.id = id
            return enfermeiro
        else:
            raise Exception('Erro: Não é possível salvar o enfermeiro')

    def get_all(self):
        enfermeiros = []
        cursor = self.DataBase.cursor()
        cursor.execute(self._SELECT_ALL)
        all_enfermeiros = cursor.fetchall()
        columns_name = [desc[0] for desc in cursor.description]
        for enfermeiro_query in all_enfermeiros:
            data = dict(zip(columns_name, enfermeiro_query))
            enfermeiro = Enfermeiros(**data)
            enfermeiros.append(enfermeiro)
        cursor.close()
        return enfermeiros

    def get_by_cpf(self, cpf):
        cursor = self.DataBase.cursor()
        cursor.execute(self._SELECT_BY_CPF.format(self._TABLE_NAME, cpf))
        columns_name = [desc[0] for desc in cursor.description]
        enfermeiro = cursor.fetchone()
        if not enfermeiro:
            return None
        data = dict(zip(columns_name, enfermeiro))
        enfermeiro = Enfermeiros(**data)
        cursor.close()
        return enfermeiro

    def get_by_id(self, id):
        cursor = self.DataBase.cursor()
        cursor.execute(self._SELECT_BY_ID.format(self._TABLE_NAME, id))
        columns_name = [desc[0] for desc in cursor.description]
        enfermeiro = cursor.fetchone()
        if not enfermeiro:
            return None
        data = dict(zip(columns_name, enfermeiro))
        enfermeiro = Enfermeiros(**data)
        cursor.close()
        return enfermeiro

    def delete_Enfermeiro(self, id):
        cursor = self.DataBase.cursor()
        cursor.execute(self._DELETE.format(self._TABLE_NAME, id))
        self.DataBase.commit()
        cursor.close()

    def update_Enfermeiro(self, enfermeiroNew, enfermeiroOld):
        cursor = self.DataBase.cursor()
        cursor.execute(self._UPDATE.format(self._TABLE_NAME,
                                           'nome', enfermeiroNew.nome,
                                           'cpf', enfermeiroNew.cpf,
                                           enfermeiroOld.id
                                           ))
        self.DataBase.commit()
        cursor.close()
