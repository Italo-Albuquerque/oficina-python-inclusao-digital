# Oficina de Letramento Digital e Programação Básica com Python

Projeto de **Atividade Extensionista II: Tecnologia Aplicada à Inclusão Digital** — CST em Ciência de Dados, Centro Universitário Internacional UNINTER.

**Autor:** Ítalo Albuquerque da Silva  
**Público-alvo:** estudantes do ensino médio de escolas públicas da rede estadual de Fortaleza – CE  
**Formato:** 4 encontros síncronos de 2 h pelo **Google Meet**, com prática no **Google Colab** (sem instalar nada, funciona no computador ou no celular)  
**ODS:** 4 – Educação de qualidade · 9 – Indústria, inovação e infraestrutura · 10 – Redução das desigualdades

---

## Objetivos

- Diagnosticar o conhecimento prévio dos participantes em informática, navegação na web e lógica, com um questionário de nivelamento.
- Desenvolver material didático prático em Python, usando notebooks do Google Colab.
- Capacitar os estudantes na resolução de problemas lógicos e na automação básica de dados, promovendo a inclusão digital e o interesse pelas áreas STEM.

## Conteúdo do repositório

```
.
├── notebooks/                        # material das aulas (abrir no Colab)
│   ├── 01_letramento_digital.ipynb
│   ├── 02_python_basico.ipynb
│   ├── 03_logica_condicionais_lacos.ipynb
│   └── 04_automacao_dados.ipynb
├── exercicios/
│   └── gabarito.py                   # soluções comentadas dos exercícios
├── avaliacao/
│   ├── questionario_diagnostico.md   # aplicado antes da oficina (Google Forms)
│   ├── questionario_final.md         # aplicado depois da oficina (Google Forms)
│   ├── analise_questionarios.py      # compara antes x depois e gera gráficos
│   └── exemplo_ficticio/             # dados FICTÍCIOS só para testar o script
├── metodologia/
│   ├── diagrama_metodologia.dot      # fonte do diagrama (Graphviz)
│   └── diagrama_metodologia.png
├── requirements.txt
└── LICENSE
```

## Encontros

| Encontro | Tema | Duração | Notebook |
|---|---|---|---|
| 1 | Letramento digital, segurança na internet e primeiros passos no Colab | 2 h | [01](notebooks/01_letramento_digital.ipynb) |
| 2 | Python básico: variáveis, tipos, `input()` e f-strings | 2 h | [02](notebooks/02_python_basico.ipynb) |
| 3 | Lógica: condicionais, listas, laços e jogo de adivinhação | 2 h | [03](notebooks/03_logica_condicionais_lacos.ipynb) |
| 4 | Automação de dados com pandas: boletim automático e gráficos | 2 h | [04](notebooks/04_automacao_dados.ipynb) |

## Metodologia

![Diagrama da metodologia](metodologia/diagrama_metodologia.png)

## Como usar

### Participantes (no Colab)
Clique no botão **Abrir no Colab** no topo de cada notebook e depois em **Arquivo → Salvar uma cópia no Drive**.

### Rodar localmente
```bash
pip install -r requirements.txt
python exercicios/gabarito.py
```

### Analisar os questionários
1. Exporte as respostas de cada formulário do Google Forms em CSV.
2. Garanta que as colunas tenham os nomes curtos descritos em `avaliacao/questionario_*.md` (ou ajuste o dicionário `RENOMEAR` no script).
3. Execute:
```bash
cd avaliacao
python analise_questionarios.py --pre diagnostico.csv --pos final.csv --saida resultados
```
O script gera `resumo_resultados.md`, `autoavaliacao_antes_depois.png` e `quiz_antes_depois.png`.

Para testar com os dados fictícios:
```bash
python analise_questionarios.py --pre exemplo_ficticio/diagnostico.csv --pos exemplo_ficticio/final.csv --saida resultados_exemplo
```

> ⚠️ Os arquivos em `exemplo_ficticio/` são inventados e servem **apenas** para testar o script. Os resultados reais da oficina devem vir das respostas reais dos participantes.

## Privacidade
Os participantes são identificados apenas por um código escolhido por eles; nenhum nome, telefone ou e-mail é publicado neste repositório.

## Licença
[MIT](LICENSE)
