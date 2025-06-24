# import pandas as pd
# import matplotlib.pyplot as plt

# def ContingencyTable(data, col1, col2) :
#     return data.groupby([col1, col2]).size().unstack(col1, fill_value = 0)

# df = pd.read_json('data/sensoring_data.json')

# df['category'].value_counts(dropna = True).plot(kind = 'bar')
# plt.savefig('catValCtsBP.png')

# import pandas as pd
# import matplotlib.pyplot as plt
# import os

# # --- Step 1: Set Matplotlib Style to 'classic' ---
# plt.style.use('classic')

# # --- Step 2: Define custom parameters for XP look ---
# # Muted blue/green color for bars, common in XP UI
# xp_bar_color = '#90A4AE' # A muted blue-grey, similar to some XP elements
# xp_edge_color = '#546E7A' # A darker shade for edges, gives slight depth
# xp_bg_color = '#ECEFF1' # Very light grey for the plot area background
# xp_grid_color = '#CFD8DC' # Light grey for grid lines
# xp_font = 'Tahoma' # Common Windows font (ensure it's available on your system)

# # Update rcParams (runtime configuration parameters) for the XP style
# plt.rcParams.update({
#     'figure.facecolor': xp_bg_color,     # Background outside the plot area
#     'axes.facecolor': xp_bg_color,       # Background of the plot area
#     'axes.edgecolor': xp_edge_color,     # Border of the plot area
#     'grid.color': xp_grid_color,
#     'grid.linestyle': '-',
#     'grid.linewidth': 0.8,
#     'font.family': xp_font,
#     'text.color': '#37474F',             # Dark text color
#     'axes.labelcolor': '#37474F',
#     'xtick.color': '#37474F',
#     'ytick.color': '#37474F',
#     'axes.prop_cycle': plt.cycler(color=[xp_bar_color]) # Set the bar color
# })


# def ContingencyTable(data, col1, col2):
#     return data.groupby([col1, col2]).size().unstack(col1, fill_value=0)

# # --- Start of your original script logic ---

# # Ensure the 'data' directory exists for json and output
# # It's good practice to create directories if they don't exist
# output_dir = 'data'
# if not os.path.exists(output_dir):
#     os.makedirs(output_dir)
#     print(f"Created directory: {output_dir}")

# # Attempt to read the JSON file with the absolute path construction
# # This is a robust way to handle the FileNotFoundError
# json_file_path = os.path.join(output_dir, 'sensoring_data.json')

# try:
#     df = pd.read_json(json_file_path)
# except FileNotFoundError:
#     print(f"Error: File not found at {json_file_path}")
#     print("Please ensure 'sensoring_data.json' is in the 'data' folder next to your script.")
#     print("Creating dummy data for demonstration purposes.")
#     # Create dummy DataFrame for demonstration if file is not found
#     data = {
#         'category': ['plastic', 'metal', 'plastic', 'glass', 'other', 'plastic', 'metal'],
#         'temperature': [25, 22, 26, 20, 23, 24, 21]
#     }
#     df = pd.DataFrame(data)

# # --- Plot 1: Category Value Counts Bar Plot ---
# fig1, ax1 = plt.subplots(figsize=(8, 6)) # Create a figure and axes explicitly for more control
# df['category'].value_counts(dropna=True).plot(
#     kind='bar',
#     ax=ax1, # Plot onto the created axes
#     color=xp_bar_color,
#     edgecolor=xp_edge_color,
#     linewidth=1.5 # Thicker edges for more definition
# )
# ax1.set_title('Category Distribution (XP Style)', color='#37474F')
# ax1.set_xlabel('Category', color='#37474F')
# ax1.set_ylabel('Count', color='#37474F')
# ax1.tick_params(axis='x', rotation=0) # Keep labels horizontal
# ax1.grid(axis='y', linestyle='-', alpha=0.7) # Add subtle horizontal grid

# # Adjust axes spines (borders)
# for spine in ax1.spines.values():
#     spine.set_edgecolor(xp_edge_color)
#     spine.set_linewidth(1.5)

# # Save the first plot
# plt.savefig('catValCtsBP_xp_style.png') # Changed filename to reflect XP style

# # --- Plot 2: Contingency Table Plot ---
# dfCatLoc = ContingencyTable(df, 'temperature', 'category')

# fig2, ax2 = plt.subplots(figsize=(10, 7)) # New figure for the second plot
# dfCatLoc.plot(
#     kind='bar',
#     ax=ax2, # Plot onto the new axes
#     color=[xp_bar_color, '#B0BEC5', '#78909C', '#607D8B'], # Use multiple XP-like colors for different bars
#     edgecolor=xp_edge_color,
#     linewidth=1.5
# )
# ax2.set_title('Category by Temperature (XP Style)', color='#37474F')
# ax2.set_xlabel('Category', color='#37474F')
# ax2.set_ylabel('Count', color='#37474F')
# ax2.tick_params(axis='x', rotation=45, ha='right') # Rotate x-labels if needed
# ax2.grid(axis='y', linestyle='-', alpha=0.7)

# # Adjust axes spines (borders)
# for spine in ax2.spines.values():
#     spine.set_edgecolor(xp_edge_color)
#     spine.set_linewidth(1.5)

# # Add a legend for the second plot since it has multiple bars
# ax2.legend(title='Temperature', bbox_to_anchor=(1.05, 1), loc='upper left')
# plt.tight_layout(rect=[0, 0, 0.85, 1]) # Adjust layout for legend

# # Save the second plot
# plt.savefig('catLocCor_xp_style.png') # Changed filename

# plt.show() # Display both plots
# print("Plots generated with XP-like style!")

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