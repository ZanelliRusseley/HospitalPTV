from DataBase.connect import ConexaoBD
from model.Atendimento.Atendimento import Atendimentos


class AtendimentoDao:
    _TABLE_NAME = 'ATENDIMENTO'

    _INSERT_INTO = f'INSERT INTO {_TABLE_NAME}(enfermeiro_id, paciente_id)' \
                   'values(%s, %s) RETURNING id'
    _SELECT_ALL = f'SELECT * FROM {_TABLE_NAME}'
    _SELECT_BY_ID = 'SELECT * FROM {} WHERE ID={}'
    _DELETE = 'DELETE FROM {} WHERE ID={}'
    _UPDATE = "UPDATE {} SET {}='{}', {}='{}' WHERE ID={}"

    def __init__(self):
        self.DataBase = ConexaoBD().get_instance()

    def salvar(self, atendimento):
        if atendimento.id is None:
            cursor = self.DataBase.cursor()
            cursor.execute(self._INSERT_INTO, (atendimento.enfermeiro_id, atendimento.paciente_id))
            id = cursor.fetchone()[0]
            self.DataBase.commit()
            cursor.close()
            atendimento.id = id
            return atendimento
        else:
            raise Exception('Erro: Não é possivel salvar a consulta')

    def get_all(self):
        atendimentos = []
        cursor = self.DataBase.cursor()
        cursor.execute(self._SELECT_ALL)
        all_atendimentos = cursor.fetchall()
        columns_name = [desc[0] for desc in cursor.description]
        for antendimento_query in all_atendimentos:
            data = dict(zip(columns_name, antendimento_query))
            atendimento = Atendimentos(**data)
            atendimentos.append(atendimento)
        cursor.close()
        return atendimentos

    def get_by_id(self, id):
        cursor = self.DataBase.cursor()
        cursor.execute(self._SELECT_BY_ID.format(self._TABLE_NAME, id))
        columns_name = [desc[0] for desc in cursor.description]
        atendimento = cursor.fetchone()
        if not atendimento:
            return None
        data = dict(zip(columns_name, atendimento))
        atendimento = Atendimentos(**data)
        cursor.close()
        return atendimento

    def delete_Atendimento(self, id):
        cursor = self.DataBase.cursor()
        cursor.execute(self._DELETE.format(self._TABLE_NAME, id))
        self.DataBase.commit()
        cursor.close()

    def update_Atendimento(self, atendimentoNew, atendimentoOld):
        cursor = self.DataBase.cursor()
        cursor.execute(self._UPDATE.format(self._TABLE_NAME,
                                           'enfermeiro_id', atendimentoNew.enfermeiro_id,
                                           'paciente_id', atendimentoNew.paciente_id,
                                           atendimentoOld.id))
        self.DataBase.commit()
        cursor.close()
