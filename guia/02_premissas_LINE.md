# 🔍 Premissas LINE e Análise de Resíduos

## As 4 premissas do modelo de Regressão Linear Simples

O modelo Y = β₀ + β₁X + ε é válido apenas se os erros ε satisfazem as premissas **LINE**:

| Letra | Premissa | O que significa |
|-------|----------|-----------------|
| **L** | **L**inear function | A relação entre X e Y é **de fato linear** |
| **I** | **I**ndependent errors | Os erros são **independentes** entre si |
| **N** | **N**ormal distribution | Os erros seguem distribuição **normal** |
| **E** | **E**qual variance | Os erros têm **variância constante** (homocedasticidade) |

Se alguma premissa for violada, as estimativas e inferências do modelo podem ser inválidas.

---

## Os 3 gráficos de resíduo que você vai fazer

### Gráfico 1 — Histograma dos Resíduos
**O que mostra:** distribuição dos resíduos  
**O que verificar:** premissa **N** (Normalidade)

✅ OK se: histograma aproximadamente simétrico em forma de sino  
❌ Violação se: assimetria forte, caudas pesadas, ou picos/vales inesperados

```python
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

residuos = modelo.resid
fig, ax = plt.subplots(figsize=(7, 5))
ax.hist(residuos, bins='auto', density=True, alpha=0.7, color='steelblue', edgecolor='white')

# Curva normal de referência
x_range = np.linspace(residuos.min(), residuos.max(), 200)
ax.plot(x_range, stats.norm.pdf(x_range, residuos.mean(), residuos.std()), 
        'r-', linewidth=2, label='Normal')
ax.set_xlabel('Resíduos')
ax.set_ylabel('Densidade')
ax.set_title('Histograma dos Resíduos')
ax.legend()
plt.tight_layout()
plt.show()
```

---

### Gráfico 2 — Resíduos vs. Valores Preditos
**O que mostra:** como os resíduos se distribuem em função dos valores preditos  
**O que verificar:** premissas **L** (linearidade) e **E** (variância constante)

✅ OK se: pontos espalhados **aleatoriamente** em torno de y=0, sem padrão  
❌ Violação **L** se: padrão curvilíneo visível (abre em "U" ou "∩")  
❌ Violação **E** se: dispersão dos resíduos **aumenta** (ou diminui) com os valores preditos (forma de "funil")

```python
fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(modelo.fittedvalues, modelo.resid, alpha=0.7, color='steelblue', edgecolors='white')
ax.axhline(0, color='red', linestyle='--', linewidth=1.5)
ax.set_xlabel('Valores Preditos (ŷ)')
ax.set_ylabel('Resíduos (e = y - ŷ)')
ax.set_title('Resíduos vs. Valores Preditos')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

---

### Gráfico 3 — QQ-Plot dos Resíduos
**O que mostra:** os quantis dos resíduos vs. quantis da distribuição normal teórica  
**O que verificar:** premissa **N** (Normalidade)

✅ OK se: pontos alinhados próximos à linha diagonal  
❌ Violação se: pontos curvados nas extremidades (caudas pesadas) ou forma de "S"

```python
import scipy.stats as stats

fig, ax = plt.subplots(figsize=(7, 5))
(osm, osr), (slope, intercept, r) = stats.probplot(modelo.resid, dist='norm', plot=ax)
ax.set_title('QQ-Plot dos Resíduos (vs. Normal)')
plt.tight_layout()
plt.show()

# Ou usando statsmodels:
import statsmodels.graphics.gofplots as smgof
fig = smgof.qqplot(modelo.resid, line='s')
plt.title('QQ-Plot dos Resíduos')
plt.show()
```

---

## Como comentar as premissas LINE

Use essa estrutura para cada dataset:

```
Análise das premissas LINE:

L (Linearidade): [Satisfeita / Violada]
  → Com base no scatter plot original e no gráfico de resíduos vs. preditos,
    [observamos padrão aleatório / observamos curvatura ...]

I (Independência): [Assumida / Suspeita]
  → Não é possível verificar apenas com esses gráficos. Assumimos que as 
    observações são independentes dado o design do estudo. [OU: Há suspeita 
    de dependência pois as medições são séries temporais...]

N (Normalidade): [Satisfeita / Violada]
  → O histograma mostra [forma aproximadamente normal / assimetria ...].
    O QQ-plot mostra [pontos próximos à diagonal / desvios nas caudas ...].

E (Variância constante): [Satisfeita / Violada]
  → O gráfico de resíduos vs. preditos mostra [dispersão uniforme / 
    padrão de funil, com maior dispersão para valores maiores...].
```

---

## O que significa cada violação para o seu EP?

| Violação detectada | Consequência | O que o EP pede |
|-------------------|-------------|-----------------|
| Não-linearidade | Reta não é adequada | Testar transformações (etapa 3) |
| Heterocedasticidade | Intervalos de confiança incorretos | Transformações podem corrigir |
| Não-normalidade | Testes de hipótese menos confiáveis | Transformações podem ajudar |
| Dependência | Erros padrão subestimados | Fora do escopo do EP |

> **Dica**: As transformações nas etapas 3-5 do EP são justamente para corrigir violações de linearidade e, muitas vezes, também de heterocedasticidade e normalidade.
