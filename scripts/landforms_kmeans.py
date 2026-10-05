import numpy as np
import rasterio
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

N_CLUSTERS = 5

# 1. Read slope and SVF
def read(path):
    with rasterio.open(path) as src:
        data = src.read(1).astype("float64")
        valid = np.isfinite(data)
        if src.nodata is not None:
            valid &= data != src.nodata
        return data, valid, src.profile

slope, valid_slope, profile = read("TIFF/slope_05m.tif")
svf, valid_svf, _ = read("TIFF/svf_05m.tif")

# 2. Keep pixels that are valid in both
valid = valid_slope & valid_svf
features = np.column_stack([slope[valid], svf[valid]])
print("Valid pixels:", len(features))

# 3. Scale the features so both count equally
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)

# 4. Train K-means on a random sample (faster), then label all pixels
rng = np.random.default_rng(42)
sample = features_scaled[rng.choice(len(features_scaled), 200000, replace=False)]
kmeans = KMeans(n_clusters=N_CLUSTERS, random_state=42, n_init=10).fit(sample)
labels = kmeans.predict(features_scaled)

# 5. Describe each cluster (to interpret it)
print("\nCluster | mean slope (deg) | mean SVF | share of area")
for c in range(N_CLUSTERS):
    part = features[labels == c]
    print(c + 1, "|", round(part[:, 0].mean(), 1), "|",
          round(part[:, 1].mean(), 3), "|", round(100 * len(part) / len(features), 1), "%")

# 6. Put the labels back into a map (0 = no data, 1-5 = clusters)
result = np.zeros(slope.shape, dtype="uint8")
result[valid] = labels + 1

profile.update(dtype="uint8", count=1, nodata=0)
with rasterio.open("TIFF/landforms_kmeans.tif", "w", **profile) as dst:
    dst.write(result, 1)

# 7. Quick preview image
plt.figure(figsize=(10, 4))
masked = np.ma.masked_equal(result, 0)
plt.imshow(masked, cmap="tab10", interpolation="nearest")
plt.colorbar(label="Cluster")
plt.title("K-means landform clusters (slope + SVF)")
plt.axis("off")
plt.tight_layout()
plt.savefig("figures/landforms_kmeans.png", dpi=150)
print("\nSaved TIFF/landforms_kmeans.tif and figures/landforms_kmeans.png")