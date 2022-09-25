from DataBase.connect import ConexaoBD
from Medico import Medicos


class MedicoDao:
    _TABLE_NAME = 'MEDICO'

    _INSERT_INTO = f'INSERT INTO {_TABLE_NAME}(nome, cpf, crm)' \
                   'values(%s, %s, %s) RETURNING id'
    _SELECT_ALL = f'SELECT * FROM {_TABLE_NAME}'
    _SELECT_BY_CPF = "SELECT * FROM {} WHERE CPF='{}'"
    _SELECT_BY_ID = 'SELECT * FROM {} WHERE ID={}'
    _DELETE = 'DELETE FROM {} WHERE ID={}'
    _UPDATE = "UPDATE {} SET {}='{}', {}='{}', {}='{}' WHERE ID={}"

    def __init__(self):
        self.DataBase = ConexaoBD.get_instance()

    def salvar(self, medico):
        if medico.id is None:
            cursor = self.DataBase.cursor()
            cursor.execute(self._INSERT_INTO, (medico.nome, medico.cpf, medico.crm))
            id = cursor.fetchone()[0]
            self.DataBase.commit()
            cursor.close()
            medico.id = id
            return medico
        else:
            raise Exception('Erro: Não é possível salvar o médico')

    def get_all(self):
        medicos = []
        cursor = self.DataBase.cursor()
        cursor.execute(self._SELECT_ALL)
        all_medicos = cursor.fetchall()
        columns_name = [desc[0] for desc in cursor.description]
        for medico_query in all_medicos:
            data = dict(zip(columns_name, medico_query))
            medico = Medicos(**data)
            medicos.append(medico)
        cursor.close()
        return medicos

    def get_by_cpf(self, cpf):
        cursor = self.DataBase.cursor()
        cursor.execute(self._SELECT_BY_CPF.format(self._TABLE_NAME, cpf))
        columns_name = [desc[0] for desc in cursor.description]
        medico = cursor.fetchone()
        if not medico:
            return None
        data = dict(zip(columns_name, medico))
        medico = Medicos(**data)
        cursor.close()
        return medico

    def get_by_id(self, id):
        cursor = self.DataBase.cursor()
        cursor.execute(self._SELECT_BY_ID.format(self._TABLE_NAME, id))
        columns_name = [desc[0] for desc in cursor.description]
        medico = cursor.fetchone()
        if not medico:
            return None
        data = dict(zip(columns_name, medico))
        medico = Medicos(**data)
        cursor.close()
        return medico

    def delete_Medico(self, id):
        cursor = self.DataBase.cursor()
        cursor.execute(self._DELETE.format(self._TABLE_NAME, id))
        self.DataBase.commit()
        cursor.close()

    def update_Medico(self, medicoNew, medicoOld):
        cursor = self.DataBase.cursor()
        cursor.execute(self._UPDATE.format(self._TABLE_NAME,
                                           'nome', medicoNew.nome,
                                           'cpf', medicoNew.cpf,
                                           'crm', medicoNew.crm,
                                           medicoOld.id
                                           ))
        self.DataBase.commit()
        cursor.close()
