# Lunar Crustal Magnetic Field & Soft Landing Sites Notebook

This directory contains the computational notebook used to generate **Figure 1** for the review manuscript:  
*Near-Null Magnetic Fields in Lunar Plant Biology: The First Five Days of Seedling Growth*.

---

## Overview

The notebook [`mag_near_far_landings.ipynb`](mag_near_far_landings.ipynb) generates a publication-ready, three-panel figure depicting the Moon's crustal magnetic field at 30 km altitude over high-resolution LOLA topography, superposed with all 28 historical soft landings (1966–2024) and candidate Artemis South Polar exploration regions:

- **Panel a (Near side):** Orthographic projection centered on $(0^\circ\text{E}, 10^\circ\text{S})$ showing the `T2015_449` total magnetic field magnitude over LOLA hillshade, overlaid with Surveyor, Apollo, Luna, Chang'e, SLIM, and Chandrayaan-3 landing locations.
- **Panel b (Far side):** Orthographic projection centered on $(180^\circ\text{E}, 10^\circ\text{S})$ highlighting the South Pole-Aitken (SPA) basin anomaly and far-side landings (Chang'e 4, Chang'e 6).
- **Panel c (South polar region):** Polar stereographic zoom ($S0/-90^\circ$) displaying NASA's candidate Artemis exploration regions (Haworth, Malapert Massif, Mons Mouton Plateau, Mons Mouton, Nobile Rim 1 & 2, de Gerlache Rim 2, Slater Plain, Peak near Cabeus B) and recent polar robotic landings (IM-1, Chandrayaan-3), with a 100 km scale bar, landing catalog index (1–28), and a shared 0–10 nT Roma colormap.

---

## Data Sources & Models

1. **Magnetic Field Model (`T2015_449`):**  
   Spherical harmonic crustal field model evaluated at 30 km altitude above the mean lunar radius ($R_M = 1737.4\text{ km}$), derived from combined Kaguya (LMAG) and Lunar Prospector (MAG) observations (Tsunakawa et al., 2015).
2. **Topography Model (`LOLA_shape`):**  
   Spherical harmonic lunar shape model up to degree and order 1439, derived from the Lunar Orbiter Laser Altimeter (LOLA) aboard the Lunar Reconnaissance Orbiter (Wieczorek, 2024).
3. **Soft Landing Coordinates:**  
   Compiled from published mission records and LRO camera landing site coordinates (NASA LROC / PDS).

---

## Environment & Execution Setup

Because `pygmt` interfaces with the Generic Mapping Tools (GMT) C shared libraries, installing via `conda-forge` is recommended:

```bash
# 1. Create dedicated conda environment
conda create -n lunar-maps -c conda-forge python=3.11 pyshtools=4.13.1 pygmt=0.15.0 gmt=6.4.0 numpy=1.26 ghostscript xarray scipy pooch netcdf4 jupyterlab ipywidgets

# 2. Activate environment
conda activate lunar-maps

# 3. Launch JupyterLab and run all cells
jupyter lab mag_near_far_landings.ipynb
```

On first execution, `pyshtools` will automatically retrieve and cache the spherical harmonic coefficient datasets (~20 MB). Outputs are saved directly as vector EPS/PDF and 300 DPI PNG (`Mag_near_far_landings.png` and `.pdf`).
