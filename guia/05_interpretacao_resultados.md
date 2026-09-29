# 📝 Como Interpretar e Comentar os Resultados

Este guia te dá frases-modelo para comentar cada parte do EP. Adapte os valores.

---

## Etapa 1 — Scatter Plot Original

**Template de comentário:**

> "O gráfico de dispersão entre [Y] (eixo vertical) e [X] (eixo horizontal) mostra [uma associação positiva/negativa/nenhuma associação visível] entre as variáveis. [Os pontos seguem uma tendência aproximadamente linear / A relação apresenta curvatura notável, com os valores de Y crescendo mais rapidamente que X / Os dados apresentam grande variabilidade sem tendência clara]. A correlação de Pearson é r = X.XX, indicando [fraca/moderada/forte] associação [positiva/negativa]."

**Classificação do r:**
| |r| | Interpretação |
|-------|----------------|
| 0.00–0.19 | Muito fraca |
| 0.20–0.39 | Fraca |
| 0.40–0.59 | Moderada |
| 0.60–0.79 | Forte |
| 0.80–1.00 | Muito forte |

---

## Etapa 2a — R² Ajustado

**Template:**

> "O R² ajustado do modelo é X.XX (XX%), indicando que o modelo explica [apenas XX% / cerca de XX% / uma proporção elevada de XX%] da variabilidade de [Y]. [Este valor sugere um ajuste razoável / Um R² ajustado tão baixo sugere que a relação linear é fraca, e possivelmente uma transformação de escala possa melhorar o ajuste / O modelo captura bem a variabilidade de Y]."

**Referências de R²:**
| R²_adj | Qualidade do ajuste |
|--------|---------------------|
| < 0.30 | Fraco — modelo explica pouco |
| 0.30–0.60 | Moderado |
| 0.60–0.80 | Bom |
| > 0.80 | Muito bom |
| → 1.00 | Excelente (cuidado com overfitting em n pequeno) |

---

## Etapa 2b — Gráfico com Reta, IC e IP

> "O gráfico mostra a reta de regressão ajustada, acompanhada da banda de 95% de confiança para a média (região mais escura) e da banda de 95% de predição para novas observações (região mais clara). Como esperado, a banda de predição é mais larga, pois incorpora tanto a incerteza sobre a reta quanto o erro aleatório individual."

---

## Etapa 2c — Análise de Resíduos (premissas LINE)

### Histograma dos resíduos

✅ **Quando a premissa N é satisfeita:**
> "O histograma dos resíduos apresenta forma aproximadamente simétrica e unimodal, compatível com uma distribuição normal. A curva de densidade normal sobreposta ao histograma se ajusta bem aos dados. A premissa de normalidade (N) parece ser satisfeita."

❌ **Quando é violada:**
> "O histograma apresenta forte assimetria à direita (cauda longa à direita), indicando que os resíduos não seguem distribuição normal. A premissa N parece violada."

### Resíduos vs. Preditos

✅ **Linearidade e variância constante OK:**
> "O gráfico de resíduos vs. valores preditos mostra pontos distribuídos aleatoriamente em torno da linha horizontal y=0, sem padrão sistemático visível. Isso indica que as premissas de linearidade (L) e variância constante (E) parecem ser satisfeitas."

❌ **Curvatura (violação de L):**
> "O gráfico de resíduos vs. preditos exibe um padrão curvilíneo (em forma de 'U'), indicando que a relação entre X e Y não é puramente linear. A premissa L está possivelmente violada."

❌ **Funil (violação de E — heterocedasticidade):**
> "Observa-se no gráfico um padrão de 'funil', com os resíduos apresentando dispersão crescente conforme os valores preditos aumentam. Isso sugere heterocedasticidade, ou seja, violação da premissa E de variância constante dos erros."

### QQ-Plot

✅ **Normalidade OK:**
> "No QQ-plot, os pontos se alinham próximos à reta diagonal de referência, sem desvios sistemáticos nas caudas. Isso corrobora a premissa de normalidade (N)."

❌ **Caudas pesadas:**
> "O QQ-plot mostra desvios nas extremidades (pontos acima da reta na cauda superior e abaixo na cauda inferior), característico de distribuição com caudas mais pesadas que a normal (leptocúrtica). A premissa N parece violada."

---

## Etapas 3-4 — Escolha da melhor transformação

> "Foram testadas 9 combinações de transformações (raiz quadrada, quadrado e log₁₀, aplicadas a X, a Y e a ambas). A comparação visual dos scatter plots e os valores de R² ajustado indicam que a transformação (log X, log Y) — ou seja, log₁₀ aplicado tanto a [X] quanto a [Y] — é a que melhor lineariza a relação entre as variáveis, com R² ajustado = X.XX. Os pontos no scatter plot transformado se distribuem de forma mais próxima a uma reta, justificando esta escolha."

---

## Etapa 5 — Modelo Transformado

> "Após aplicar a transformação log₁₀ em ambas as variáveis, o modelo ajustado é:
>
> log₁₀([Y]) = b₀ + b₁ · log₁₀([X])
>
> com b₀ = X.XXXX e b₁ = X.XXXX. O R² ajustado passou de X.XX (modelo original) para X.XX (modelo transformado), indicando uma melhora substancial no ajuste. A análise de resíduos do modelo transformado também mostra menor evidência de violações das premissas LINE em comparação com o modelo original."

---

## Dica: Tabela-resumo para o relatório

Considere incluir uma tabela assim no relatório:

| | Treadwear | Alligator | ConcPatog |
|-|-----------|-----------|-----------|
| R² original | X.XX | X.XX | X.XX |
| Premissas violadas | L, E | - | L, N, E |
| Melhor transformação | log X, log Y | log X, log Y | log X, log Y |
| R² transformado | X.XX | X.XX | X.XX |
