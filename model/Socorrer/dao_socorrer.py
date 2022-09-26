from DataBase.connect import ConexaoBD
from model.Socorrer.Socorrer import Socorros

class SocorrerDao:
    _TABLE_NAME = 'SOCORRER'

    _INSERT_INTO = f'INSERT INTO {_TABLE_NAME}(motorista_id, ambulancia_id)' \
                   'values(%s, %s) RETURNING id'
    _SELECT_ALL = f'SELECT * FROM {_TABLE_NAME}'
    _SELECT_BY_ID = 'SELECT * FROM {} WHERE ID={}'
    _DELETE = 'DELETE FROM {} WHERE ID={}'
    _UPDATE = "UPDATE {} SET {}='{}', {}='{}' WHERE ID={}"

    def __init__(self):
        self.DataBase = ConexaoBD().get_instance()

    def salvar(self, socorrer):
        if socorrer.id is None:
            cursor = self.DataBase.cursor()
            cursor.execute(self._INSERT_INTO, (socorrer.motorista_id, socorrer.ambulancia_id))
            id = cursor.fetchone()[0]
            self.DataBase.commit()
            cursor.close()
            socorrer.id = id
            return socorrer
        else:
            raise Exception('Erro: Não é possivel salvar o Socorro')

    def get_all(self):
        socorros = []
        cursor = self.DataBase.cursor()
        cursor.execute(self._SELECT_ALL)
        all_socorros = cursor.fetchall()
        columns_name = [desc[0] for desc in cursor.description]
        for socorrer_query in all_socorros:
            data = dict(zip(columns_name, socorrer_query))
            socorrer = Socorros(**data)
            socorros.append(socorrer)
        cursor.close()
        return socorros

    def get_by_id(self, id):
        cursor = self.DataBase.cursor()
        cursor.execute(self._SELECT_BY_ID.format(self._TABLE_NAME, id))
        columns_name = [desc[0] for desc in cursor.description]
        socorrer = cursor.fetchone()
        if not socorrer:
            return None
        data = dict(zip(columns_name, socorrer))
        socorrer = Socorros(**data)
        cursor.close()
        return socorrer

    def delete_Socorrer(self, id):
        cursor = self.DataBase.cursor()
        cursor.execute(self._DELETE.format(self._TABLE_NAME, id))
        self.DataBase.commit()
        cursor.close()

    def update_Socorrer(self, socorrerNew, socorrerOld):
        cursor = self.DataBase.cursor()
        cursor.execute(self._UPDATE.format(self._TABLE_NAME,
                                           'motorista_id', socorrerNew.motorista_id,
                                           'ambulancia_id', socorrerNew.ambulancia_id,
                                           socorrerOld.id))
        self.DataBase.commit()
        cursor.close()
