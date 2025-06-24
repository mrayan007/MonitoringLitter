import pandas as pd
import matplotlib.pyplot as plt
import os
import matplotlib as mpl

plt.style.use('seaborn-v0_8')

modern_primary_color = '#1E88E5'
modern_text_color = '#212121'
modern_light_grey = '#F5F5F5'
modern_grid_color = '#E0E0E0'


plt.rcParams.update({
    'axes.facecolor': modern_light_grey,
    'figure.facecolor': 'white', 
    'text.color': modern_text_color,
    'axes.labelcolor': modern_text_color,
    'xtick.color': modern_text_color,
    'ytick.color': modern_text_color,
    'axes.edgecolor': modern_grid_color,
    'grid.color': modern_grid_color,
    'grid.linestyle': '-',
    'grid.linewidth': 0.7,
    'axes.titleweight': 'bold',
    'axes.titlesize': 16, 
    'font.size': 10,
})

def ContingencyTable(data, col1, col2):
    return data.groupby([col1, col2]).size().unstack(col1, fill_value=0)


output_dir = 'data'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Created directory: {output_dir}")

json_file_path = os.path.join(output_dir, 'sensoring_data.json')

try:
    df = pd.read_json(json_file_path)
except FileNotFoundError:
    print(f"Error: File not found at {json_file_path}")
    print("Please ensure 'sensoring_data.json' is in the 'data' folder next to your script.")
    print("Creating dummy data for demonstration purposes.")
    data = {
        'category': ['plastic', 'metal', 'plastic', 'glass', 'other', 'plastic', 'metal', 'paper', 'glass'],
        'temperature': [25, 22, 26, 20, 23, 24, 21, 19, 20]
    }
    df = pd.DataFrame(data)

fig1, ax1 = plt.subplots(figsize=(9, 6)) 
df['category'].value_counts(dropna=True).plot(
    kind='bar',
    ax=ax1,
    color=modern_primary_color,
    edgecolor='none'
)
ax1.set_title('Distribution of Litter Categories', pad=20)
ax1.set_xlabel('Category')
ax1.set_ylabel('Count')
ax1.tick_params(axis='x', rotation=0)

ax1.grid(axis='y', linestyle='-', alpha=0.6, color=modern_grid_color)
ax1.grid(axis='x', visible=False)

ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['left'].set_color(modern_grid_color)
ax1.spines['bottom'].set_color(modern_grid_color)
ax1.spines['left'].set_linewidth(0.8)
ax1.spines['bottom'].set_linewidth(0.8)

plt.savefig('catValCtsBP_modern_style.png', dpi=300, bbox_inches='tight')

dfCatLoc = ContingencyTable(df, 'temperature', 'category')

fig2, ax2 = plt.subplots(figsize=(11, 7)) 
import numpy as np
colors = plt.cm.Blues(np.linspace(0.4, 0.9, len(dfCatLoc.columns)))
dfCatLoc.plot(
    kind='bar',
    ax=ax2,
    color=colors,
    edgecolor='none'
)
ax2.set_title('Litter Categories by Temperature', pad=20)
ax2.set_xlabel('Category')
ax2.set_ylabel('Count')
ax2.tick_params(axis='x', rotation=45, ha='right')

ax2.grid(axis='y', linestyle='-', alpha=0.6, color=modern_grid_color)
ax2.grid(axis='x', visible=False)

ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['left'].set_color(modern_grid_color)
ax2.spines['bottom'].set_color(modern_grid_color)
ax2.spines['left'].set_linewidth(0.8)
ax2.spines['bottom'].set_linewidth(0.8)

ax2.legend(title='Temperature', bbox_to_anchor=(1.05, 1), loc='upper left', frameon=False)
plt.tight_layout(rect=[0, 0, 0.85, 1])

plt.savefig('catLocCor_modern_style.png', dpi=300, bbox_inches='tight')

plt.show()
print("Plots generated with cool and modern style!")