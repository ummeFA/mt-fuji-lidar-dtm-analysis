import numpy as np
import rasterio
import matplotlib.pyplot as plt

SLOPE_FILE = "TIFF/slope_05m.tif"
CHART_FILE = "figures/slope_stats.png"

with rasterio.open(SLOPE_FILE) as src:
    slope = src.read(1).astype("float64")
    nodata = src.nodata
    pixel_area = abs(src.res[0] * src.res[1])

valid = np.isfinite(slope)
if nodata is not None:
    valid &= slope != nodata
values = slope[valid]

classes = [
    ("0-15 (gentle)", 0, 15, "#91cf60"),
    ("15-30 (moderate)", 15, 30, "#fee08b"),
    ("30-45 (steep)", 30, 45, "#fc8d59"),
    ("over 45 (very steep)", 45, 90.1, "#d73027"),
]

total = values.size
print("Area:", round(total * pixel_area / 1e6, 2), "km2")

labels, shares, colors = [], [], []
for name, low, high, color in classes:
    count = np.count_nonzero((values >= low) & (values < high))
    share = 100 * count / total
    print(name, ":", round(share, 1), "%")
    labels.append(name)
    shares.append(share)
    colors.append(color)

print("Mean slope:", round(values.mean(), 1), "degrees")

plt.figure(figsize=(7, 4))
plt.bar(labels, shares, color=colors, edgecolor="black")
plt.ylabel("Share of area (%)")
plt.title("Slope classes, Mt. Fuji summit area")
plt.tight_layout()
plt.savefig(CHART_FILE, dpi=150)
print("Chart saved")