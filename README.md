# gps-analysis

[![arXiv][arXiv-badge]][arXiv-url]

Code to analyse GPS data for oscillating shifts in the frequency of the on board atomic clocks.

Companion code to: 
 * _Ultralight Dark Matter Search with Space-Time Separated Atomic Clocks and Cavities_, Melina Filzinger, Ashlee R. Caddell, Dhruv Jani, Martin Steinel, Leonardo Giani, Nils Huntemann, and Benjamin M. Roberts, [arXiv:2312.13723](https://arxiv.org/abs/2312.13723)

 * [AnalyseGPS.py](AnalyseGPS.py)
   * Base functions to grab, parse, and analyse the GPS atomic clock and positions data, made publicly available by JPL at [sideshow.jpl.nasa.gov/pub/jpligsac/](https://sideshow.jpl.nasa.gov/pub/jpligsac/)
   * _Note added: The clock and position solutions from JPL seem to have been removed or moved from the above location? The current link gives a 404 error_
 * [analyse_gps_sats.ipynb](analyse_gps_sats.ipynb)
   * Some examples demonstrating method, then the full analysis for the paper
 * [calc_dailymod_ECI.ipynb](calc_dailymod_ECI.ipynb)
   * Calculates the $\vec{n}(t)\cdot\vec{n}_{\rm gal}$ dot product for the sidereal modulation calculation. Relevant for NPL-PTB cavity comparison (see paper)
 * [shm.nb](shm.nb)
   * Mathematic notebook with vector Standard Halo Model formulas; not directly used for paper, but useful for directional sensitivity

[arXiv-badge]: https://img.shields.io/badge/arXiv-2312.13723-b31b1b.svg?style=flat
[arXiv-url]: https://arxiv.org/abs/2312.13723
