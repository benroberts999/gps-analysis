#!/usr/bin/env python3
import numpy as np
import pandas as pd
from scipy.fft import fft, fftshift, fftfreq

"""
Functions to analyse GPS data.

calculate_GPS_spectrum() Performs the full analysis:

 * For given day of data:
    * Downloads the data (clock solution and orbits)
    * Discards all clocks with incomplete data
    * Forms "pairs" of GPS clocks that are at opposite orbital positions
    * Forms weighted average of fractional frequency (average of all clock pairs)
    * Calculates amplitude spectrum 

OR:
Doed analysis for each satellite, without forming pairs.
This is what we actually need.

Indevidual functions also available.
"""

# Folder to download data
dpath = "jpligsac/"
# Data sampling time (in seconds)
tau0 = 30.0
# Number of data points in frequency data
num_data_points = 2880

# Frequencies (sample points of ampltide spectrum)
freq = fftshift(fftfreq(num_data_points, d=tau0))


###############################################################################
def download_data(week, day, get_orbits=True):
    from os import path, mkdir
    from urllib import request

    if not path.exists(dpath):
        mkdir(dpath)

    """Downloads GPS clock and orbit data (if we don't already have it)"""
    url = "https://sideshow.jpl.nasa.gov/pub/jpligsac/" + str(week) + "/"
    filename_base = "jpl" + str(week) + str(day)
    clk_fname = filename_base + ".clk.gz"
    orb_fname = filename_base + ".sp3.gz"
    # download clock data:
    if not path.isfile(dpath + clk_fname):
        downloaded_file, _ = request.urlretrieve(
            url + clk_fname,
            dpath + clk_fname,
        )
        if downloaded_file != dpath + clk_fname:
            return False
    # download orbit data:
    if get_orbits:
        if not path.isfile(dpath + orb_fname):
            downloaded_file, _ = request.urlretrieve(
                url + orb_fname,
                dpath + orb_fname,
            )
            if downloaded_file != dpath + orb_fname:
                return False
    return filename_base


###############################################################################
def find_line_containing(file, the_string) -> int:
    """Looks for string `the_string` in open file `file`; returns line number.
    File pointer will now point to end of `the_string`.
    """
    for num, line in enumerate(file, 1):
        if the_string in line:
            return num


def convert_time(row, day):
    """Converts GPS time stamps into usuable float `seconds`"""
    return (
        row["Day"] * 24.0 * 60.0 * 60.0
        + row["Hour"] * 60.0 * 60.0
        + row["Minute"] * 60.0
        + row["Second"]
        - day * 24.0 * 60.0 * 60.0
    )


###############################################################################
def get_data(filename):
    """Return pandas dataframe of all clock data"""
    import gzip

    with gzip.open(dpath + filename + ".clk.gz", "rt") as unziped:
        _ = find_line_containing(unziped, "END OF HEADER")
        data = pd.read_csv(
            unziped,
            delimiter=" ",
            skipinitialspace=True,  # Interpret multiple spaces as 1 delimiter
            names=(  # Optional: give meaningful names to each column of data file:
                "Type",  # AR=Reciever, AS=Satellite
                "PRN",  # "PRN" clode for each sattelite
                "Year",  # time stamp
                "Month",
                "Day",
                "Hour",
                "Minute",
                "Second",
                "ncols",  # always 2
                "Bias",  # Bias (s): main data
                "FError",  # "Formal Error" - not very meaningful
            ),
        )
        keywords = {"day": data["Day"].iloc[0]}
        data["Time"] = data.apply(convert_time, axis=1, **keywords)

        # Get date in human-readable form
        date_string = (
            str(data.iloc[0]["Year"])
            + "-"
            + str(data.iloc[0]["Month"])
            + "-"
            + str(data.iloc[0]["Day"])
        )

        return data[data.Type == "AS"], date_string


###############################################################################
def get_good_clocks(data):
    """Returns list of `good` clocks (and their fractional frequencies dw/w).
    Good means no missing data."""
    # Get "good" clocks: no missing data
    t_PRNs = np.sort(data["PRN"].unique())
    PRNs = []
    for prn in t_PRNs:
        tbias = data[data["PRN"] == prn]["Bias"]
        ttime = data[data["PRN"] == prn]["Time"]
        # Number of data points in bias data is 1 more than in freq. data
        if tbias.size == num_data_points + 1 and ttime.size == tbias.size:
            PRNs.append(prn)
    PRNs = np.array(PRNs)
    dws = np.array([np.diff(data[data.PRN == prn]["Bias"]) / tau0 for prn in PRNs])
    return [PRNs, dws]


###############################################################################
def get_orbits(filename):
    """Return pandas dataframe of all orbit data (in km).
    (Sampled every 5 minuts only)"""
    import csv

    return pd.read_csv(
        dpath + filename + ".sp3.gz",
        skiprows=22,  # hopefully always the same *fingers crossed emoji*
        delimiter=" ",
        on_bad_lines="skip",
        comment="*",
        skipinitialspace=True,
        usecols=[i for i in range(4)],
        quoting=csv.QUOTE_NONE,
        names=(
            "PRN",
            "x",
            "y",
            "z",
        ),
    )[:-1]


###############################################################################
def calculate_distance(d1, d2):
    """Calculates disnace between two clock orbits. Returns in units of 10000 km"""
    return (
        np.sqrt(
            (d1["x"].to_numpy() - d2["x"].to_numpy()) ** 2
            + ((d1["y"].to_numpy() - d2["y"].to_numpy()) ** 2)
            + ((d1["z"].to_numpy() - d2["z"].to_numpy()) ** 2)
        )
        / 10000
    )


###############################################################################
def form_GPS_pairs(good_clocks, orbits, min_distance=5.0, max_range_fraction=0.05):
    """
    Forms pairs of GPS clocks in the oposite orbital position.
    only choose pairs that are at least 5 (*10000) km apart on average
    And that have a range < 5% of their maximum
    """

    good_pairs = []
    distances = []
    for i0, clock0 in enumerate(good_clocks):
        d0 = orbits[orbits["PRN"] == "P" + clock0]

        for i1, clock_i in enumerate(good_clocks):
            if i1 <= i0:  # only include each pair once
                continue
            d_i = orbits[orbits["PRN"] == "P" + clock_i]

            dr = calculate_distance(d0, d_i)

            distance = np.mean(dr)
            d_range = 0.5 * (np.max(dr) - np.min(dr))
            good_pair = (
                distance > min_distance and d_range < max_range_fraction * distance
            )

            if good_pair:
                good_pairs.append([i0, i1])
                distances.append([distance])

    good_pairs = np.array(good_pairs)
    distances = np.array(distances)
    return good_pairs, np.mean(distances)


###############################################################################
def return_distances(good_pairs, good_clocks, orbits):
    """Calculates distances bwteen clock pairs, as function of time.
    (Not used in analysis, just for plotting)."""

    num_points = orbits[orbits["PRN"] == "P" + good_clocks[0]]["x"].size
    Rs = np.empty((len(good_pairs), num_points))
    time = np.linspace(0.0, 24.0, num_points)

    for count, [i0, i1] in enumerate(good_pairs):
        clock0, clock1 = good_clocks[i0], good_clocks[i1]
        d0 = orbits[orbits["PRN"] == "P" + clock0]
        d1 = orbits[orbits["PRN"] == "P" + clock1]
        Rs[count] = calculate_distance(d0, d1)
    return time, Rs


###############################################################################
def form_weighted_average(dws, good_clocks_or_pairs, max_sigma=0):
    """Forms weighted average of clock frequncy data dw/w"""

    dw_avg = np.zeros(2880)
    weight = 0.0

    max_var = max_sigma**2

    use_pairs = len(good_clocks_or_pairs) > 0 and len(good_clocks_or_pairs[0]) == 2

    if use_pairs:
        for i0, i1 in good_clocks_or_pairs:
            dw1 = dws[i0] - dws[i1]
            dw1 = dw1 - np.mean(dw1)
            sig2 = np.var(dw1)
            if sig2 > max_var and max_var > 0.0:
                continue
            dw_avg += dw1 / sig2
            weight += 1.0 / sig2
    else:
        for i, _ in enumerate(good_clocks_or_pairs):
            sig2 = np.var(dws[i])
            if sig2 > max_var and max_var > 0.0:
                continue
            dw_avg += (dws[i] - np.mean(dws[i])) / sig2
            weight += 1.0 / sig2

    dw_avg /= weight
    return dw_avg


###############################################################################
def amplitude_spectrum(dw_avg):
    """Computes amplitude spectrum"""
    ft = fftshift(fft(dw_avg))
    return 2.0 * np.abs(ft) / dw_avg.size


###############################################################################
def calculate_GPS_spectrum(week, day):
    """Performs full analysis for a single day of data.
    Downloads data, parses it, forms clocks into pairs with L=~50,000km,
    forms weigted average of freuqencies, and finally the amplitude spectrum.
    Returns: ampltiude sprectum (array), date (string)
    """
    fname = download_data(week, day)
    if not fname:
        return [], ""
    data, date = get_data(fname)
    good_clocks, dws = get_good_clocks(data)
    if len(good_clocks) == 0:
        return [], ""

    orbits = get_orbits(fname)
    good_pairs, _ = form_GPS_pairs(good_clocks, orbits)
    if len(good_pairs) == 0:
        return [], ""

    dw_avg = form_weighted_average(dws, good_pairs)
    return amplitude_spectrum(dw_avg), date


###############################################################################
def calculate_GPS_spectrum_single(week, day):
    """Performs full analysis for a single day of data.
    Downloads data, parses it, forms clocks into pairs with L=~50,000km,
    forms weigted average of freuqencies, and finally the amplitude spectrum.
    Returns: ampltiude sprectum (array), date (string)
    """
    fname = download_data(week, day, False)
    if not fname:
        return [], ""
    data, date = get_data(fname)
    good_clocks, dws = get_good_clocks(data)
    if len(good_clocks) == 0:
        return [], ""

    dw_avg = form_weighted_average(dws, good_clocks)
    return amplitude_spectrum(dw_avg), date


###############################################################################
###############################################################################
def main():
    from matplotlib import pyplot as plt
    from sys import argv

    week = argv[1] if len(argv) > 1 else 2300
    day = argv[2] if len(argv) > 2 else 0

    print(f"As a test: calculate spectrum for GPS day {week}:{day}")

    amplitude, date = calculate_GPS_spectrum(week, day)
    if len(amplitude) == 0:
        print(f"GPS day {week}:{day} [{date}] not OK?")

    plt.plot(freq, amplitude)
    plt.title(f"Amplitude spectrum for GPS pairs [{date}]")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("$\\delta\\omega/\\omega$ Amplitude spectrum")
    plt.xlim(1e-5, 0.1)
    plt.ylim(1e-16, 1e-13)
    plt.xscale("log")
    plt.yscale("log")
    plt.tick_params(direction="in", which="both")
    plt.show()


###############################################################################
if __name__ == "__main__":
    main()
