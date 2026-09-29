# 📚 Conceitos Fundamentais de Regressão Linear Simples

## 1. O que é Regressão Linear Simples?

É um modelo estatístico que descreve a relação entre **uma variável resposta Y** e **uma variável preditora X** através de uma reta:

```
Y = β₀ + β₁·X + ε
```

| Símbolo | Nome | Significado |
|---------|------|-------------|
| `β₀` | Intercepto | Valor esperado de Y quando X = 0 |
| `β₁` | Slope (inclinação) | Quanto Y muda, em média, para cada aumento de 1 unidade em X |
| `ε` | Erro aleatório | O que o modelo não explica (ruído) |

Os valores estimados a partir dos dados são chamados de **b₀** e **b₁** (para diferenciar dos parâmetros populacionais β₀ e β₁).

---

## 2. Como o modelo é ajustado? (Mínimos Quadrados)

O método de **Mínimos Quadrados Ordinários (OLS)** encontra b₀ e b₁ que **minimizam a soma dos quadrados dos resíduos**:

```
SSE = Σ (yᵢ - ŷᵢ)² = Σ eᵢ²
```

Onde:
- `yᵢ` = valor real observado
- `ŷᵢ` = valor predito pelo modelo (= b₀ + b₁·xᵢ)
- `eᵢ` = resíduo (diferença entre real e predito)

---

## 3. Decomposição da variância (SSTO, SSR, SSE)

A variação total de Y pode ser decomposta em:

```
SSTO = SSR + SSE
```

| Sigla | Nome | Fórmula | O que significa |
|-------|------|---------|-----------------|
| **SSTO** | Soma Total dos Quadrados | Σ(yᵢ - ȳ)² | Variabilidade total de Y |
| **SSR** | Soma dos Quadrados da Regressão | Σ(ŷᵢ - ȳ)² | Quanto o modelo explica |
| **SSE** | Soma dos Quadrados dos Erros | Σ(yᵢ - ŷᵢ)² | Quanto sobrou (não explicado) |

---

## 4. R² — Coeficiente de Determinação

```
R² = SSR / SSTO = 1 - (SSE / SSTO)
```

**Interpretação:**
- Varia de 0 a 1 (ou 0% a 100%)
- Indica a **proporção da variabilidade de Y explicada pelo modelo**
- R² = 0.75 → o modelo explica 75% da variação em Y
- **Quanto maior, melhor** (mas cuidado: não é a única métrica!)

### R² Ajustado

O R² sobe artificialmente quando você adiciona mais variáveis. O R² ajustado penaliza por isso:

```
R²_adj = 1 - (1 - R²) · (n-1)/(n-p-1)
```

Em regressão simples (p=1 preditora), a diferença é pequena, mas use sempre o **R² ajustado** para reportar.

---

## 5. Tabela de Coeficientes — Como interpretar

Quando você faz `modelo.summary()`, a tabela central mostra:

```
              coef    std err          t      P>|t|      [0.025      0.975]
Intercept    b₀       SE(b₀)    t=b₀/SE   p-valor    IC_inf    IC_sup
X            b₁       SE(b₁)    t=b₁/SE   p-valor    IC_inf    IC_sup
```

| Coluna | O que significa |
|--------|-----------------|
| `coef` | Estimativa do coeficiente (b₀ ou b₁) |
| `std err` | Erro padrão — incerteza da estimativa |
| `t` | Estatística de teste (coef / std err) |
| `P>|t|` | p-valor do teste H₀: β = 0 |
| `[0.025, 0.975]` | Intervalo de confiança de 95% para o coeficiente |

### Teste de hipótese para β₁

- **H₀**: β₁ = 0 (não há relação linear entre X e Y)
- **H₁**: β₁ ≠ 0 (há relação linear)
- Se `p-valor < 0.05`: rejeitamos H₀ → **há evidência de relação linear**
- Se o IC de β₁ **não contém 0**: mesma conclusão

---

## 6. Intervalo de Confiança (IC) vs. Intervalo de Predição (IP)

Ambos são calculados para um valor específico X = xₕ:

| | Para quem? | Largura |
|--|------------|---------|
| **IC** | Média de Y para todos os indivíduos com X = xₕ | Mais estreito |
| **IP** | Uma nova observação individual com X = xₕ | Mais largo |

O IP é sempre mais largo porque carrega a incerteza adicional do erro aleatório ε.

---

## 7. Tabela ANOVA

A tabela ANOVA testa se o modelo como um todo é significativo:

```
                df    sum_sq     mean_sq        F    PR(>F)
X               1      SSR       MSR=SSR/1     F*    p-valor
Residual      n-2      SSE       MSE=SSE/(n-2)
```

- **F = MSR / MSE** → quanto o modelo explica vs. quanto é ruído
- Se `p-valor < 0.05`: o modelo é estatisticamente significativo
- Em regressão simples, o teste F é equivalente ao teste t para β₁

---

## 8. MSE e Erro Padrão da Regressão (s)

```
MSE = SSE / (n-2)      ← "Erro Quadrático Médio"
s   = √MSE              ← "Erro Padrão da Regressão"
```

- `s` é a estimativa do desvio padrão dos erros (ε)
- No `modelo.summary()`, aparece como `Root MSE` ou pode ser obtido via `modelo.mse_resid`
- Interpretação: em média, as predições erram por ±s unidades de Y
