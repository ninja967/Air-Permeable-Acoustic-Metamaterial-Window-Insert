import matplotlib.pyplot as plt
import numpy as np

# Create clean, high-resolution conceptual graphic
fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
ax.set_facecolor('#F8FAFC')
fig.patch.set_facecolor('#F8FAFC')

# Draw bounding box for insert
ax.add_patch(plt.Rectangle((3.5, 0.5), 3.0, 5.0, facecolor='#E2E8F0', edgecolor='#475569', lw=2.5, zorder=2))

# Central Airway
ax.add_patch(plt.Rectangle((3.5, 2.0), 3.0, 2.0, facecolor='#E0F2FE', edgecolor='#0284C7', lw=2.0, zorder=3))

# Side Labyrinth Chambers
ax.add_patch(plt.Rectangle((3.5, 4.0), 3.0, 1.5, facecolor='#FEF3C7', edgecolor='#D97706', lw=1.5, zorder=3))
ax.add_patch(plt.Rectangle((3.5, 0.5), 3.0, 1.5, facecolor='#FEF3C7', edgecolor='#D97706', lw=1.5, zorder=3))

# Baffles in top chamber
ax.plot([4.2, 4.2], [4.0, 5.1], color='#B45309', lw=3.0, zorder=4)
ax.plot([5.0, 5.0], [5.5, 4.4], color='#B45309', lw=3.0, zorder=4)
ax.plot([5.8, 5.8], [4.0, 5.1], color='#B45309', lw=3.0, zorder=4)

# Baffles in bottom chamber
ax.plot([4.2, 4.2], [0.9, 2.0], color='#B45309', lw=3.0, zorder=4)
ax.plot([5.0, 5.0], [0.5, 1.6], color='#B45309', lw=3.0, zorder=4)
ax.plot([5.8, 5.8], [0.9, 2.0], color='#B45309', lw=3.0, zorder=4)

# Airflow Arrow (Straight blue arrow)
ax.annotate('', xy=(8.5, 3.0), xytext=(0.8, 3.0),
            arrowprops=dict(arrowstyle="->", color='#0284C7', lw=4.0), zorder=5)
ax.text(1.2, 3.3, "Continuous Fresh Airflow", color='#0369A1', fontsize=12, fontweight='bold', zorder=6)
ax.text(8.7, 3.0, "Fresh Air Indoors\n(Zero Energy Breeze)", color='#0369A1', fontsize=11, fontweight='bold', va='center', zorder=6)

# Incident Sound Wave (Orange sine wave on left)
x_in = np.linspace(0.8, 3.4, 200)
y_in = 3.0 + 0.6 * np.sin(2 * np.pi * 2.0 * x_in)
ax.plot(x_in, y_in, color='#EA580C', lw=2.5, linestyle='-', zorder=6)
ax.text(0.8, 4.2, "Incoming Urban Noise\n(75 - 85 dB Traffic)", color='#C2410C', fontsize=11, fontweight='bold', zorder=6)

# Sound splitting arrows
ax.annotate('', xy=(3.8, 4.6), xytext=(3.4, 3.3),
            arrowprops=dict(arrowstyle="->", color='#D97706', lw=2.2, linestyle='--'), zorder=5)
ax.annotate('', xy=(3.8, 1.4), xytext=(3.4, 2.7),
            arrowprops=dict(arrowstyle="->", color='#D97706', lw=2.2, linestyle='--'), zorder=5)

# Labyrinth delay annotation
ax.text(5.0, 5.65, "Coiled Path: Half-Wavelength Path Delay", color='#92400E', fontsize=9.5, fontweight='bold', ha='center', zorder=6)
ax.text(5.0, 0.15, "Sound Waves Fold & Invert Phase by 180°", color='#92400E', fontsize=9.5, fontweight='bold', ha='center', zorder=6)

# Superposition / Cancellation on Right
x_out = np.linspace(6.6, 8.5, 150)
y_w1 = 3.0 + 0.5 * np.sin(2 * np.pi * 2.0 * x_out)
y_w2 = 3.0 - 0.5 * np.sin(2 * np.pi * 2.0 * x_out)
ax.plot(x_out, y_w1, color='#0284C7', lw=1.8, linestyle=':', alpha=0.7, label='Direct Wave')
ax.plot(x_out, y_w2, color='#D97706', lw=1.8, linestyle='--', alpha=0.7, label='Delayed Wave')

# Resulting flat cancelled line
ax.plot([6.6, 8.5], [3.0, 3.0], color='#16A34A', lw=3.5, zorder=7)
ax.text(8.7, 4.1, "Destructive Interference:\nCrest + Trough = Silence!\n(> 30 dB Attenuation)", 
        color='#15803D', fontsize=11, fontweight='bold', va='center', zorder=6)

# Labels inside blocks
ax.text(5.0, 3.0, "Open Airway Core\n(33.3% Open)", color='#0369A1', fontsize=10, fontweight='bold', ha='center', va='center', zorder=6)

ax.set_xlim(0.5, 11.5)
ax.set_ylim(-0.2, 6.2)
ax.axis('off')

plt.tight_layout()
plt.savefig('concept_how_it_works.png', bbox_inches='tight', dpi=300)
print("Saved concept_how_it_works.png")
