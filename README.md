## Description:
This script grabs a random assortment of songs from the million song dataset (or from a subset of it), and extracts desired attributes. It then creates a partial arff file that can be input into weka after adding in the 'like' or 'dislike' class value.

## Setup:
1. Install hdf5: https://support.hdfgroup.org/HDF5/release/obtain518.html
  * I couldn't get this working on windows, I ended up using linux and the following: http://stackoverflow.com/questions/31719451/install-hdf5-and-pytables-in-ubuntu
2. Install the follwing python packages:
  * numpy
  * tables

## Use:
Open up main.py, set the `msd_subset_path` to the location of the dataset (tested with the 10,000 song subset), and set the desired number of random songs (`number_of_songs`).

Next, run it with `python main.py`

This will output a file called songs.arff. Open the file, and add in the 'like' or 'dislike' attribute to the end of each song line. This data can then be opened in weka.
