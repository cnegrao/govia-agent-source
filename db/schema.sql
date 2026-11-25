CREATE TABLE ouvidoria.manifestacao (
  protocolo TEXT PRIMARY KEY,
  nome_cidadao TEXT NOT NULL,
  cpf TEXT,
  email TEXT,
  canal TEXT NOT NULL,
  texto TEXT NOT NULL,
  categoria TEXT,
  registrada_em TIMESTAMP NOT NULL
);

CREATE TABLE ouvidoria.encaminhamento (
  protocolo TEXT NOT NULL,
  setor TEXT NOT NULL,
  situacao TEXT NOT NULL,
  aprovado_por TEXT,
  encaminhado_em TIMESTAMP
);
