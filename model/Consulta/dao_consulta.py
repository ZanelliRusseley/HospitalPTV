from DataBase.connect import ConexaoBD
from model.Consulta.Consulta import Consultas


class ConsultaDao:
    _TABLE_NAME = 'CONSULTA'

    _INSERT_INTO = f'INSERT INTO {_TABLE_NAME}(medico_id, paciente_id)' \
                   'values(%s, %s) RETURNING id'
    _SELECT_ALL = f'SELECT * FROM {_TABLE_NAME}'
    _SELECT_BY_ID = 'SELECT * FROM {} WHERE ID={}'
    _DELETE = 'DELETE FROM {} WHERE ID={}'
    _UPDATE = "UPDATE {} SET {}='{}', {}='{}' WHERE ID={}"

    def __init__(self):
        self.DataBase = ConexaoBD().get_instance()

    def salvar(self, consulta):
        if consulta.id is None:
            cursor = self.DataBase.cursor()
            cursor.execute(self._INSERT_INTO, (consulta.medico_id, consulta.paciente_id))
            id = cursor.fetchone()[0]
            self.DataBase.commit()
            cursor.close()
            consulta.id = id
            return consulta
        else:
            raise Exception('Erro: Não é possivel salvar a consulta')

    def get_all(self):
        consultas = []
        cursor = self.DataBase.cursor()
        cursor.execute(self._SELECT_ALL)
        all_consultas = cursor.fetchall()
        columns_name = [desc[0] for desc in cursor.description]
        for consulta_query in all_consultas:
            data = dict(zip(columns_name, consulta_query))
            consulta = Consultas(**data)
            consultas.append(consulta)
        cursor.close()
        return consultas

    def get_by_id(self, id):
        cursor = self.DataBase.cursor()
        cursor.execute(self._SELECT_BY_ID.format(self._TABLE_NAME, id))
        columns_name = [desc[0] for desc in cursor.description]
        consulta = cursor.fetchone()
        if not consulta:
            return None
        data = dict(zip(columns_name, consulta))
        consulta = Consultas(**data)
        cursor.close()
        return consulta

    def delete_Consulta(self, id):
        cursor = self.DataBase.cursor()
        cursor.execute(self._DELETE.format(self._TABLE_NAME, id))
        self.DataBase.commit()
        cursor.close()

    def update_Consulta(self, consultaNew, consultaOld):
        cursor = self.DataBase.cursor()
        cursor.execute(self._UPDATE.format(self._TABLE_NAME,
                                           'medico_id', consultaNew.medico_id,
                                           'paciente_id', consultaNew.paciente_id,
                                           consultaOld.id
                                           ))
        self.DataBase.commit()
        cursor.close()
