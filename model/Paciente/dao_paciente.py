from DataBase.connect import ConexaoBD
from model.Paciente.Paciente import Pacientes

class PacienteDao:
    _TABLE_NAME = 'PACIENTES'

    _INSERT_INTO = f'INSERT INTO {_TABLE_NAME}(nome, cpf)' \
                   'values(%s, %s) RETURNING id'
    _SELECT_ALL = f'SELECT * FROM {_TABLE_NAME}'
    _SELECT_BY_CPF = "SELECT * FROM {} WHERE CPF='{}'"
    _SELECT_BY_ID = 'SELECT * FROM {} WHERE ID={}'
    _DELETE = 'DELETE FROM {} WHERE ID={}'
    _UPDATE = "UPDATE {} SET {}='{}', {}='{}' WHERE ID={}"

    def __init__(self):
        self.DataBase = ConexaoBD().get_instance()

    def salvar(self, paciente):
        if paciente.id is None:
            cursor = self.DataBase.cursor()
            cursor.execute(self._INSERT_INTO, (paciente.nome, paciente.cpf))
            id = cursor.fetchone()[0]
            self.DataBase.commit()
            cursor.close()
            paciente.id = id
            return paciente
        else:
            raise Exception('Erro: Não é possível salvar o paciente')

    def get_all(self):
        pacientes = []
        cursor = self.DataBase.cursor()
        cursor.execute(self._SELECT_ALL)
        all_pacientes = cursor.fetchall()
        columns_name = [desc[0] for desc in cursor.description]
        for paciente_query in all_pacientes:
            data = dict(zip(columns_name, paciente_query))
            paciente = Pacientes(**data)
            pacientes.append(paciente)
        cursor.close()
        return pacientes

    def get_by_cpf(self, cpf):
        cursor = self.DataBase.cursor()
        cursor.execute(self._SELECT_BY_CPF.format(self._TABLE_NAME, cpf))
        columns_name = [desc[0] for desc in cursor.description]
        paciente = cursor.fetchone()
        if not paciente:
            return None
        data = dict(zip(columns_name, paciente))
        paciente = Pacientes(**data)
        cursor.close()
        return paciente

    def get_by_id(self, id):
        cursor = self.DataBase.cursor()
        cursor.execute(self._SELECT_BY_ID.format(self._TABLE_NAME, id))
        columns_name = [desc[0] for desc in cursor.description]
        paciente = cursor.fetchone()
        if not paciente:
            return None
        data = dict(zip(columns_name, paciente))
        paciente = Pacientes(**data)
        cursor.close()
        return paciente

    def delete_Paciente(self, id):
        cursor = self.DataBase.cursor()
        cursor.execute(self._DELETE.format(self._TABLE_NAME, id))
        self.DataBase.commit()
        cursor.close()

    def update_Paciente(self, pacienteNew, pacienteOld):
        cursor = self.DataBase.cursor()
        cursor.execute(self._UPDATE.format(self._TABLE_NAME,
                                           'nome', pacienteNew.nome,
                                           'cpf', pacienteNew.cpf,
                                           pacienteOld.id
                                           ))
        self.DataBase.commit()
        cursor.close()
