from model.Medico.dao_medico import MedicoDao
from model.Paciente.dao_paciente import PacienteDao

dao_medico = MedicoDao()
dao_paciente = PacienteDao()


class Consultas:
    campos_validacao = ['medico_id', 'paciente_id']

    def __init__(self, medico_id, paciente_id, id=None):
        self.id = id
        self.medico_id = medico_id
        self.paciente_id = paciente_id

    def get_data_dict(self):
        return ({
            'id': id,
            'medico_id': dao_medico.get_by_id(self.medico_id).get_data_dict(),
            'paciente_id': dao_paciente.get_by_id(self.paciente_id).get_data_dict()
        })

    def __str__(self):
        return f'Medico_id: {self.medico_id}, Paciente_id: {self.paciente_id}'
