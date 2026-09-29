# 🗺️ Roteiro Geral — EP1 MQAM (ACH2036)
**Prazo: 06/10 | Entrega: PDF via e-disciplinas | Pode ser em dupla**

---

## O que você vai entregar?

Um **relatório em PDF** com análises de regressão linear simples para **3 datasets**:
1. `treadwear.txt` — desgaste de pneu
2. `alligator.txt` — peso de jacarés
3. `ConcPatog.txt` — concentração de patógenos em esgoto

---

## Para CADA dataset, você faz as mesmas 5 etapas:

| Etapa | O que fazer | O que entregar |
|-------|-------------|----------------|
| **1** | Gráfico de dispersão (scatter plot) Y vs X | Gráfico + comentário |
| **2a** | Ajustar regressão linear simples | Tabela de resultados + R² ajustado comentado |
| **2b** | Gráfico com reta + IC + IP | Gráfico |
| **2c** | Análise de resíduos (3 gráficos) | Gráficos + comentário sobre premissas LINE |
| **3→5** | Testar 9 transformações, escolher a melhor | Repetir etapas 1+2 com variáveis transformadas |

---

## Checklist de entrega

Para cada dataset, confirme que tem:

- [ ] Scatter plot original (Y vs X) com comentário
- [ ] Tabela de regressão com comentário sobre R² ajustado
- [ ] Gráfico com reta de regressão + banda de IC + banda de IP
- [ ] Histograma dos resíduos (com curva normal se possível)
- [ ] Resíduos vs. valores preditos (residuals vs. fitted)
- [ ] QQ-plot dos resíduos (normal probability plot)
- [ ] Comentário sobre premissas LINE
- [ ] 9 scatter plots das transformações
- [ ] Escolha justificada da melhor transformação
- [ ] Repetição das etapas 1+2 para a variável transformada

---

## Ordem sugerida de leitura dos guias

```
01_conceitos_regressao.md      → Entenda a teoria antes de tudo
02_premissas_LINE.md           → O que verificar nos resíduos
03_transformacoes.md           → Por que e como transformar
04_codigo_referencia.py        → Código Python pronto para copiar/adaptar
05_interpretacao_resultados.md → Como comentar cada resultado
```

---

## Estrutura dos datasets

| Dataset | Y (resposta) | X (preditora) | n |
|---------|-------------|----------------|---|
| `treadwear.txt` | `groove` | `mileage` | 9 |
| `alligator.txt` | `weight` | `length` | 25 |
| `ConcPatog.txt` | `CPatog2` | `CPatog1` | 105 |
