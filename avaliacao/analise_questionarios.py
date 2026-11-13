"""
Análise dos questionários da Oficina de Letramento Digital e Programação Básica com Python.

Compara as respostas do questionário diagnóstico (antes) com as do questionário final
(depois), gera gráficos e um resumo em Markdown para o relatório.

Uso:
    python analise_questionarios.py --pre dados/diagnostico.csv --pos dados/final.csv --saida resultados

Os CSVs podem ser exportados do Google Forms (Respostas → Planilhas → Arquivo → Fazer download → CSV).
Se os títulos das colunas do Forms forem as próprias perguntas, ajuste o dicionário
RENOMEAR abaixo para converter cada pergunta no nome curto da coluna.

Para testar com dados fictícios:
    python analise_questionarios.py --pre exemplo_ficticio/diagnostico.csv \
        --pos exemplo_ficticio/final.csv --saida resultados_exemplo
"""
import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

COMPETENCIAS = {
    "auto_computador": "Uso do computador",
    "auto_seguranca": "Segurança na internet",
    "auto_logica": "Lógica / algoritmos",
    "auto_python": "Programação em Python",
    "auto_dados": "Organização de dados",
}

# Exemplo: "Código do participante": "id"
RENOMEAR = {
    "Código do participante": "id",
}


def carregar(caminho):
    df = pd.read_csv(caminho).rename(columns=RENOMEAR)
    df["id"] = df["id"].astype(str).str.strip().str.upper()
    return df.drop_duplicates(subset="id", keep="last")


def sim_nao(serie):
    return serie.astype(str).str.strip().str.lower().isin(["sim", "s", "yes", "1", "true"])


def analisar(pre, pos, saida):
    saida.mkdir(parents=True, exist_ok=True)
    pareado = pre.merge(pos, on="id", suffixes=("_pre", "_pos"))
    n_pre, n_pos, n_par = len(pre), len(pos), len(pareado)

    # ---------- Autoavaliação: média antes x depois
    linhas = []
    for col, nome in COMPETENCIAS.items():
        antes = pareado[f"{col}_pre"].mean()
        depois = pareado[f"{col}_pos"].mean()
        linhas.append({"Competência": nome, "Antes": round(antes, 2),
                       "Depois": round(depois, 2), "Variação": round(depois - antes, 2)})
    tab_auto = pd.DataFrame(linhas)

    # ---------- Quiz de conhecimentos
    quiz_antes = pareado["quiz_acertos_pre"].mean()
    quiz_depois = pareado["quiz_acertos_pos"].mean()
    melhoraram = (pareado["quiz_acertos_pos"] > pareado["quiz_acertos_pre"]).mean() * 100

    # ---------- Avaliação da oficina
    aval = {}
    if "satisfacao" in pos:
        aval["Satisfação média (1 a 5)"] = f"{pos['satisfacao'].mean():.2f}"
    for col, rotulo in [("recomendaria", "Recomendariam a oficina"),
                        ("interesse_stem", "Relataram mais interesse por STEM"),
                        ("problema_conexao", "Tiveram problemas de conexão/equipamento")]:
        if col in pos:
            aval[rotulo] = f"{sim_nao(pos[col]).mean() * 100:.0f}%"
    if "encontros_presentes" in pos:
        aval["Presença média (encontros de 4)"] = f"{pos['encontros_presentes'].mean():.1f}"

    # ---------- Gráfico 1: autoavaliação
    fig, ax = plt.subplots(figsize=(8, 4.2))
    y = range(len(tab_auto))
    ax.barh([i + 0.2 for i in y], tab_auto["Antes"], height=0.4, color="#9DB7D5", label="Antes")
    ax.barh([i - 0.2 for i in y], tab_auto["Depois"], height=0.4, color="#1F4E8C", label="Depois")
    ax.set_yticks(list(y), tab_auto["Competência"])
    ax.set_xlim(0, 5)
    ax.set_xlabel("Autoavaliação média (1 a 5)")
    ax.set_title(f"Autoavaliação antes e depois da oficina (n = {n_par})")
    ax.invert_yaxis()
    ax.legend(loc="lower right")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    fig.savefig(saida / "autoavaliacao_antes_depois.png", dpi=200)
    plt.close(fig)

    # ---------- Gráfico 2: quiz
    fig, ax = plt.subplots(figsize=(5, 3.6))
    barras = ax.bar(["Antes", "Depois"], [quiz_antes, quiz_depois], color=["#9DB7D5", "#1F4E8C"])
    ax.bar_label(barras, fmt="%.1f")
    ax.set_ylim(0, 5)
    ax.set_ylabel("Acertos médios (de 5)")
    ax.set_title("Questões de conhecimento")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    fig.savefig(saida / "quiz_antes_depois.png", dpi=200)
    plt.close(fig)

    # ---------- Resumo em Markdown
    md = [
        "# Resultados da oficina",
        "",
        f"- Responderam ao questionário diagnóstico: **{n_pre}**",
        f"- Responderam ao questionário final: **{n_pos}**",
        f"- Participantes com os dois questionários (análise pareada): **{n_par}**",
        "",
        "## Autoavaliação (média de 1 a 5)",
        "",
        tab_auto.to_markdown(index=False),
        "",
        "## Questões de conhecimento",
        "",
        f"- Acertos médios antes: **{quiz_antes:.1f} de 5**",
        f"- Acertos médios depois: **{quiz_depois:.1f} de 5**",
        f"- Participantes que aumentaram a nota: **{melhoraram:.0f}%**",
        "",
    ]
    if aval:
        md += ["## Avaliação da oficina", ""] + [f"- {k}: **{v}**" for k, v in aval.items()] + [""]
    if "comentario" in pos:
        comentarios = pos["comentario"].dropna().astype(str).str.strip()
        comentarios = comentarios[comentarios != ""]
        if len(comentarios):
            md += ["## Comentários dos participantes", ""] + [f"> {c}" for c in comentarios] + [""]
    (saida / "resumo_resultados.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))
    print(f"\nArquivos salvos em: {saida.resolve()}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--pre", required=True, help="CSV do questionário diagnóstico")
    p.add_argument("--pos", required=True, help="CSV do questionário final")
    p.add_argument("--saida", default="resultados", help="pasta de saída")
    a = p.parse_args()
    analisar(carregar(a.pre), carregar(a.pos), Path(a.saida))


if __name__ == "__main__":
    main()
