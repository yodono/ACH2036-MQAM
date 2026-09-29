"""
=============================================================================
EP1 — MQAM (ACH2036) — Código de Referência Completo
=============================================================================
Este arquivo contém funções prontas para todas as etapas do EP.
Copie e adapte conforme necessário para cada dataset.

Datasets:
  - treadwear.txt  : X=mileage, Y=groove
  - alligator.txt  : X=length,  Y=weight
  - ConcPatog.txt  : X=CPatog1, Y=CPatog2
=============================================================================
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import scipy.stats as stats
import statsmodels.formula.api as smf
import statsmodels.graphics.gofplots as smgof
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# CONFIGURAÇÃO — MUDE AQUI PARA CADA DATASET
# =============================================================================

# DATASET 1: Treadwear
DATASET_PATH = '../datasets/treadwear.txt'
X_COL = 'mileage'
Y_COL = 'groove'
DATASET_NAME = 'Treadwear'
SEP = '\t'

# DATASET 2: Alligator
# DATASET_PATH = '../datasets/alligator.txt'
# X_COL = 'length'
# Y_COL = 'weight'
# DATASET_NAME = 'Alligator'
# SEP = '\s+'  # espaço(s)

# DATASET 3: ConcPatog
# DATASET_PATH = '../datasets/ConcPatog.txt'
# X_COL = 'CPatog1'
# Y_COL = 'CPatog2'
# DATASET_NAME = 'Concentração de Patógenos'
# SEP = '\t'

# =============================================================================
# CARREGAMENTO E EXPLORAÇÃO
# =============================================================================

df = pd.read_csv(DATASET_PATH, sep=SEP, engine='python')
df = df.dropna(subset=[X_COL, Y_COL])

x = df[X_COL]
y = df[Y_COL]
n = len(df)

print(f"Dataset: {DATASET_NAME}")
print(f"n = {n} observações")
print(f"\nEstatísticas descritivas:")
print(df[[X_COL, Y_COL]].describe())


# =============================================================================
# ETAPA 1: SCATTER PLOT ORIGINAL
# =============================================================================

def plot_scatter(x, y, xlabel, ylabel, title):
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(x, y, alpha=0.7, s=80, color='steelblue', edgecolors='white', linewidth=1.5)
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_title(title, fontsize=13)
    ax.grid(True, alpha=0.3)
    # Mostra correlação
    corr = np.corrcoef(x, y)[0, 1]
    ax.annotate(f'r = {corr:.3f}', xy=(0.05, 0.92), xycoords='axes fraction', fontsize=12,
                bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', alpha=0.8))
    plt.tight_layout()
    plt.show()
    print(f"Correlação de Pearson: r = {corr:.4f}")

plot_scatter(x, y, X_COL, Y_COL, f'Scatter Plot — {DATASET_NAME}\n({Y_COL} vs {X_COL})')


# =============================================================================
# ETAPA 2: AJUSTE DO MODELO
# =============================================================================

# Ajuste
modelo = smf.ols(f'{Y_COL} ~ {X_COL}', data=df).fit()

# Tabela completa (equivalente ao exemplo do professor)
print("\n" + "="*70)
print("TABELA DE RESULTADOS DO AJUSTE")
print("="*70)
print(modelo.summary())

# Extração dos principais valores
b0 = modelo.params['Intercept']
b1 = modelo.params[X_COL]
r2 = modelo.rsquared
r2_adj = modelo.rsquared_adj

print(f"\nEquação da reta: {Y_COL} = {b0:.4f} + {b1:.4f} × {X_COL}")
print(f"R² = {r2:.4f}  |  R² ajustado = {r2_adj:.4f}")


# =============================================================================
# ETAPA 2b: GRÁFICO COM RETA + IC + IP
# =============================================================================

def plot_regression_with_bands(df, modelo, x_col, y_col, title):
    x_range = np.linspace(df[x_col].min(), df[x_col].max(), 200)
    x_pred_df = pd.DataFrame({x_col: x_range})
    
    pred = modelo.get_prediction(x_pred_df)
    pred_df = pred.summary_frame(alpha=0.05)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Pontos
    ax.scatter(df[x_col], df[y_col], alpha=0.7, s=80, color='steelblue',
               edgecolors='white', linewidth=1.5, zorder=5, label='Dados')
    
    # Reta de regressão
    ax.plot(x_range, pred_df['mean'], color='crimson', linewidth=2.5, label='Reta de Regressão')
    
    # Intervalo de Confiança (IC) — para a MÉDIA
    ax.fill_between(x_range, pred_df['mean_ci_lower'], pred_df['mean_ci_upper'],
                    alpha=0.25, color='crimson', label='IC 95% (Média)')
    
    # Intervalo de Predição (IP) — para NOVA OBSERVAÇÃO
    ax.fill_between(x_range, pred_df['obs_ci_lower'], pred_df['obs_ci_upper'],
                    alpha=0.12, color='darkorange', label='IP 95% (Predição)')
    
    ax.set_xlabel(x_col, fontsize=12)
    ax.set_ylabel(y_col, fontsize=12)
    ax.set_title(title, fontsize=13)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
    r2_adj = modelo.rsquared_adj
    ax.annotate(f'R²(adj) = {r2_adj:.3f}', xy=(0.05, 0.92), xycoords='axes fraction',
                fontsize=12, bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', alpha=0.8))
    
    plt.tight_layout()
    plt.show()

plot_regression_with_bands(df, modelo, X_COL, Y_COL,
    f'Regressão com IC e IP — {DATASET_NAME}')


# =============================================================================
# ETAPA 2c: ANÁLISE DE RESÍDUOS (3 gráficos)
# =============================================================================

def plot_residuos(modelo, dataset_name):
    residuos = modelo.resid
    fitted = modelo.fittedvalues
    
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.suptitle(f'Análise de Resíduos — {dataset_name}', fontsize=14, fontweight='bold')
    
    # --- Gráfico 1: Histograma ---
    ax = axes[0]
    ax.hist(residuos, bins='auto', density=True, alpha=0.7, color='steelblue', edgecolor='white')
    x_norm = np.linspace(residuos.min(), residuos.max(), 200)
    ax.plot(x_norm, stats.norm.pdf(x_norm, residuos.mean(), residuos.std()),
            'r-', linewidth=2, label='Normal')
    ax.set_title('Histograma dos Resíduos', fontsize=11)
    ax.set_xlabel('Resíduos')
    ax.set_ylabel('Densidade')
    ax.legend()
    
    # --- Gráfico 2: Resíduos vs. Preditos ---
    ax = axes[1]
    ax.scatter(fitted, residuos, alpha=0.7, color='steelblue', edgecolors='white', s=60)
    ax.axhline(0, color='red', linestyle='--', linewidth=1.5)
    ax.set_title('Resíduos vs. Valores Preditos', fontsize=11)
    ax.set_xlabel('Valores Preditos (ŷ)')
    ax.set_ylabel('Resíduos (e)')
    ax.grid(True, alpha=0.3)
    
    # --- Gráfico 3: QQ-Plot ---
    ax = axes[2]
    smgof.qqplot(residuos, line='s', ax=ax)
    ax.set_title('QQ-Plot dos Resíduos', fontsize=11)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    # Teste de Shapiro-Wilk (normalidade)
    if len(residuos) <= 5000:
        stat, p = stats.shapiro(residuos)
        print(f"\nTeste de Shapiro-Wilk para normalidade dos resíduos:")
        print(f"  W = {stat:.4f}, p-valor = {p:.4f}")
        if p > 0.05:
            print("  → Não rejeitamos normalidade (p > 0.05)")
        else:
            print("  → Rejeitamos normalidade (p <= 0.05)")

plot_residuos(modelo, DATASET_NAME)


# =============================================================================
# ETAPAS 3-4: TESTAR 9 TRANSFORMAÇÕES
# =============================================================================

# ATENÇÃO: Para ConcPatog, use log10(X+1) pois há zeros em CPatog1
# Ajuste a função de log abaixo se necessário:
LOG_OFFSET = 0  # mude para 1 se houver zeros em X ou Y

transformacoes = {
    'raiz':     lambda v: np.sqrt(v),
    'quadrado': lambda v: v**2,
    'log10':    lambda v: np.log10(v + LOG_OFFSET),
}

pares = [
    ('raiz',     None,       f'(√{X_COL}, {Y_COL})'),
    (None,       'raiz',     f'({X_COL}, √{Y_COL})'),
    ('raiz',     'raiz',     f'(√{X_COL}, √{Y_COL})'),
    ('quadrado', None,       f'({X_COL}², {Y_COL})'),
    (None,       'quadrado', f'({X_COL}, {Y_COL}²)'),
    ('quadrado', 'quadrado', f'({X_COL}², {Y_COL}²)'),
    ('log10',    None,       f'(log {X_COL}, {Y_COL})'),
    (None,       'log10',    f'({X_COL}, log {Y_COL})'),
    ('log10',    'log10',    f'(log {X_COL}, log {Y_COL})'),
]

# Tabela de R² para cada transformação
print("\n" + "="*70)
print("COMPARAÇÃO DAS 9 TRANSFORMAÇÕES")
print("="*70)

resultados = []
for tx, ty, titulo in pares:
    x_t = transformacoes[tx](x) if tx else x
    y_t = transformacoes[ty](y) if ty else y
    
    # Remove NaN/inf que podem surgir de log(0) ou sqrt de negativos
    mask = np.isfinite(x_t) & np.isfinite(y_t)
    x_t = x_t[mask]
    y_t = y_t[mask]
    
    temp_df = pd.DataFrame({'X': x_t, 'Y': y_t})
    mod = smf.ols('Y ~ X', data=temp_df).fit()
    
    corr = np.corrcoef(x_t, y_t)[0, 1]
    resultados.append({
        'Transformação': titulo,
        'R²': round(mod.rsquared, 4),
        'R² ajustado': round(mod.rsquared_adj, 4),
        'Correlação (r)': round(corr, 4)
    })

res_df = pd.DataFrame(resultados).sort_values('R² ajustado', ascending=False)
print(res_df.to_string(index=False))

# Scatter plots das 9 transformações
fig, axes = plt.subplots(3, 3, figsize=(15, 13))
axes = axes.flatten()

for i, (tx, ty, titulo) in enumerate(pares):
    x_t = transformacoes[tx](x) if tx else x
    y_t = transformacoes[ty](y) if ty else y
    
    mask = np.isfinite(x_t) & np.isfinite(y_t)
    x_t = x_t[mask]
    y_t = y_t[mask]
    
    corr = np.corrcoef(x_t, y_t)[0, 1]
    axes[i].scatter(x_t, y_t, alpha=0.7, color='steelblue', edgecolors='white', s=50)
    axes[i].set_title(titulo, fontsize=11, fontweight='bold')
    axes[i].set_xlabel(f'r = {corr:.3f}', fontsize=10)
    axes[i].grid(True, alpha=0.3)

plt.suptitle(f'9 Transformações — {DATASET_NAME}', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()


# =============================================================================
# ETAPA 5: MELHOR TRANSFORMAÇÃO — REPETIR ETAPAS 1 e 2
# =============================================================================
# Após identificar a melhor transformação, ajuste abaixo:

# EXEMPLO: se a melhor foi log10 em ambos
TX_MELHOR = 'log10'   # 'raiz', 'quadrado', 'log10', ou None
TY_MELHOR = 'log10'   # 'raiz', 'quadrado', 'log10', ou None

x_best = transformacoes[TX_MELHOR](x) if TX_MELHOR else x
y_best = transformacoes[TY_MELHOR](y) if TY_MELHOR else y

mask = np.isfinite(x_best) & np.isfinite(y_best)
x_best = x_best[mask]
y_best = y_best[mask]

df_best = pd.DataFrame({'X_t': x_best, 'Y_t': y_best})
modelo_best = smf.ols('Y_t ~ X_t', data=df_best).fit()

print("\n" + "="*70)
print(f"MODELO COM MELHOR TRANSFORMAÇÃO: ({TX_MELHOR} {X_COL}, {TY_MELHOR} {Y_COL})")
print("="*70)
print(modelo_best.summary())

# Scatter com reta
plot_scatter(x_best, y_best,
    f'log₁₀({X_COL})' if TX_MELHOR == 'log10' else X_COL,
    f'log₁₀({Y_COL})' if TY_MELHOR == 'log10' else Y_COL,
    f'Scatter Plot Transformado — {DATASET_NAME}')

# Gráfico com reta + IC + IP
plot_regression_with_bands(df_best, modelo_best, 'X_t', 'Y_t',
    f'Regressão Transformada — {DATASET_NAME}')

# Análise de resíduos
plot_residuos(modelo_best, f'{DATASET_NAME} (transformado)')
