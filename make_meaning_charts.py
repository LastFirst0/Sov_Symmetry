from pathlib import Path
import matplotlib.pyplot as plt

out = Path('/home/ubuntu/projects/sov-e4e91854')
labels = ['Markdown\ndocs', 'Python\nfiles', 'Rust\nfiles', 'Lean\nfiles', 'Attached\nexplorers']
values = [307, 907, 31, 7, 10]
colors = ['#4C78A8', '#F58518', '#54A24B', '#B279A2', '#E45756']

plt.style.use('seaborn-v0_8-whitegrid')
fig, ax = plt.subplots(figsize=(10, 6), dpi=180)
bars = ax.bar(labels, values, color=colors, width=0.68)
ax.set_title('Sovereign Engine: Source and Embodiment Surface', fontsize=16, weight='bold', pad=14)
ax.set_ylabel('Count of inventoried artifacts')
ax.set_ylim(0, max(values)*1.18)
for b, v in zip(bars, values):
    ax.text(b.get_x()+b.get_width()/2, v+max(values)*0.025, f'{v:,}', ha='center', va='bottom', fontsize=11, weight='bold')
ax.text(0.01, -0.16, 'Counts are inventory observations from the cloned repository and shared attachment directory; they do not measure quality or completion.', transform=ax.transAxes, fontsize=9, color='#444')
fig.tight_layout()
fig.savefig(out/'source_surface_chart.png', bbox_inches='tight')
plt.close(fig)

# Conceptual stack chart, intentionally labeled as a model rather than empirical measurement.
labels2 = ['Meaning\nontology', 'Geometry\nprimitives', 'Inference\nand transforms', 'Verification\nand provenance', 'Interfaces\nand embodiment']
values2 = [1, 5, 4, 4, 6]
colors2 = ['#264653', '#2A9D8F', '#E9C46A', '#F4A261', '#E76F51']
fig, ax = plt.subplots(figsize=(11, 5.8), dpi=180)
bars = ax.barh(labels2, values2, color=colors2)
ax.invert_yaxis()
ax.set_xlim(0, 6.3)
ax.set_xlabel('Representative concept families (not a capability score)')
ax.set_title('Meaning Layer: Five Interlocking Planes', fontsize=16, weight='bold', pad=14)
for b, v in zip(bars, values2):
    ax.text(v+0.08, b.get_y()+b.get_height()/2, str(v), va='center', fontsize=11, weight='bold')
fig.tight_layout()
fig.savefig(out/'meaning_planes_chart.png', bbox_inches='tight')
plt.close(fig)
print('created', out/'source_surface_chart.png', out/'meaning_planes_chart.png')
