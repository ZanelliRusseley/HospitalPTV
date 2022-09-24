CREATE TABLE if not exists ambulancias (
	id SERIAL PRIMARY KEY,
	nome Varchar(60) not NULL,
	placa Varchar(60) not NULL UNIQUE,
	disponivel BOOLEAN
);

CREATE TABLE if not exists motoristas (
	id SERIAL PRIMARY KEY,
	nome Varchar(60) not null,
	CPF VARCHAR(60) not null unique,
	CNH VARCHAR(60) not null unique,
	disponivel Boolean
);

CREATE TABLE if not exists medicos(
	id SERIAL PRIMARY KEY,
	CPF VARCHAR(60) not null unique,
	CRM VARCHAR(60) not null unique,
	disponivel Boolean
);

CREATE TABLE if not exists enfermeiros(
	id SERIAL PRIMARY KEY,
	CPF VARCHAR(60) not null unique,
	disponivel Boolean
);

CREATE TABLE if not exists pacientes(
	id SERIAL PRIMARY KEY,
	CPF VARCHAR(60) not null unique
);

CREATE TABLE if not exists consulta(
	id SERIAL PRIMARY KEY,
	medico_id INTEGER REFERENCES medicos(id),
	paciente_id INTEGER REFERENCES pacientes(id)
);

CREATE TABLE if not exists antendimento(
	id SERIAL PRIMARY KEY,
	enfermeiro_id INTEGER REFERENCES enfermeiros(id),
	paciente_id INTEGER REFERENCES pacientes(id)
);

CREATE TABLE if not exists socorrer(
	id SERIAL PRIMARY KEY,
	motorista_id INTEGER REFERENCES motoristas(id),
	ambulancia_id INTEGER REFERENCES ambulancias(id)
);