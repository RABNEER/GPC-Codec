"""
Generate Publication-Quality Scientific Figures for BC-DNA Research Paper
=========================================================================
Adheres strictly to the Matplotlib Expert Skill guidelines:
- Object-oriented API (fig, ax)
- High resolution (300 DPI, bbox_inches='tight')
- Colorblind-friendly, publication-standard palette
- Clear annotations, units, and self-contained captions
"""

import os
import sys
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Set global publication styling
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['grid.color'] = '#cccccc'
plt.rcParams['grid.linestyle'] = '--'
plt.rcParams['grid.alpha'] = 0.5

# Colors: Colorblind friendly
C_BCDNA = '#1f77b4'    # Deep Blue
C_GOLDMAN = '#ff7f0e'  # Orange
C_NAIVE = '#d62728'    # Red
C_ACCENT = '#2ca02c'   # Green

def load_data():
    results_path = os.path.join(os.path.dirname(__file__), 'benchmark_results.json')
    with open(results_path, 'r') as f:
        return json.load(f)

def plot_fig1_biological_compliance(data, out_dir):
    """Figure 1: Homopolymer Length Distribution & GC-Content Stability."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5), constrained_layout=True)
    
    # Panel A: Homopolymer Run Lengths on Structured Telemetry Payload
    telem = data['experiment_1_physical_compliance']['telemetry']
    
    # Extract distributions
    runs = list(range(1, 10))
    naive_counts = [telem['Naive Direct 2-bit']['homopolymer_distribution'].get(str(r), 0) for r in runs]
    gold_counts = [telem['Goldman 2013 (Nature)']['homopolymer_distribution'].get(str(r), 0) for r in runs]
    bcdna_counts = [telem['BC-DNA (Proposed)']['homopolymer_distribution'].get(str(r), 0) for r in runs]
    
    x = np.arange(len(runs))
    w = 0.28
    
    ax1.bar(x - w, naive_counts, width=w, label='Naive Direct (2.0 b/nt)', color=C_NAIVE, alpha=0.85, edgecolor='black', lw=0.6)
    ax1.bar(x, gold_counts, width=w, label='Goldman 2013 (1.33 b/nt)', color=C_GOLDMAN, alpha=0.85, edgecolor='black', lw=0.6)
    ax1.bar(x + w, bcdna_counts, width=w, label='BC-DNA [Ours] (1.45 b/nt)', color=C_BCDNA, alpha=0.9, edgecolor='black', lw=0.6)
    
    ax1.set_yscale('log')
    ax1.set_xlabel('Homopolymer Run Length $L$ (nucleotides)', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Frequency (log scale)', fontsize=11, fontweight='bold')
    ax1.set_title('(A) Homopolymer Run-Length Distribution (Telemetry)', fontsize=12, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels([f'$L={r}$' for r in runs])
    ax1.axvline(1.5, color='gray', linestyle=':', lw=1.2)
    ax1.text(1.6, 1e3, r'Nanopore Stutter Threshold' + '\n' + r'($L \geq 3$ triggers deletions)', fontsize=8.5, color='#444444', style='italic')
    ax1.legend(frameon=True, facecolor='white', framealpha=0.9, fontsize=9)
    ax1.grid(True, which='both', axis='y')

    # Panel B: GC Content across 4 diverse payloads
    payload_names = ['Structured Text', 'Random Binary', 'Science Emblem', 'Telemetry Stream']
    keys = ['text', 'random_binary', 'image_emblem', 'telemetry']
    
    naive_gc = [data['experiment_1_physical_compliance'][k]['Naive Direct 2-bit']['gc_percentage'] for k in keys]
    gold_gc = [data['experiment_1_physical_compliance'][k]['Goldman 2013 (Nature)']['gc_percentage'] for k in keys]
    bcdna_gc = [data['experiment_1_physical_compliance'][k]['BC-DNA (Proposed)']['gc_percentage'] for k in keys]
    
    x2 = np.arange(len(keys))
    ax2.plot(x2, naive_gc, marker='s', markersize=7, lw=2, color=C_NAIVE, label='Naive Direct')
    ax2.plot(x2, gold_gc, marker='^', markersize=7, lw=2, color=C_GOLDMAN, label='Goldman 2013')
    ax2.plot(x2, bcdna_gc, marker='o', markersize=8, lw=2.5, color=C_BCDNA, label='BC-DNA [Ours]')
    
    # Wet-Lab stability zone [40% - 60%]
    ax2.axhspan(40, 60, color='#2ca02c', alpha=0.12, label='Wet-Lab Viable Window (40–60%)')
    ax2.axhline(50, color='gray', linestyle='--', lw=1, alpha=0.7)
    
    ax2.set_xlabel('Payload Type', fontsize=11, fontweight='bold')
    ax2.set_ylabel('GC Content (%)', fontsize=11, fontweight='bold')
    ax2.set_title('(B) GC-Content Stability Across Diverse Payloads', fontsize=12, fontweight='bold')
    ax2.set_xticks(x2)
    ax2.set_xticklabels(payload_names, rotation=15, ha='right', fontsize=9.5)
    ax2.set_ylim(15, 75)
    ax2.legend(loc='lower left', frameon=True, facecolor='white', framealpha=0.9, fontsize=9)
    ax2.grid(True)
    
    out_file = os.path.join(out_dir, 'fig1_biological_compliance.png')
    fig.savefig(out_file, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"[+] Saved {out_file}")

def plot_fig2_nanopore_noise_sweep(data, out_dir):
    """Figure 2: Byte Error Rate vs. Oxford Nanopore Sequencing Noise."""
    sweep = data['experiment_2_nanopore_noise_sweep']
    
    noise = [row['noise_scaling'] for row in sweep]
    naive_ber = [row['codecs']['Naive Direct 2-bit']['mean_ber'] * 100 for row in sweep]
    gold_ber = [row['codecs']['Goldman 2013 (Nature)']['mean_ber'] * 100 for row in sweep]
    bc_ber = [row['codecs']['BC-DNA (Proposed)']['mean_ber'] * 100 for row in sweep]
    resyncs = [row['codecs']['BC-DNA (Proposed)']['mean_resyncs'] for row in sweep]

    fig, ax1 = plt.subplots(figsize=(8, 5), constrained_layout=True)

    # Primary axis: BER
    l1 = ax1.plot(noise, naive_ber, marker='s', lw=2.2, color=C_NAIVE, label='Naive Direct (2.0 b/nt)')
    l2 = ax1.plot(noise, gold_ber, marker='^', lw=2.2, color=C_GOLDMAN, label='Goldman 2013 (1.33 b/nt)')
    l3 = ax1.plot(noise, bc_ber, marker='o', lw=2.8, color=C_BCDNA, label='BC-DNA [Ours] (1.45 b/nt)')

    ax1.set_xlabel(r'Oxford Nanopore Physical Noise Scaling ($\epsilon$)', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Byte Error Rate (BER, %)', fontsize=11, fontweight='bold')
    ax1.set_title('Nanopore Sequencing Noise Sweep: Coordinate Drift vs Confinement', fontsize=12, fontweight='bold')
    ax1.set_ylim(-2, 105)
    ax1.grid(True)

    # Secondary axis: Resynchronization count for BC-DNA
    ax2 = ax1.twinx()
    l4 = ax2.plot(noise, resyncs, marker='d', lw=1.8, color=C_ACCENT, linestyle='-.', label='BC-DNA Drift Resyncs')
    ax2.set_ylabel(r'Active Frame Resynchronizations ($N_{sync}$)', fontsize=11, fontweight='bold', color=C_ACCENT)
    ax2.tick_params(axis='y', labelcolor=C_ACCENT)
    ax2.set_ylim(-5, 260)

    # Combine legends
    lines = l1 + l2 + l3 + l4
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='center right', frameon=True, facecolor='white', framealpha=0.9, fontsize=9.5)

    # Add explanatory annotation
    ax1.annotate(r'Catastrophic Desync (BER > 90% at $\epsilon = 0.25$)', 
                 xy=(0.25, 91.4), xytext=(0.45, 80),
                 arrowprops=dict(facecolor='#333333', arrowstyle='->', lw=1.2),
                 fontsize=8.5, fontweight='bold',
                 bbox=dict(boxstyle='round,pad=0.4', facecolor='#fff2f2', edgecolor='#d62728', lw=1))

    out_file = os.path.join(out_dir, 'fig2_nanopore_noise_sweep.png')
    fig.savefig(out_file, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"[+] Saved {out_file}")

def plot_fig3_burst_deletion_confinement(data, out_dir):
    """Figure 3: Localized Burst Deletion Stress Test & Operational Envelope."""
    burst_data = data['experiment_3_burst_deletion_stress']
    
    burst_nt = [row['burst_nt'] for row in burst_data]
    naive_ber = [row['codecs']['Naive Direct 2-bit']['mean_ber'] * 100 for row in burst_data]
    gold_ber = [row['codecs']['Goldman 2013 (Nature)']['mean_ber'] * 100 for row in burst_data]
    bc_ber = [row['codecs']['BC-DNA (Proposed)']['mean_ber'] * 100 for row in burst_data]

    fig, ax = plt.subplots(figsize=(8.5, 5), constrained_layout=True)

    ax.plot(burst_nt, naive_ber, marker='s', lw=2.2, color=C_NAIVE, label='Naive Direct')
    ax.plot(burst_nt, gold_ber, marker='^', lw=2.2, color=C_GOLDMAN, label='Goldman 2013')
    ax.plot(burst_nt, bc_ber, marker='o', lw=2.8, color=C_BCDNA, label='BC-DNA [Ours]')

    # Highlight operational envelope boundary (W = 12 nt)
    ax.axvspan(0, 12, color='#e6f2ff', alpha=0.6, label=r'Operational Window ($b \leq W = 12$ nt)')
    ax.axvline(12, color='#004c99', linestyle='--', lw=1.5)
    
    ax.annotate('Mathematical Slip Boundary $W = 12$ nt\n(Search window capacity limit)', 
                 xy=(12, 50), xytext=(14.5, 45),
                 arrowprops=dict(facecolor='#004c99', arrowstyle='->', lw=1.5),
                 fontsize=9, fontweight='bold', color='#004c99',
                 bbox=dict(boxstyle='round,pad=0.4', facecolor='#e6f2ff', edgecolor='#004c99', lw=1))

    ax.set_xlabel('Burst Deletion Length $b$ (contiguous nucleotides)', fontsize=11, fontweight='bold')
    ax.set_ylabel('Byte Error Rate (BER, %)', fontsize=11, fontweight='bold')
    ax.set_title('Burst Deletion Resilience: Confinement vs Breakdown Boundary', fontsize=12, fontweight='bold')
    ax.set_xlim(-0.5, 30.5)
    ax.set_ylim(-3, 105)
    ax.legend(loc='center left', frameon=True, facecolor='white', framealpha=0.9, fontsize=9.5)
    ax.grid(True)

    out_file = os.path.join(out_dir, 'fig3_burst_deletion_confinement.png')
    fig.savefig(out_file, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"[+] Saved {out_file}")

def plot_fig4_visual_image_recovery(out_dir):
    """Figure 4: Visual 32x32 Science Emblem Recovery under Burst Deletion (b = 6 nt)."""
    import random
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
    from dna_codec.codec import BCDNACodec, NaiveDirectCodec, GoldmanNature2013Codec
    
    # 1. Generate 32x32 emblem
    dim = 32
    emblem = np.zeros((dim, dim), dtype=np.uint8)
    for r in range(dim):
        for c in range(dim):
            dx = c - 15.5
            dy = r - 15.5
            dist = (dx*dx + dy*dy)**0.5
            if (13.0 <= dist <= 15.0) or (dist <= 3.5) or (abs(dx) <= 0.8 and 4.0 <= abs(dy) <= 12.0) or (abs(dy) <= 0.8 and 4.0 <= abs(dx) <= 12.0):
                emblem[r, c] = 1
                
    raw_bytes = bytearray(128)
    for r in range(dim):
        for c in range(dim):
            if emblem[r, c]:
                b_idx = (r * dim + c) // 8
                bit_idx = (r * dim + c) % 8
                raw_bytes[b_idx] |= (1 << (7 - bit_idx))
    raw_bytes = bytes(raw_bytes)
    
    # Encode with all 3
    bc = BCDNACodec(block_size_bytes=16)
    naive = NaiveDirectCodec()
    gold = GoldmanNature2013Codec()
    
    dna_bc = bc.encode(raw_bytes)
    dna_naive = naive.encode(raw_bytes)
    dna_gold = gold.encode(raw_bytes)
    
    # Inject 6 nt deletion at pos 100
    burst = 6
    cut = 100
    dna_bc_corrupt = dna_bc[:cut] + dna_bc[cut + burst:]
    dna_naive_corrupt = dna_naive[:cut] + dna_naive[cut + burst:]
    dna_gold_corrupt = dna_gold[:cut] + dna_gold[cut + burst:]
    
    # Decode
    rec_bc, _, _ = bc.decode(dna_bc_corrupt, len(raw_bytes))
    rec_naive = naive.decode(dna_naive_corrupt, len(raw_bytes))
    rec_gold = gold.decode(dna_gold_corrupt, len(raw_bytes))
    
    def bytes_to_img(b_data):
        img = np.zeros((dim, dim), dtype=np.uint8)
        for r in range(dim):
            for c in range(dim):
                b_idx = (r * dim + c) // 8
                bit_idx = (r * dim + c) % 8
                if b_idx < len(b_data):
                    val = (b_data[b_idx] >> (7 - bit_idx)) & 1
                    img[r, c] = val
        return img
        
    img_orig = emblem
    img_naive = bytes_to_img(rec_naive)
    img_gold = bytes_to_img(rec_gold)
    img_bc = bytes_to_img(rec_bc)
    
    # Compute error rates
    ber_naive = np.mean(img_orig != img_naive) * 100
    ber_gold = np.mean(img_orig != img_gold) * 100
    ber_bc = np.mean(img_orig != img_bc) * 100
    
    fig, axes = plt.subplots(1, 4, figsize=(12, 3.5), constrained_layout=True)
    
    panels = [
        (img_orig, '(A) Original Ground Truth\n(1,024 bits / 128 bytes)', '#2ca02c', 'BER: 0.0%'),
        (img_naive, f'(B) Naive Direct (2.0 b/nt)\nCorrupted (b = 6 nt)', '#d62728', f'BER: {ber_naive:.1f}%\nTotal Coordinate Desync'),
        (img_gold, f'(C) Goldman 2013 (1.33 b/nt)\nCorrupted (b = 6 nt)', '#ff7f0e', f'BER: {ber_gold:.1f}%\nTotal Coordinate Desync'),
        (img_bc, f'(D) BC-DNA [Ours] (1.45 b/nt)\nCorrupted (b = 6 nt)', '#1f77b4', f'BER: {ber_bc:.1f}%\nConfined to Block 1')
    ]
    
    for ax, (im_data, title, col, stats_txt) in zip(axes, panels):
        ax.imshow(im_data, cmap='gray_r', interpolation='nearest')
        ax.set_title(title, fontsize=10.5, fontweight='bold', color=col)
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_edgecolor(col)
            spine.set_linewidth(1.8)
        ax.text(0.5, -0.18, stats_txt, transform=ax.transAxes, ha='center', fontsize=9, fontweight='bold', color='#333333')

    out_file = os.path.join(out_dir, 'fig4_visual_image_recovery.png')
    fig.savefig(out_file, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"[+] Saved {out_file}")

def main():
    out_dir = os.path.join(os.path.dirname(__file__), '..', 'figures')
    os.makedirs(out_dir, exist_ok=True)
    data = load_data()
    
    print("Generating publication-ready figures...")
    plot_fig1_biological_compliance(data, out_dir)
    plot_fig2_nanopore_noise_sweep(data, out_dir)
    plot_fig3_burst_deletion_confinement(data, out_dir)
    plot_fig4_visual_image_recovery(out_dir)
    print("All figures successfully generated at 300 DPI.")

if __name__ == '__main__':
    main()
