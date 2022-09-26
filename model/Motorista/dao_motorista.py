from DataBase.connect import ConexaoBD
from model.Motorista.Motorista import Motoristas

class MotoristaDao:
    _TABLE_NAME = 'MOTORISTAS'

    _INSERT_INTO = f'INSERT INTO {_TABLE_NAME}(nome, cpf, cnh)' \
                   'values(%s, %s, %s) RETURNING id'
    _SELECT_ALL = f'SELECT * FROM {_TABLE_NAME}'
    _SELECT_BY_CPF = "SELECT * FROM {} WHERE CPF='{}'"
    _SELECT_BY_ID = 'SELECT * FROM {} WHERE ID={}'
    _DELETE = 'DELETE FROM {} WHERE ID={}'
    _UPDATE = "UPDATE {} SET {}='{}', {}='{}', {}='{}' WHERE ID={}"

    def __init__(self):
        self.DataBase = ConexaoBD().get_instance()

    def salvar(self, motorista):
        if motorista.id is None:
            cursor = self.DataBase.cursor()
            cursor.execute(self._INSERT_INTO, (motorista.nome, motorista.cpf, motorista.cnh))
            id = cursor.fetchone()[0]
            self.DataBase.commit()
            cursor.close()
            motorista.id = id
            return motorista
        else:
            raise Exception('Erro: Não é possível salvar o motorista')

    def get_all(self):
        motoristas = []
        cursor = self.DataBase.cursor()
        cursor.execute(self._SELECT_ALL)
        all_motoristas = cursor.fetchall()
        columns_name = [desc[0] for desc in cursor.description]
        for motorista_query in all_motoristas:
            data = dict(zip(columns_name, motorista_query))
            motorista = Motoristas(**data)
            motoristas.append(motorista)
        cursor.close()
        return motoristas

    def get_by_cpf(self, cpf):
        cursor =self.DataBase.cursor()
        cursor.execute(self._SELECT_BY_CPF.format(self._TABLE_NAME, cpf))
        columns_name = [desc[0] for desc in cursor.description]
        motorista = cursor.fetchone()
        if not motorista:
            return None
        data = dict(zip(columns_name, motorista))
        motorista = Motoristas(**data)
        cursor.close()
        return motorista

    def get_by_id(self, id):
        cursor = self.DataBase.cursor()
        cursor.execute(self._SELECT_BY_ID.format(self._TABLE_NAME, id))
        columns_name = [desc[0] for desc in cursor.description]
        motorista = cursor.fetchone()
        if not motorista:
            return None
        data = dict(zip(columns_name, motorista))
        motorista = Motoristas(**data)
        cursor.close()
        return motorista

    def delete_Motorista(self, id):
        cursor = self.DataBase.cursor()
        cursor.execute(self._DELETE.format(self._TABLE_NAME, id))
        self.DataBase.commit()
        cursor.close()

    def update_Motorista(self, motoristaNew, motoristaOld):
        cursor =self.DataBase.cursor()
        cursor.execute(self._UPDATE.format(self._TABLE_NAME,
                                           'nome', motoristaNew.nome,
                                           'cpf', motoristaNew.cpf,
                                           'cnh', motoristaNew.cnh,
                                           motoristaOld.id
                                           ))
        self.DataBase.commit()
        cursor.close()
