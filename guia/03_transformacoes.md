# 🔄 Transformações de Escala

## Por que transformar?

Quando o scatter plot mostra uma relação **não-linear** entre X e Y, aplicamos uma transformação matemática em X ou em Y (ou em ambos) para **linearizar** a relação e poder usar a regressão linear.

Bônus frequente das transformações:
- Também corrigem heterocedasticidade (violação da premissa E)
- Muitas vezes melhoram a normalidade dos resíduos

---

## As 3 transformações e as 9 combinações do EP

O EP pede que você teste **3 transformações × em X, Y, ou ambos = 9 combinações**:

| # | Transformação | Aplicada em | Notação |
|---|--------------|-------------|---------|
| 1 | Raiz quadrada (√) | Apenas X | (√X, Y) |
| 2 | Raiz quadrada (√) | Apenas Y | (X, √Y) |
| 3 | Raiz quadrada (√) | Ambos | (√X, √Y) |
| 4 | Quadrado (²) | Apenas X | (X², Y) |
| 5 | Quadrado (²) | Apenas Y | (X, Y²) |
| 6 | Quadrado (²) | Ambos | (X², Y²) |
| 7 | Log₁₀ | Apenas X | (log X, Y) |
| 8 | Log₁₀ | Apenas Y | (X, log Y) |
| 9 | Log₁₀ | Ambos | (log X, log Y) |

---

## Como cada transformação muda a relação

### Raiz quadrada — "comprime" os valores grandes
```
Útil quando: Y cresce mais devagar que X (côncavo para cima)
Exemplo: dados de contagem, áreas
```

### Quadrado — "expande" os valores grandes
```
Útil quando: Y cresce mais rápido que X (convexo para cima)
Exemplo: relações de potência com expoente > 1
```

### Log₁₀ — transforma multiplicativo em aditivo
```
Útil quando: dados variam em várias ordens de magnitude
Útil para: dados que crescem exponencialmente
Interpretação: log(X+1) quando há zeros; np.log10(X)
Preferido pelo professor por ser mais fácil de interpretar que ln
```

---

## Código para gerar os 9 scatter plots

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Carregue seus dados
df = pd.read_csv('../datasets/treadwear.txt', sep='\t')
x = df['mileage']
y = df['groove']

# Dicionário de transformações
transformacoes = {
    'original': lambda v: v,
    'raiz':     lambda v: np.sqrt(v),
    'quadrado': lambda v: v**2,
    'log10':    lambda v: np.log10(v),
}

# Pares de transformações para X e Y (excluindo original-original)
pares = [
    ('raiz',     'original', '(√X, Y)'),
    ('original', 'raiz',     '(X, √Y)'),
    ('raiz',     'raiz',     '(√X, √Y)'),
    ('quadrado', 'original', '(X², Y)'),
    ('original', 'quadrado', '(X, Y²)'),
    ('quadrado', 'quadrado', '(X², Y²)'),
    ('log10',    'original', '(log X, Y)'),
    ('original', 'log10',    '(X, log Y)'),
    ('log10',    'log10',    '(log X, log Y)'),
]

fig, axes = plt.subplots(3, 3, figsize=(14, 12))
axes = axes.flatten()

for i, (tx, ty, titulo) in enumerate(pares):
    x_t = transformacoes[tx](x)
    y_t = transformacoes[ty](y)
    
    axes[i].scatter(x_t, y_t, alpha=0.7, color='steelblue', edgecolors='white', s=60)
    axes[i].set_title(titulo, fontsize=12, fontweight='bold')
    
    # Calcula e mostra correlação
    corr = np.corrcoef(x_t, y_t)[0, 1]
    axes[i].set_xlabel(f'X transformado (r={corr:.3f})')
    axes[i].set_ylabel('Y transformado')
    axes[i].grid(True, alpha=0.3)

plt.suptitle('Scatter plots — 9 combinações de transformações', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()
```

---

## Como escolher a melhor transformação

**Critério visual (o que o EP pede):** qual scatter plot mostra os pontos mais próximos de uma linha reta?

**Critério objetivo:** qual transformação tem **maior correlação** (valor absoluto de r)?

Também ajuda calcular o R² após ajustar cada transformação:

```python
import statsmodels.formula.api as smf

resultados = []
for tx, ty, titulo in pares:
    x_t = transformacoes[tx](x)
    y_t = transformacoes[ty](y)
    
    temp_df = pd.DataFrame({'X': x_t, 'Y': y_t})
    mod = smf.ols('Y ~ X', data=temp_df).fit()
    resultados.append({
        'Transformação': titulo,
        'R²': mod.rsquared,
        'R² ajustado': mod.rsquared_adj,
        'Correlação': np.corrcoef(x_t, y_t)[0, 1]
    })

resultado_df = pd.DataFrame(resultados).sort_values('R² ajustado', ascending=False)
print(resultado_df.to_string(index=False))
```

---

## Atenção com o log quando há zeros

Se X ou Y tiver valores **zero ou negativos**, `log10(0)` = -∞ e vai dar erro!

Soluções comuns:
```python
# Opção 1: log(x + 1) — adiciona 1 para evitar log(0)
np.log10(x + 1)

# Opção 2: log(x + 0.5) — suavização com constante menor
np.log10(x + 0.5)
```

No dataset `ConcPatog.txt`, a coluna CPatog1 tem alguns valores 0 — use log10(X+1).

---

## Como interpretar o modelo transformado

Se você escolheu a transformação log10 em ambos (log X, log Y):

```
log10(Y) = b₀ + b₁ · log10(X)
```

Isso equivale a um modelo de **potência**:
```
Y = 10^b₀ · X^b₁
```

Se escolheu apenas log10 em Y:
```
log10(Y) = b₀ + b₁ · X
```

Equivale a um modelo **exponencial**:
```
Y = 10^(b₀ + b₁·X) = 10^b₀ · 10^(b₁·X)
```

> **Dica**: Para o relatório, você não precisa fazer essa conversão. Apenas informe qual transformação foi escolhida e interprete o R² ajustado do modelo transformado.
