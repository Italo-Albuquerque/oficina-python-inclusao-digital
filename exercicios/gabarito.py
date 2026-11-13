"""
Gabarito comentado dos exercícios da oficina.
Execute com:  python gabarito.py
(Os exercícios que usam input() foram escritos com valores fixos para rodar direto.)
"""
import pandas as pd

print("=" * 50, "\nENCONTRO 1 — Letramento digital\n" + "=" * 50)
# 1. Segundos em um dia
print("Segundos em um dia:", 24 * 60 * 60)
# 2. Pizza dividida entre 5 amigos
print(f"Cada amigo paga: R$ {48 / 5:.2f}")
# 3. Nome e escola
print("Meu nome é Fulano e estudo na Escola Estadual X.")

print("=" * 50, "\nENCONTRO 2 — Python básico\n" + "=" * 50)
# 1. Conversor de temperatura   (em sala: c = float(input("Temperatura em °C: ")))
c = 30.0
print(f"{c} °C = {c * 9 / 5 + 32} °F")
# 2. Média de três notas
n1, n2, n3 = 7.5, 8.0, 6.0
media = (n1 + n2 + n3) / 3
print(f"Média: {media:.1f}")
# 3. Conta de luz
consumo_kwh, preco_kwh = 150, 0.85
print(f"Valor da conta: R$ {consumo_kwh * preco_kwh:.2f}")

print("=" * 50, "\nENCONTRO 3 — Lógica\n" + "=" * 50)
# 1. Par ou ímpar
numero = 17
print(numero, "é par" if numero % 2 == 0 else "é ímpar")
# 2. Múltiplos de 3 entre 1 e 50
print("Múltiplos de 3:", [i for i in range(1, 51) if i % 3 == 0])
# 3. Maiores de idade
idades = [15, 17, 14, 18, 16, 19]
maiores = 0
for idade in idades:
    if idade >= 18:
        maiores += 1
print("Maiores de idade:", maiores)

print("=" * 50, "\nENCONTRO 4 — Automação de dados\n" + "=" * 50)
df = pd.DataFrame({
    "aluno": ["Ana", "Bruno", "Carla", "Diego", "Eduarda", "Felipe", "Gabriela", "Heitor", "Isabela", "João"],
    "matematica": [8.5, 5.0, 9.5, 6.0, 7.5, 4.0, 8.0, 6.5, 10.0, 5.5],
    "portugues": [7.0, 6.5, 9.0, 5.5, 8.0, 5.0, 9.5, 7.0, 8.5, 4.0],
    "ciencias": [9.0, 4.5, 8.5, 7.0, 6.5, 5.5, 9.0, 7.5, 9.5, 6.0],
    "faltas": [2, 8, 0, 5, 1, 12, 3, 4, 0, 9],
})
disciplinas = ["matematica", "portugues", "ciencias"]
df["media"] = df[disciplinas].mean(axis=1).round(1)
# 1. Maior nota de Ciências
melhor = df.sort_values("ciencias", ascending=False).iloc[0]
print(f"Maior nota de Ciências: {melhor['aluno']} ({melhor['ciencias']})")
# 2. Média da turma por disciplina
print("Média da turma por disciplina:")
print(df[disciplinas].mean().round(2).to_string())
# 3. Bônus para quem não faltou
df["bonus"] = df["media"] + (df["faltas"] == 0) * 0.5
print(df[["aluno", "media", "faltas", "bonus"]].to_string(index=False))
