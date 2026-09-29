"""
=============================================================================
EXEMPLO GUIADO — Dataset Treadwear (o mais simples dos 3)
=============================================================================
Rode este arquivo para ver TUDO funcionando antes de fazer o seu EP.
Cada seção tem comentários explicando o que está acontecendo.

Execute: python3 06_exemplo_treadwear.py
(ou cole no Jupyter célula por célula)
=============================================================================
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
import statsmodels.formula.api as smf
import statsmodels.graphics.gofplots as smgof

# ─────────────────────────────────────────────────────────────────
# CARREGAMENTO
# ─────────────────────────────────────────────────────────────────
df = pd.read_csv('../datasets/treadwear.txt', sep='\t')
df = df.dropna()

x = df['mileage']    # preditora (X): milhas rodadas
y = df['groove']     # resposta (Y): profundidade do sulco (groove)

print("=== TREADWEAR ===")
print(f"n = {len(df)}")
print(df.describe())
# Interpretação dos dados:
# - mileage: quantas milhas o pneu rodou (0, 4, 8, ..., 32 × 1000 milhas)
# - groove: profundidade do sulco do pneu (em milésimos de polegada)
# - Esperamos que conforme mileage aumenta, groove diminui (pneu desgasta)

# ─────────────────────────────────────────────────────────────────
# ETAPA 1: SCATTER PLOT
# ─────────────────────────────────────────────────────────────────
r = np.corrcoef(x, y)[0, 1]

fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter(x, y, s=100, color='steelblue', edgecolors='white', linewidth=1.5, zorder=5)
ax.set_xlabel('Mileage (× 1000 milhas)', fontsize=13)
ax.set_ylabel('Groove depth (0.001 pol.)', fontsize=13)
ax.set_title('Scatter Plot — Treadwear\n(Desgaste do pneu vs. Milhas rodadas)', fontsize=13)
ax.grid(True, alpha=0.3)
ax.annotate(f'r = {r:.4f}', xy=(0.05, 0.92), xycoords='axes fraction', fontsize=12,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', alpha=0.9))
plt.tight_layout()
plt.savefig('fig_01_scatter_treadwear.png', dpi=150, bbox_inches='tight')
plt.show()
print(f"\nCorrelação de Pearson: r = {r:.4f}")
print("""
COMENTÁRIO PARA O RELATÓRIO:
O gráfico mostra uma forte associação negativa entre as variáveis (r = -0.99XX).
Conforme as milhas rodadas aumentam, a profundidade do sulco diminui.
Há indício visual de associação aproximadamente linear, embora com leve curvatura.
""")

# ─────────────────────────────────────────────────────────────────
# ETAPA 2a: AJUSTE DO MODELO
# ─────────────────────────────────────────────────────────────────
modelo = smf.ols('groove ~ mileage', data=df).fit()
b0 = modelo.params['Intercept']
b1 = modelo.params['mileage']
r2 = modelo.rsquared
r2_adj = modelo.rsquared_adj

print("="*70)
print("RESULTADOS DO AJUSTE — MODELO LINEAR ORIGINAL")
print("="*70)
print(modelo.summary())
print(f"\nEquação: groove = {b0:.4f} + ({b1:.4f}) × mileage")
print(f"R² = {r2:.4f}  |  R² ajustado = {r2_adj:.4f}")
print(f"""
COMENTÁRIO:
O R² ajustado = {r2_adj:.4f} indica que o modelo explica {r2_adj*100:.1f}% da 
variabilidade da profundidade do sulco. [Complete com sua interpretação]

O coeficiente b₁ = {b1:.4f} (p-valor = {modelo.pvalues['mileage']:.4f}) indica que,
para cada 1000 milhas adicionais, a profundidade do sulco diminui em média
{abs(b1):.4f} milésimos de polegada. O p-valor {'< 0.05 → relação estatisticamente significativa.' if modelo.pvalues['mileage'] < 0.05 else '≥ 0.05 → relação não significativa.'}
""")

# ─────────────────────────────────────────────────────────────────
# ETAPA 2b: GRÁFICO COM RETA + IC + IP
# ─────────────────────────────────────────────────────────────────
x_range = np.linspace(x.min(), x.max(), 200)
pred_df_range = pd.DataFrame({'mileage': x_range})
pred = modelo.get_prediction(pred_df_range)
pred_summary = pred.summary_frame(alpha=0.05)

fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(x, y, s=100, color='steelblue', edgecolors='white', linewidth=1.5, zorder=5, label='Observações')
ax.plot(x_range, pred_summary['mean'], color='crimson', linewidth=2.5, label='Reta de Regressão')
ax.fill_between(x_range, pred_summary['mean_ci_lower'], pred_summary['mean_ci_upper'],
                alpha=0.3, color='crimson', label='IC 95% (para a média)')
ax.fill_between(x_range, pred_summary['obs_ci_lower'], pred_summary['obs_ci_upper'],
                alpha=0.15, color='darkorange', label='IP 95% (nova obs.)')
ax.set_xlabel('Mileage (× 1000 milhas)', fontsize=12)
ax.set_ylabel('Groove depth (0.001 pol.)', fontsize=12)
ax.set_title(f'Regressão com IC e IP — Treadwear  (R²_adj = {r2_adj:.3f})', fontsize=13)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('fig_02_regressao_treadwear.png', dpi=150, bbox_inches='tight')
plt.show()

# ─────────────────────────────────────────────────────────────────
# ETAPA 2c: ANÁLISE DE RESÍDUOS
# ─────────────────────────────────────────────────────────────────
residuos = modelo.resid
fitted = modelo.fittedvalues

fig, axes = plt.subplots(1, 3, figsize=(16, 5))
fig.suptitle('Análise de Resíduos — Treadwear (modelo original)', fontsize=13, fontweight='bold')

# Histograma
ax = axes[0]
ax.hist(residuos, bins=5, density=True, alpha=0.7, color='steelblue', edgecolor='white')
x_norm = np.linspace(residuos.min(), residuos.max(), 200)
ax.plot(x_norm, stats.norm.pdf(x_norm, residuos.mean(), residuos.std()), 'r-', lw=2)
ax.set_title('Histograma dos Resíduos')
ax.set_xlabel('Resíduos'); ax.set_ylabel('Densidade')

# Resíduos vs. Preditos
ax = axes[1]
ax.scatter(fitted, residuos, color='steelblue', edgecolors='white', s=80)
ax.axhline(0, color='red', linestyle='--', lw=1.5)
ax.set_title('Resíduos vs. Preditos')
ax.set_xlabel('Valores Preditos (ŷ)'); ax.set_ylabel('Resíduos (e)')
ax.grid(True, alpha=0.3)

# QQ-Plot
ax = axes[2]
smgof.qqplot(residuos, line='s', ax=ax)
ax.set_title('QQ-Plot dos Resíduos')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('fig_03_residuos_treadwear.png', dpi=150, bbox_inches='tight')
plt.show()

# Teste de Shapiro-Wilk
stat_sw, p_sw = stats.shapiro(residuos)
print(f"\nShapiro-Wilk: W={stat_sw:.4f}, p={p_sw:.4f}")
print("""
COMENTÁRIO SOBRE AS PREMISSAS LINE:
L (Linearidade): O gráfico de resíduos vs. preditos mostra [descreva o padrão]
I (Independência): Assumida — os dados são medições independentes.
N (Normalidade): [Descreva o histograma e QQ-plot]
E (Variância constante): [Descreva o padrão no gráfico de resíduos vs. preditos]
""")

# ─────────────────────────────────────────────────────────────────
# ETAPAS 3-4: AS 9 TRANSFORMAÇÕES
# ─────────────────────────────────────────────────────────────────
pares = [
    (np.sqrt, None,      '(√mileage, groove)'),
    (None,    np.sqrt,   '(mileage, √groove)'),
    (np.sqrt, np.sqrt,   '(√mileage, √groove)'),
    (lambda v: v**2, None,      '(mileage², groove)'),
    (None,    lambda v: v**2,   '(mileage, groove²)'),
    (lambda v: v**2, lambda v: v**2, '(mileage², groove²)'),
    (np.log10, None,     '(log mileage, groove)'),
    (None,    np.log10,  '(mileage, log groove)'),
    (np.log10, np.log10, '(log mileage, log groove)'),
]

# Tabela de R²
print("\n" + "="*60)
print("COMPARAÇÃO DAS 9 TRANSFORMAÇÕES")
print("="*60)
resultados = []
for tx, ty, titulo in pares:
    x_t = tx(x) if tx else x
    y_t = ty(y) if ty else y
    mask = np.isfinite(x_t) & np.isfinite(y_t)
    x_t, y_t = x_t[mask], y_t[mask]
    mod = smf.ols('Y ~ X', data=pd.DataFrame({'X': x_t, 'Y': y_t})).fit()
    resultados.append({'Transformação': titulo, 'R²_adj': round(mod.rsquared_adj, 4)})

res_df = pd.DataFrame(resultados).sort_values('R²_adj', ascending=False)
print(res_df.to_string(index=False))

# Gráfico das 9
fig, axes = plt.subplots(3, 3, figsize=(15, 13))
axes = axes.flatten()
for i, (tx, ty, titulo) in enumerate(pares):
    x_t = tx(x) if tx else x
    y_t = ty(y) if ty else y
    mask = np.isfinite(x_t) & np.isfinite(y_t)
    x_t, y_t = x_t[mask], y_t[mask]
    r_t = np.corrcoef(x_t, y_t)[0, 1]
    axes[i].scatter(x_t, y_t, alpha=0.8, color='steelblue', edgecolors='white', s=60)
    axes[i].set_title(f'{titulo}\nr = {r_t:.3f}', fontsize=10, fontweight='bold')
    axes[i].grid(True, alpha=0.3)
plt.suptitle('Treadwear — 9 Transformações', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('fig_04_transformacoes_treadwear.png', dpi=150, bbox_inches='tight')
plt.show()

print("\n>>> Arquivos de figura salvos em guia/fig_0X_*.png")
print(">>> Identifique qual transformação linearizou melhor e ajuste TX_MELHOR/TY_MELHOR no 04_codigo_referencia.py")
