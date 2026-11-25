"""Ferramentas da ouvidoria: lógica determinística, sem rede e sem banco.

Cada função recebe e devolve dicionários simples, para que os agentes possam
ser executados e testados localmente. Nenhuma decisão de governança é criada
aqui: classificar uma manifestação não é decidir sobre ela.
"""
from __future__ import annotations

import re

CATEGORIAS = {
    "denuncia": ("denúncia", "denuncia", "irregularidade", "fraude"),
    "reclamacao": ("reclamação", "reclamacao", "demora", "atraso", "não fui atendido"),
    "solicitacao": ("solicito", "solicitação", "solicitacao", "pedido", "gostaria"),
    "elogio": ("elogio", "parabéns", "parabens", "agradeço", "agradeco"),
    "sugestao": ("sugestão", "sugestao", "sugiro", "poderiam"),
}

SETORES = {
    "denuncia": "corregedoria",
    "reclamacao": "atendimento",
    "solicitacao": "atendimento",
    "elogio": "comunicacao",
    "sugestao": "planejamento",
}

_CPF = re.compile(r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b")
_EMAIL = re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b")


def classificar_manifestacao(texto: str) -> dict[str, str]:
    """Classifica o tipo da manifestação por palavras-chave (sem modelo)."""
    normalizado = texto.lower()
    for categoria, termos in CATEGORIAS.items():
        if any(termo in normalizado for termo in termos):
            return {"categoria": categoria, "metodo": "palavras-chave"}
    return {"categoria": "nao_classificada", "metodo": "palavras-chave"}


def mascarar_dados_pessoais(texto: str) -> str:
    """Remove CPF e e-mail do texto antes de qualquer envio a modelo."""
    return _EMAIL.sub("[EMAIL]", _CPF.sub("[CPF]", texto))


def consultar_protocolo(protocolo: str) -> dict[str, str]:
    """Consulta o andamento de um protocolo (representação local, sem rede)."""
    if not re.fullmatch(r"\d{4}-\d{6}", protocolo):
        return {"protocolo": protocolo, "situacao": "invalido"}
    return {"protocolo": protocolo, "situacao": "em_analise"}


def encaminhar_setor(categoria: str) -> dict[str, str]:
    """Indica o setor responsável pela categoria da manifestação."""
    return {"categoria": categoria, "setor": SETORES.get(categoria, "triagem_manual")}


def registrar_resposta(protocolo: str, resposta: str) -> dict[str, str]:
    """Monta o registro de resposta ao cidadão (não grava em banco)."""
    return {"protocolo": protocolo, "resposta": resposta, "situacao": "respondida"}
