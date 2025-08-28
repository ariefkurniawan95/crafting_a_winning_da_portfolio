import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime, timedelta
import numpy as np

# Read the CSV data
df = pd.read_csv('W:\portofolio_building\demand_forecasting\indomie goreng.csv')

start_date = datetime(2025, 1, 1)  # Adjust this to your actual start date
df['actual_date'] = [start_date + timedelta(days=i) for i in range(len(df))]
df['date_str'] = df['actual_date'].dt.strftime('%Y-%m-%d')

# Set up the figure and axis
fig, ax = plt.subplots(figsize=(12, 8))
fig.patch.set_facecolor('white')

# Style the plot
ax.set_facecolor('#f8f9fa')
ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#cccccc')
ax.spines['bottom'].set_color('#cccccc')

# Initialize empty line objects
line, = ax.plot([], [], linewidth=2.5, color='#ff6b35', alpha=0.8)
scatter = ax.scatter([], [], s=50, color='#ff6b35', alpha=0.7, zorder=5)

# Add styling elements
ax.set_title('Indomie Goreng Sales Over Time', 
             fontsize=16, fontweight='bold', pad=20, color='#2c3e50')
ax.set_xlabel('Date', fontsize=12, color='#34495e', fontweight='600')
ax.set_ylabel('Quantity Sold', fontsize=12, color='#34495e', fontweight='600')

# Set axis limits
ax.set_xlim(0, len(df) - 1)
y_margin = (df['qty'].max() - df['qty'].min()) * 0.1
ax.set_ylim(df['qty'].min() - y_margin, df['qty'].max() + y_margin)

# Create custom x-axis labels (show every 10th date)
tick_positions = list(range(0, len(df), max(1, len(df)//10)))
tick_labels = [df.iloc[i]['date_str'] for i in tick_positions]
ax.set_xticks(tick_positions)
ax.set_xticklabels(tick_labels, rotation=45, ha='right')

# Add statistics text box
stats_text = ax.text(0.02, 0.98, '', transform=ax.transAxes, 
                    verticalalignment='top', fontsize=10,
                    bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8))

# Add current value indicator
current_value_text = ax.text(0.98, 0.98, '', transform=ax.transAxes,
                            verticalalignment='top', horizontalalignment='right',
                            fontsize=12, fontweight='bold',
                            bbox=dict(boxstyle='round,pad=0.5', facecolor='#ff6b35', alpha=0.2))

def animate(frame):
    # Current data up to frame
    current_data = df.iloc[:frame+1]
    
    # Update line plot
    x_data = list(range(len(current_data)))
    y_data = current_data['qty'].tolist()
    
    line.set_data(x_data, y_data)
    
    # Update scatter plot (show only the current point)
    if len(current_data) > 0:
        current_x = len(current_data) - 1
        current_y = current_data.iloc[-1]['qty']
        scatter.set_offsets([[current_x, current_y]])
    
    # Update statistics
    if len(current_data) > 0:
        avg_sales = current_data['qty'].mean()
        max_sales = current_data['qty'].max()
        min_sales = current_data['qty'].min()
        total_sales = current_data['qty'].sum()
        
        stats_text.set_text(f'Statistics (Days 1-{len(current_data)}):\n'
                           f'Total Sales: {total_sales:,.0f}\n'
                           f'Average: {avg_sales:.1f}\n'
                           f'Max: {max_sales}\n'
                           f'Min: {min_sales}')
        
        # Current value indicator
        current_date = current_data.iloc[-1]['date_str']
        current_qty = current_data.iloc[-1]['qty']
        current_value_text.set_text(f'{current_date}\nQty: {current_qty}')
    
    return line, scatter, stats_text, current_value_text

# Create animation
frames = len(df)
anim = animation.FuncAnimation(fig, animate, frames=frames, 
                              interval=100,  # 100ms between frames
                              blit=True, repeat=True)

# Adjust layout to prevent label cutoff
plt.tight_layout()

# Display the animation
plt.show()

print("\n=== Dataset Summary ===")
print(f"Total data points: {len(df)}")
print(f"Date range: {df.iloc[0]['date_str']} to {df.iloc[-1]['date_str']}")
print(f"Total sales: {df['qty'].sum():,}")
print(f"Average daily sales: {df['qty'].mean():.1f}")
print(f"Maximum daily sales: {df['qty'].max()}")
print(f"Minimum daily sales: {df['qty'].min()}")
print(f"Standard deviation: {df['qty'].std():.1f}")