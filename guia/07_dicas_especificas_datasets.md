# 💡 Dicas Específicas para Cada Dataset

---

## Dataset 1 — Treadwear
**Y = groove (profundidade do sulco) | X = mileage (milhas rodadas)**

### O que esperar:
- n = 9 observações (muito pequeno!)
- Relação claramente negativa: mais milhas → mais desgaste → sulco menor
- O scatter plot original provavelmente já mostrará boa linearidade
- R² original deve ser alto (dados quase perfeitamente lineares)

### Dicas:
- Com n=9, o histograma de resíduos terá poucos pontos — não exija muito dele
- O QQ-plot é mais informativo que o histograma para n pequeno
- Mesmo que o modelo linear simples já seja bom, teste as transformações como pedido
- Atenção: `np.log10(0)` = erro. Mas mileage começa em 0! Para log de X, use `np.log10(mileage + 1)` ou exclua mileage=0

```python
# Cuidado com mileage = 0 no log:
df_sem_zero = df[df['mileage'] > 0]  # opcional: excluir ponto x=0 para log(X)
# OU use log(mileage + 1) para incluir todos:
x_log = np.log10(df['mileage'] + 1)
```

---

## Dataset 2 — Alligator
**Y = weight (peso em libras) | X = length (comprimento em centímetros)**

### O que esperar:
- n = 25 observações
- A relação peso × comprimento em jacarés é tipicamente uma **relação de potência**
- Biologicamente, o peso cresce com o **cubo** do comprimento (alometria)
- O scatter plot original deve mostrar curvatura acentuada (crescimento não-linear)
- A transformação **log-log** (log X, log Y) geralmente lineariza muito bem dados de escala alométrica

### Por que a relação é curvilínea?
```
weight ~ length³  (em geral, para animais)
```
Ao aplicar log10 em ambos:
```
log10(weight) = log10(c) + 3 × log10(length)
```
Isso vira uma reta com slope ≈ 3!

### Dicas:
- O dataset não tem zeros → pode usar log10 diretamente
- Provavelmente a melhor transformação será (log length, log weight)
- Verifique se b₁ ≈ 3 no modelo log-log (isso validaria a relação cúbica esperada biologicamente)

---

## Dataset 3 — ConcPatog
**Y = CPatog2 | X = CPatog1 | n = 105**

### O que esperar:
- Este é o mais complexo dos 3
- Dados de concentração de patógenos variam em **ordens de magnitude** (1 a 354.000!)
- O scatter plot original deve ser muito difícil de interpretar visualmente
- Quase certamente precisará de transformação log

### Atenção com zeros!
```python
# CPatog1 e CPatog2 têm valores = 0
# Log10(0) = -inf → use log10(X + 1)
x_log = np.log10(df['CPatog1'] + 1)
y_log = np.log10(df['CPatog2'] + 1)
```

### Por que log é quase certamente a melhor transformação?
- Dados de microbiologia são comumente analisados em escala logarítmica
- Concentrações variam de 0 a centenas de milhares → distribuição muito assimétrica
- Log10 comprime os valores extremos e estabiliza a variância

### Dicas adicionais:
- Com n=105, todos os gráficos de diagnóstico são mais confiáveis
- O QQ-plot e histograma dos resíduos são informativos (tamanho amostral grande)
- Mesmo após transformação, pode haver alguma heterocedasticidade residual — comente isso
- O dataset tem variáveis categóricas (ETE, Tratamento, Estagio, Mes...) mas o EP pede apenas CPatog1 → CPatog2

---

## Comparação esperada dos 3 datasets

| Dataset | Linearidade original | Melhor transformação esperada |
|---------|---------------------|-------------------------------|
| Treadwear | Boa (mas verifique) | log-log ou raiz-raiz possivelmente melhoram |
| Alligator | Ruim (curva acentuada) | log-log (relação alométrica) |
| ConcPatog | Ruim (enorme variabilidade) | log-log (dados de concentração) |

---

## Sobre a premissa I (Independência)

Para todos os datasets:
- **Treadwear**: as medições foram feitas em momentos diferentes do mesmo pneu. Pode haver leve dependência serial, mas assume-se independência para fins do EP.
- **Alligator**: animais diferentes → independentes.
- **ConcPatog**: amostras de meses diferentes, ETEs diferentes → pode haver correlação temporal. Mencione que a premissa I é assumida mas pode ser questionada dado o design do estudo.

---

## Formatação do relatório

O EP pede apenas o **PDF final**, sem código Python. Sugestão:

1. Use Jupyter Notebook e gere as figuras
2. Salve as figuras como PNG (`plt.savefig('figura.png', dpi=150, bbox_inches='tight')`)
3. Monte o relatório no Word, Google Docs ou LaTeX
4. Exporte como PDF

**Estrutura sugerida do relatório:**

```
1. Introdução (breve — 1 parágrafo)

2. Dataset: Treadwear
   2.1 Scatter plot e comentário
   2.2 Modelo de regressão
       2.2.1 Tabela de resultados e R²
       2.2.2 Gráfico com reta + IC + IP
       2.2.3 Análise de resíduos e premissas LINE
   2.3 Transformações
       2.3.1 Scatter plots das 9 transformações
       2.3.2 Justificativa da escolha
   2.4 Modelo transformado
       2.4.1 Scatter plot transformado
       2.4.2 Tabela de resultados e R²
       2.4.3 Gráfico com reta + IC + IP
       2.4.4 Análise de resíduos e premissas LINE

3. Dataset: Alligator [mesma estrutura]

4. Dataset: ConcPatog [mesma estrutura]
```

---

## 🎯 Spoiler: resultados reais de validação (não coloque no relatório)

Rode seus próprios modelos e analise. Mas para conferir se seu código está correto:

| Dataset | n | R²_adj original | Melhor transformação | R²_adj transformado |
|---------|---|-----------------|---------------------|---------------------|
| Treadwear | 9 | ~0.946 | (X, log Y) | ~0.992 |
| Alligator | 25 | ~0.829 | (X, log Y) | ~0.958 |
| ConcPatog | 105 | ~0.086 | (log X, log Y) | ~0.660 |

**O que isso nos diz:**
- **Treadwear**: já tinha bom ajuste linear (R²=0.946), mas aplicar log em Y melhorou ainda mais
- **Alligator**: melhora expressiva com transformação (0.829 → 0.958)
- **ConcPatog**: o modelo linear original é praticamente inútil (R²=0.086!). A transformação log-log melhora muito, mas mesmo 0.66 ainda deixa 34% inexplicado — comente isso no relatório.

**Atenção**: o aviso `RuntimeWarning: divide by zero` no ConcPatog é esperado (há zeros em CPatog1). 
O código já trata isso com `+1` (offset). Certifique-se de usar `offset=1` no seu código para ConcPatog.

### Setup do ambiente Python (se precisar rodar localmente)

Um venv com tudo instalado já foi criado em `/home/yodonov/projects/MQAM/.venv/`. Para usar:

```bash
# No terminal, dentro da pasta do projeto:
source .venv/bin/activate

# Agora rode seus scripts:
python3 guia/06_exemplo_treadwear.py

# Ou inicie o Jupyter:
pip install jupyter
jupyter notebook
```
