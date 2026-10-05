# \# Reading the Summit: LiDAR Terrain Analysis of Mt. Fuji

# 

# A 0.5 m bare-earth terrain model of Mt. Fuji's summit area and upper slopes, built from open airborne LiDAR and used to map steepness, erosion gullies and human-made trails.

# 

# !\[DTM coloured by elevation over hillshade](figures/dtm.png)

# \*0.5 m DTM coloured by elevation (≈2,330 m to 3,778 m) over a hillshade. The summit crater is at the top left; radial gullies and switchback trails run down the slopes.\*

# 

# \---

# 

# \## Overview

# 

# High-resolution airborne LiDAR can reveal terrain detail that coarser elevation models miss. This project processes 38 open LiDAR tiles covering Mt. Fuji's summit area into a seamless digital terrain model (DTM), then derives three complementary views of the surface:

# 

# \- \*\*Hillshade\*\*: overall form of the summit and slopes

# \- \*\*Sky-view factor (SVF)\*\*: direction-independent relief that highlights gullies and enclosed features

# \- \*\*Slope classes\*\*: steepness in four classes relevant to rockfall and debris-flow susceptibility

# 

# \## Data

# 

# | Item | Details |

# |---|---|

# | Source | VIRTUAL SHIZUOKA open point cloud data, Shizuoka Prefecture (2021) |

# | Product | Ground-classified airborne LiDAR (`LP/Ground`) |

# | Location | `s3://virtual-shizuoka/2021/LP/Ground/08/ME/35/` (public, no sign-in required) |

# | Tiles | 38 tiles, each 400 m × 300 m (list in \[`scripts/tiles.txt`](scripts/tiles.txt)) |

# | Points | ≈7–11 million ground points per tile, roughly 60–90 points/m² |

# | CRS | JGD2011 / Japan Plane Rectangular CS VIII (EPSG:6676) |

# 

# Raw data is not included in this repository because of its size. Run \[`scripts/01\_download\_tiles.ps1`](scripts/01\_download\_tiles.ps1) to download it.

# 

# \*\*Data credit:\*\* VIRTUAL SHIZUOKA point cloud data © Shizuoka Prefecture (静岡県), licensed under \[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Distributed via the \[G-Spatial Information Center](https://www.geospatial.jp/ckan/dataset/shizuoka-19-20-pointcloud) and the AWS open data bucket above. The data was processed (CRS assignment, rasterisation and terrain analysis) for this project.

# 

# \## Method

# 

# All processing was done in QGIS 3.44.1 using its PDAL-based point cloud tools (PDAL 2.9.0) and the Relief Visualization Toolbox.

# 

# 1\. \*\*Download:\*\* fetch the 38 zipped LAS tiles from the public S3 bucket.

# 2\. \*\*Assign CRS:\*\* the tiles had no coordinate system recorded, so EPSG:6676 was assigned to each tile (batch process).

# 3\. \*\*Virtual point cloud (VPC):\*\* link all tiles into a single virtual layer instead of merging them into one large file.

# 4\. \*\*DTM:\*\* rasterise ground point elevations (Z) at \*\*0.5 m\*\* resolution. The high point density easily supports this resolution.

# 5\. \*\*Hillshade:\*\* azimuth 315°, altitude 45°, z-factor 1.

# 6\. \*\*Sky-view factor:\*\* search radius 20 px (10 m), 16 directions.

# 7\. \*\*Slope:\*\* computed in degrees, then displayed in four classes: 0–15°, 15–30°, 30–45° and >45°.

# 8\. \*\*Contours:\*\* 20 m interval, generated from the DTM.

# 

# The processing commands are in \[`scripts/02\_process.py`](scripts/02\_process.py), exported from the QGIS Processing History. Layer styles are in \[`styles/`](styles/).

# 

# \## Results

# 

# | Hillshade | Sky-view factor |

# |---|---|

# | !\[Hillshade](figures/hillshade.png) | !\[Sky-view factor](figures/svf.png) |

# | Overall form of the summit crater and upper slopes. | Gullies appear as dark lines and ridges as bright ones, independent of light direction. |

# 

# \### Slope classes

# 

# !\[Slope classes over hillshade](figures/slope\_classes.png)

# \*Green: 0–15° · Yellow: 15–30° · Orange: 30–45° · Red: >45°\*

# 

# \- Most of the upper slope falls in the \*\*30–45°\*\* class, consistent with Mt. Fuji's steep upper cone.

# \- Slopes \*\*above 45°\*\* are concentrated on the \*\*crater walls\*\* and the \*\*sides of the radial gullies\*\*, the zones most prone to rockfall.

# \- The gentlest areas (<15°) are on the crater floor and summit rim, and along constructed paths.

# 

# \### Human-made features at 0.5 m

# 

# !\[Close-up of switchback trails](figures/closeup\_trails.png)

# \*Close-up of the slope map below the summit.\*

# 

# At 0.5 m resolution, the DTM resolves the \*\*switchback climbing trails\*\*: flat (green) paths cut into the steep (orange) slope. Small rectangular features along the trails and near the summit rim appear to be structures such as mountain huts. Because the data is ground-classified, these show up as outlines in the terrain rather than as full buildings.

# 

# \## Limitations

# 

# \- \*\*Ground points only:\*\* buildings, vegetation and other above-ground features were removed by the data provider's classification, so the DTM represents bare earth.

# \- \*\*Coverage gaps:\*\* the selected tiles do not form a complete rectangle, leaving blank (NoData) areas.

# \- \*\*Single date:\*\* with one survey epoch, the project describes current terrain but cannot measure change over time.

# \- \*\*Edge effects:\*\* SVF and slope values near NoData borders may be less reliable.

# \- \*\*Visual interpretation:\*\* the identification of trails and structures is based on visual inspection, not ground verification.

# 

# \## How to reproduce

# 

# 1\. Install \[QGIS](https://qgis.org) (3.32 or later for point cloud processing tools) and the \[AWS CLI](https://aws.amazon.com/cli/).

# 2\. Download the tiles:

# &#x20;  ```powershell

# &#x20;  ./scripts/01\_download\_tiles.ps1

# &#x20;  ```

# 3\. Unzip the tiles and run the processing steps in \[`scripts/02\_process.py`](scripts/02\_process.py) from the QGIS Python console, adjusting file paths as needed.

# 4\. Load the styles from \[`styles/`](styles/) to match the figures.

# 

# \## Repository structure

# 

# ```

# mt-fuji-lidar-dtm-analysis/

# ├── README.md

# ├── scripts/

# │   ├── 01\_download\_tiles.ps1   # download tiles from the public S3 bucket

# │   ├── 02\_process.py           # QGIS processing steps (from Processing History)

# │   └── tiles.txt               # list of the 38 tile IDs

# ├── figures/                    # exported PNG maps

# └── styles/                     # QGIS layer styles (.qml)

# ```

# 

# \## Next steps

# 

# \- Quantify the area in each slope class with Python (`rasterio`, `numpy`).

# \- Unsupervised landform classification (K-means on slope, SVF and curvature) to separate crater walls, gullies, ridges and trails.

# \- Pair with a second survey epoch for change detection.

# 

# \## Author

# 

# \*\*Umme Fatema\*\*, LiDAR and geospatial data engineer · \[github.com/ummeFA](https://github.com/ummeFA)

