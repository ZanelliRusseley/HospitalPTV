import psycopg2

class conexaoBD:

    def __int__(self):
        self._conexao = psycopg2.connect(
            host="localhost",
            database="hospitalPTV",
            user="postgres",
            password="Filho4123"
        )

    def get_instance(self):
        return self._conexao