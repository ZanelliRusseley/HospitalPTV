from model.Enfermeiro.dao_enfermeiro import EnfermeiroDao
from model.Paciente.dao_paciente import PacienteDao

dao_enfermeiro = EnfermeiroDao()
dao_paciente = PacienteDao()

class Atendimentos:
    campos_Validacao = ['enfermeiro_id', 'paciente_id']

    def __init__(self,enfermeiro_id, paciente_id, id=None):
        self.id = id
        self.enfermeiro_id = enfermeiro_id
        self.paciente_id = paciente_id

    def get_data_dict(self):
        return({
            'id': self.id,
            'Enfermeiro': dao_enfermeiro.get_by_id(self.enfermeiro_id).get_data_dict(),
            'Paciente': dao_paciente.get_by_id(self.paciente_id).get_data_dict()
        })

    def __str__(self):
        return f'Enfermeiro_id: {self.enfermeiro_id}, Paciente_id: {self.paciente_id}'
