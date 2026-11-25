"""Agente de encaminhamento: recebe o caso triado e abre o processo no setor.

A abertura do processo é representada localmente (sem rede). Uma pessoa da
ouvidoria aprova o encaminhamento antes de qualquer resposta ao cidadão.
"""
from __future__ import annotations

from .ferramentas import encaminhar_setor, registrar_resposta

MODEL_PROVIDER = "openai"
MODEL_REFERENCE = "gpt-4.1"
ENCAMINHAMENTO_PROMPT = "Prepare o encaminhamento ao setor responsavel e aguarde aprovacao humana antes de responder."
PROCESSOS_API = {
    "id": "sistema-processos-api",
    "base_url": "https://processos.exemplo.gov.br/api/v1/processos",
}


def abrir_processo(protocolo: str, setor: str) -> dict[str, str]:
    """Representa a chamada à API de processos sem executar I/O de rede."""
    return {
        "api_id": PROCESSOS_API["id"],
        "endpoint": PROCESSOS_API["base_url"],
        "protocolo": protocolo,
        "setor": setor,
    }


class EncaminhamentoAgent:
    kind = "agent"
    model = MODEL_REFERENCE
    instructions = ENCAMINHAMENTO_PROMPT
    tools = [encaminhar_setor, registrar_resposta]

    def encaminhar(self, caso: dict[str, str], aprovado_por_humano: bool) -> dict[str, str]:
        destino = encaminhar_setor(caso["categoria"])
        if not aprovado_por_humano:
            return {"protocolo": caso["protocolo"], "situacao": "aguardando_aprovacao", "setor": destino["setor"]}
        processo = abrir_processo(caso["protocolo"], destino["setor"])
        return {"protocolo": caso["protocolo"], "situacao": "encaminhado", "setor": destino["setor"],
                "processo_api": processo["endpoint"]}
