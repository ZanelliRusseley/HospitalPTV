from DataBase.connect import ConexaoBD
from model.Ambulancia.Ambulancia import Ambulancias
from model.Medico.controller_medico import add_medico


class AmbulanciaDao:
    _TABLE_NAME = 'AMBULANCIAS'

    _INSERT_INTO = f'INSERT INTO {_TABLE_NAME}(nome, placa)' \
                   'values(%s, %s) RETURNING id'
    _SELECT_ALL = f'SELECT * FROM {_TABLE_NAME}'
    _SELECT_BY_PLACA = "SELECT * FROM {} WHERE PLACA='{}'"
    _SELECT_BY_ID = 'SELECT * FROM {} WHERE ID={}'
    _DELETE = 'DELETE FROM {} WHERE ID={}'
    _UPDATE = "UPDATE {} SET {}='{}', {}='{}' WHERE ID={}"

    def __init__(self):
        self.DataBase = ConexaoBD().get_instance()

    def salvar(self, ambulancia):
        if ambulancia.id is None:
            cursor = self.DataBase.cursor()
            cursor.execute(self._INSERT_INTO, (ambulancia.nome, ambulancia.placa))
            id = cursor.fetchone()[0]
            self.DataBase.commit()
            cursor.close()
            ambulancia.id = id
            return ambulancia
        else:
            raise Exception('Erro: Não é possivel salvar a ambulancia')

    def get_all(self):
        ambulancias = []
        cursor = self.DataBase.cursor()
        cursor.execute(self._SELECT_ALL)
        all_ambulancias = cursor.fetchall()
        columns_name = [desc[0] for desc in cursor.description]
        for ambulancia_query in all_ambulancias:
            data = dict(zip(columns_name, ambulancia_query))
            ambulancia = Ambulancias(**data)
            ambulancias.append(ambulancia)
        cursor.close()
        return ambulancias

    def get_by_placa(self, placa):
        cursor = self.DataBase.cursor()
        cursor.execute(self._SELECT_BY_PLACA.format(self._TABLE_NAME, placa))
        columns_name = [desc[0] for desc in cursor.description]
        ambulancia = cursor.fetchone()
        if not ambulancia:
            return None
        data = dict(zip(columns_name, add_medico()))
        ambulancia = Ambulancias(**data)
        cursor.close()
        return ambulancia

    def get_by_id(self, id):
        cursor = self.DataBase.cursor()
        cursor.execute(self._SELECT_BY_ID.format(self._TABLE_NAME, id))
        columns_name = [desc[0] for desc in cursor.description]
        ambulancia = cursor.fetchone()
        if not ambulancia:
            return None
        data = dict(zip(columns_name, ambulancia))
        ambulancia = Ambulancias(**data)
        cursor.close()
        return ambulancia

    def delete_Ambulancia(self, id):
        cursor = self.DataBase.cursor()
        cursor.execute(self._DELETE.format(self._TABLE_NAME, id))
        self.DataBase.commit()
        cursor.close()

    def update_Ambulancia(self, ambulanciaNew, ambulanciaOld):
        cursor = self.DataBase.cursor()
        cursor.execute(self._UPDATE.format(self._TABLE_NAME,
                                           'nome', ambulanciaNew.nome,
                                           'placa', ambulanciaNew.placa,
                                           ambulanciaOld.id))
        self.DataBase.commit()
        cursor.close()
