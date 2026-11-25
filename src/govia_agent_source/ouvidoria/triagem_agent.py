"""Agente de triagem de manifestações da ouvidoria.

Recebe o texto do cidadão, mascara dados pessoais, classifica a manifestação e
consulta o protocolo. Não decide nem responde ao cidadão: só prepara o caso
para o agente de encaminhamento e para a revisão humana.
"""
from __future__ import annotations

from .ferramentas import classificar_manifestacao, consultar_protocolo, mascarar_dados_pessoais

MODEL_PROVIDER = "openai"
MODEL_REFERENCE = "gpt-4.1-mini"
TRIAGEM_PROMPT = "Classifique a manifestacao do cidadao sem expor CPF ou e-mail e sem decidir o merito."


class TriagemManifestacaoAgent:
    kind = "agent"
    model = MODEL_REFERENCE
    instructions = TRIAGEM_PROMPT
    knowledge_base = "manual-atendimento-cidadao"
    tools = [mascarar_dados_pessoais, classificar_manifestacao, consultar_protocolo]

    def triar(self, protocolo: str, texto: str) -> dict[str, str]:
        texto_seguro = mascarar_dados_pessoais(texto)
        classificacao = classificar_manifestacao(texto_seguro)
        andamento = consultar_protocolo(protocolo)
        return {
            "protocolo": protocolo,
            "texto": texto_seguro,
            "categoria": classificacao["categoria"],
            "situacao": andamento["situacao"],
            "proximo_passo": "encaminhamento",
        }
