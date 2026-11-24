"""EcoExpert: Sistema especialista baseado em regras para classificação de resíduos domésticos."""

import unicodedata
from typing import Dict, List, Tuple

# Base de conhecimento: 21 resíduos distribuídos em 4 grupos
BASE: Dict[str, List[str]] = {
    "especial": [
        "pilha",
        "bateria",
        "lampada fluorescente",
        "oleo de cozinha",
        "remedio vencido",
        "eletronico",
    ],
    "reciclavel": [
        "papel",
        "papelao",
        "garrafa pet",
        "lata de aluminio",
        "vidro",
        "plastico",
    ],
    "organico": [
        "borra de cafe",
        "casca de fruta",
        "resto de comida",
        "folha seca",
        "casca de ovo",
    ],
    "rejeito": [
        "fralda",
        "papel higienico",
        "absorvente",
        "bituca de cigarro",
    ],
}

# Regras de produção em ordem de prioridade (R1 -> R4; R5 é fallback)
REGRAS: Tuple[Tuple[str, str, str, str], ...] = (
    (
        "R1",
        "especial",
        "Descarte especial",
        "Encaminhe a um ponto de coleta específico ou logística reversa. Não descarte no lixo comum.",
    ),
    (
        "R2",
        "reciclavel",
        "Reciclável",
        "Lave levemente se necessário, seque e encaminhe para a coleta seletiva.",
    ),
    (
        "R3",
        "organico",
        "Orgânico",
        "Destine para compostagem doméstica/comunitária ou coleta de resíduos orgânicos.",
    ),
    (
        "R4",
        "rejeito",
        "Rejeito",
        "Descarte no lixo comum (rejeito), pois não é reciclável nem compostável nas condições habituais.",
    ),
)

ORIENTACAO_DESCONHECIDO = (
    "Resíduo não encontrado na base de conhecimento. "
    "Consulte o serviço de limpeza urbana ou a coleta seletiva do seu município."
)


def normalizar(texto: str) -> str:
    """Normaliza o texto removendo acentos, convertendo para minúsculas e ajustando espaços."""
    sem_acento = "".join(
        c for c in unicodedata.normalize("NFKD", texto) if not unicodedata.combining(c)
    )
    return " ".join(sem_acento.lower().split())


def inferir(entrada: str) -> Tuple[str, str, str]:
    """
    Executa o motor de inferência por correspondência exata e ordem de prioridade.

    Retorna uma tupla (categoria, orientacao, regra_aplicada).
    """
    termo = normalizar(entrada)
    if not termo:
        return ("Não identificado", ORIENTACAO_DESCONHECIDO, "R5")

    for codigo_regra, grupo, categoria, orientacao in REGRAS:
        if termo in BASE[grupo]:
            return (categoria, orientacao, codigo_regra)

    return ("Não identificado", ORIENTACAO_DESCONHECIDO, "R5")


def proximo_estado(estado_atual: str, evento: str) -> str:
    """Função de transição da máquina de estados finita do menu."""
    if estado_atual == "MENU":
        transicoes = {
            "1": "CLASSIFICAR",
            "2": "HISTORICO",
            "3": "FIM",
        }
        return transicoes.get(evento.strip(), "MENU")
    if estado_atual in ("CLASSIFICAR", "HISTORICO"):
        return "MENU"
    return "FIM"


def exibir_menu() -> None:
    """Exibe as opções principais do sistema no terminal."""
    print("\n=== EcoExpert | Sistema Especialista de Resíduos Domésticos ===")
    print("1 - Classificar resíduo")
    print("2 - Ver histórico da sessão")
    print("3 - Sair")


def executar() -> None:
    """Loop principal controlado pela máquina de estados Q = {MENU, CLASSIFICAR, HISTORICO, FIM}."""
    estado = "MENU"
    historico: List[Tuple[str, str, str]] = []

    while estado != "FIM":
        if estado == "MENU":
            exibir_menu()
            opcao = input("Escolha uma opção (1, 2 ou 3): ")
            estado = proximo_estado(estado, opcao)
            if estado == "MENU":
                print("Opção inválida. Por favor, digite 1, 2 ou 3.")

        elif estado == "CLASSIFICAR":
            entrada = input("\nDigite o nome do resíduo doméstico: ")
            categoria, orientacao, regra = inferir(entrada)
            print(f"\nResultado: {categoria} (Regra aplicada: {regra})")
            print(f"Orientação: {orientacao}")
            print("Aviso: Esta é uma recomendação automatizada por regras; confirme conforme a coleta local.")
            historico.append((entrada.strip() or "(vazio)", categoria, regra))
            estado = proximo_estado(estado, "concluida")

        elif estado == "HISTORICO":
            print("\n--- Histórico de Consultas (Sessão Atual) ---")
            if not historico:
                print("Nenhuma consulta realizada nesta sessão.")
            else:
                for idx, (item, categoria, regra) in enumerate(historico, start=1):
                    print(f"{idx}. '{item}' -> {categoria} ({regra})")
            estado = proximo_estado(estado, "concluida")

    print("\nEncerrando o EcoExpert. Obrigado por contribuir com o descarte consciente!")


if __name__ == "__main__":
    executar()
