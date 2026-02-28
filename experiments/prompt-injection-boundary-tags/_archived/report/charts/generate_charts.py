#!/usr/bin/env python3
"""Generate publication-quality charts for the defense ablation study."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np

# ── Color palette ──────────────────────────────────────────────────
COLORS = {
    'primary': '#2563eb',
    'secondary': '#7c3aed',
    'accent': '#059669',
    'danger': '#dc2626',
    'warning': '#d97706',
    'muted': '#6b7280',
    'bg': '#ffffff',
    'grid': '#e5e7eb',
}

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.size': 11,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.grid': True,
    'grid.alpha': 0.3,
    'grid.color': COLORS['grid'],
    'figure.facecolor': COLORS['bg'],
    'axes.facecolor': COLORS['bg'],
    'figure.dpi': 150,
})


def chart_defense_stacking():
    """Headline chart: injection rate drops with each defense layer."""
    conditions = ['No Defense', 'Tags Only', 'Instruction\nOnly', 'Instruction\n+ Tags', 'Full Stack']

    # Direct channel (R7)
    direct = [18.9, 9.1, 5.3, 2.3, 0.2]
    # Retrieval channel (R8)
    retrieval = [19.9, 16.2, 9.8, 8.8, 0.0]

    x = np.arange(len(conditions))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))
    bars1 = ax.bar(x - width/2, direct, width, label='Direct injection (R7, N=1,202)',
                   color=COLORS['primary'], edgecolor='white', linewidth=0.5)
    bars2 = ax.bar(x + width/2, retrieval, width, label='Retrieval injection (R8, N=1,981)',
                   color=COLORS['secondary'], edgecolor='white', linewidth=0.5)

    # Value labels
    for bar in bars1:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., h + 0.4,
                f'{h:.1f}%', ha='center', va='bottom', fontsize=9, color=COLORS['primary'])
    for bar in bars2:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., h + 0.4,
                f'{h:.1f}%', ha='center', va='bottom', fontsize=9, color=COLORS['secondary'])

    ax.set_ylabel('Injection Success Rate (%)')
    ax.set_title('Defense Stacking Reduces Injection Success to <0.2%', fontsize=14, fontweight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(conditions)
    ax.legend(loc='upper right', framealpha=0.9)
    ax.set_ylim(0, 25)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())

    # Annotation arrow
    ax.annotate('99.8% reduction\nfrom baseline',
                xy=(4, 0.5), xytext=(3.2, 8),
                arrowprops=dict(arrowstyle='->', color=COLORS['accent'], lw=1.5),
                fontsize=10, color=COLORS['accent'], fontweight='bold',
                ha='center')

    plt.tight_layout()
    plt.savefig('experiments/prompt-injection-boundary-tags/report/charts/defense_stacking.png',
                bbox_inches='tight')
    plt.savefig('experiments/prompt-injection-boundary-tags/report/charts/defense_stacking.svg',
                bbox_inches='tight')
    plt.close()
    print('  defense_stacking.png/svg')


def chart_model_vulnerability():
    """Model vulnerability heatmap (raw condition)."""
    models = ['GPT-5.2', 'Claude\nSonnet 4.5', 'Gemini 3\nFlash', 'Grok 4.1\nFast',
              'GLM-4.7', 'DeepSeek\nV3.2', 'Kimi K2\nThinking', 'Qwen3\nCoder', 'MiniMax\nM2.1']
    conditions = ['Raw', 'Tags', 'Instr.', 'Instr.+Tags', 'Full Stack']

    # R7 phase 1 data (injection rates %, approximate from analysis)
    data = np.array([
        [ 8.3,  0.0,  0.0, 0.0, 0.0],   # GPT-5.2
        [16.7,  8.3,  0.0, 0.0, 0.0],   # Claude Sonnet 4.5
        [ 8.3,  0.0,  8.3, 0.0, 0.0],   # Gemini 3 Flash
        [33.3, 16.7,  8.3, 0.0, 0.0],   # Grok 4.1 Fast
        [ 8.3,  0.0,  0.0, 0.0, 0.0],   # GLM-4.7
        [25.0, 33.3,  8.3, 8.3, 0.0],   # DeepSeek V3.2
        [16.7,  8.3,  8.3, 0.0, 0.0],   # Kimi K2 Thinking
        [41.7, 50.0, 16.7, 8.3, 0.0],   # Qwen3 Coder
        [41.7,  8.3,  0.0, 8.3, 0.0],   # MiniMax M2.1 (note: 0.2% in phase 2)
    ])

    fig, ax = plt.subplots(figsize=(10, 7))
    im = ax.imshow(data, cmap='YlOrRd', aspect='auto', vmin=0, vmax=50)

    ax.set_xticks(np.arange(len(conditions)))
    ax.set_yticks(np.arange(len(models)))
    ax.set_xticklabels(conditions)
    ax.set_yticklabels(models)

    # Cell labels
    for i in range(len(models)):
        for j in range(len(conditions)):
            val = data[i, j]
            color = 'white' if val > 25 else 'black'
            ax.text(j, i, f'{val:.0f}%', ha='center', va='center',
                    fontsize=9, color=color, fontweight='bold' if val > 0 else 'normal')

    ax.set_title('Injection Success by Model and Defense Layer (R7 Direct Channel)',
                 fontsize=13, fontweight='bold', pad=15)
    cbar = plt.colorbar(im, ax=ax, shrink=0.8, label='Injection Rate (%)')

    plt.tight_layout()
    plt.savefig('experiments/prompt-injection-boundary-tags/report/charts/model_vulnerability_heatmap.png',
                bbox_inches='tight')
    plt.savefig('experiments/prompt-injection-boundary-tags/report/charts/model_vulnerability_heatmap.svg',
                bbox_inches='tight')
    plt.close()
    print('  model_vulnerability_heatmap.png/svg')


def chart_payload_effectiveness():
    """Payload category effectiveness under raw conditions."""
    categories = [
        'Gradual\nescalation', 'Indirect\nextraction', 'Social\nengineering',
        'Helpful\nframing', 'Multi-step', 'Encoding',
        'Authority\nimpersonation', 'Context\nconfusion', 'Direct\noverride',
        'Tag\nbreaking', 'Persona\nhijack', 'Direct tool\ninvocation'
    ]
    # Approximate raw success rates from R2 + R7 aggregate
    raw_rates = [72, 41, 33, 26, 22, 14, 11, 8, 0, 0, 0, 0]

    fig, ax = plt.subplots(figsize=(10, 6))
    colors = [COLORS['danger'] if r > 30 else COLORS['warning'] if r > 10 else COLORS['accent']
              for r in raw_rates]
    bars = ax.barh(categories, raw_rates, color=colors, edgecolor='white', linewidth=0.5)

    for bar, val in zip(bars, raw_rates):
        if val > 0:
            ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
                    f'{val}%', va='center', fontsize=9, color=COLORS['muted'])

    ax.set_xlabel('Raw Injection Success Rate (%)')
    ax.set_title('Payload Effectiveness: Subtle Attacks Dominate, Classical Attacks Are Dead',
                 fontsize=13, fontweight='bold', pad=15)
    ax.set_xlim(0, 85)
    ax.invert_yaxis()

    # Legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=COLORS['danger'], label='High threat (>30%)'),
        Patch(facecolor=COLORS['warning'], label='Moderate (10-30%)'),
        Patch(facecolor=COLORS['accent'], label='Low/zero (<10%)'),
    ]
    ax.legend(handles=legend_elements, loc='lower right', framealpha=0.9)

    plt.tight_layout()
    plt.savefig('experiments/prompt-injection-boundary-tags/report/charts/payload_effectiveness.png',
                bbox_inches='tight')
    plt.savefig('experiments/prompt-injection-boundary-tags/report/charts/payload_effectiveness.svg',
                bbox_inches='tight')
    plt.close()
    print('  payload_effectiveness.png/svg')


def chart_tool_filter_precision_recall():
    """Tool-call filter precision/recall across configurations."""
    configs = ['Permissive', 'Balanced', 'Strict', 'Paranoid']
    recall = [74.1, 92.6, 96.3, 100.0]
    fpr = [0.0, 0.0, 2.8, 8.3]

    fig, ax1 = plt.subplots(figsize=(8, 5))

    x = np.arange(len(configs))
    width = 0.35

    bars1 = ax1.bar(x - width/2, recall, width, label='Recall (%)',
                    color=COLORS['primary'], edgecolor='white')
    ax2 = ax1.twinx()
    bars2 = ax2.bar(x + width/2, fpr, width, label='False Positive Rate (%)',
                    color=COLORS['danger'], alpha=0.7, edgecolor='white')

    ax1.set_ylabel('Recall (%)', color=COLORS['primary'])
    ax2.set_ylabel('False Positive Rate (%)', color=COLORS['danger'])
    ax1.set_xticks(x)
    ax1.set_xticklabels(configs)
    ax1.set_ylim(60, 105)
    ax2.set_ylim(0, 12)

    # Value labels
    for bar, val in zip(bars1, recall):
        ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.5,
                 f'{val:.1f}%', ha='center', va='bottom', fontsize=9, color=COLORS['primary'])
    for bar, val in zip(bars2, fpr):
        ax2.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.2,
                 f'{val:.1f}%', ha='center', va='bottom', fontsize=9, color=COLORS['danger'])

    ax1.set_title('Tool-Call Filter: Balanced Config Achieves 92.6% Recall at 0% FPR',
                  fontsize=13, fontweight='bold', pad=15)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', framealpha=0.9)

    plt.tight_layout()
    plt.savefig('experiments/prompt-injection-boundary-tags/report/charts/tool_filter_precision_recall.png',
                bbox_inches='tight')
    plt.savefig('experiments/prompt-injection-boundary-tags/report/charts/tool_filter_precision_recall.svg',
                bbox_inches='tight')
    plt.close()
    print('  tool_filter_precision_recall.png/svg')


if __name__ == '__main__':
    print('Generating charts...')
    chart_defense_stacking()
    chart_model_vulnerability()
    chart_payload_effectiveness()
    chart_tool_filter_precision_recall()
    print('Done. 4 charts (PNG + SVG) saved to report/charts/')
