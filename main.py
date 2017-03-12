"""
Adapted from the Tutorial for the Million Song Dataset
by Thierry Bertin-Mahieux (2011) Columbia University
   tb2332@columbia.edu
   Copyright 2011 T. Bertin-Mahieux, All Rights Reserved
"""

import os
import sys
import time
import glob
import datetime
import sqlite3
import numpy as np
import re

# Set this - path to the Million Song Dataset subset (uncompressed)
msd_subset_path='/home/devin/Desktop/MillionSongSubset'
msd_subset_data_path=os.path.join(msd_subset_path,'data')
msd_subset_addf_path=os.path.join(msd_subset_path,'AdditionalFiles')
assert os.path.isdir(msd_subset_path),'wrong path'

# imports specific to the MSD
import hdf5_getters as GETTERS

# print out table columns - uncomment if you want to check these
# conn = sqlite3.connect(os.path.join(msd_subset_addf_path, 'subset_track_metadata.db'))
# q = "PRAGMA table_info(songs)"
# res = conn.execute(q)
# table_info = res.fetchall()
# conn.close()

# for info in table_info:
#     print(info)


# iterate the files
def apply_to_all_files(basedir,func=lambda x: x,ext='.h5'):
    """
    From a base directory, go through all subdirectories,
    find all files with the given extension, apply the
    given function 'func' to all of them.
    If no 'func' is passed, we do nothing except counting.
    INPUT
       basedir  - base directory of the dataset
       func     - function to apply to all filenames
       ext      - extension, .h5 by default
    RETURN
       number of files
    """
    cnt = 0
    # iterate over all files in all subdirectories
    for root, dirs, files in os.walk(basedir):
        files = glob.glob(os.path.join(root,'*'+ext))
        # count files
        cnt += len(files)
        # apply function to all files
        for f in files :
            func(f)       
    return cnt

number_of_songs = 20

# get some random songs
conn = sqlite3.connect(os.path.join(msd_subset_addf_path, 'subset_track_metadata.db'))
q = "SELECT * FROM songs ORDER BY RANDOM() LIMIT " + str(number_of_songs)
res = conn.execute(q)
random_songs = res.fetchall()
print('got ' + str(number_of_songs) + ' random songs from metedata db!')
conn.close()

print('fetching actual song data for each song...')

all_the_data = []

# weka doesn't like the following characters in arff files
# we might need to add more characters to this as we discover them
def replace_characters(string):
    return string.replace(" ", "_").replace(",", "_").replace("'", "_")

# what we want to run on each file - this is super inefficient, but it works
def func_to_desired_song_data(filename):
    h5 = GETTERS.open_h5_file_read(filename)
    track_id = GETTERS.get_track_id(h5)
    for song in random_songs:
        if song[0] == track_id:
            print("FOUND ONE!")
            title = replace_characters(GETTERS.get_title(h5))
            artist = replace_characters(GETTERS.get_artist_name(h5))
            energy = GETTERS.get_energy(h5)
            tempo = GETTERS.get_tempo(h5)
            key = GETTERS.get_key(h5)
            loudness = GETTERS.get_loudness(h5)

            song_data = {
                'title': title,
                'artist': artist,
                'energy': energy,
                'tempo': tempo,
                'key': key,
                'loudness': loudness
            }

            all_the_data.append(song_data)

    h5.close()

apply_to_all_files(msd_subset_data_path,func=func_to_desired_song_data)

# Print data
for data in all_the_data:
    print(data)

# Output arff file - the like/dislike class will be manually added
output_filename = 'songs.arff'
with open(output_filename,"w") as fp:
    fp.write('''@RELATION songs

@ATTRIBUTE title string
@ATTRIBUTE artist string
@ATTRIBUTE energy numeric
@ATTRIBUTE tempo numeric
@ATTRIBUTE key numeric
@ATTRIBUTE loudness numeric
@ATTRIBUTE class {like, dislike}

@DATA
''')
    for data in all_the_data:
        fp.write("%s," % data['title'])
        fp.write("%s," % data['artist'])
        fp.write("%s," % data['energy'])
        fp.write("%s," % data['tempo'])
        fp.write("%s," % data['key'])
        fp.write("%s," % data['loudness'])
        # class will be manually written here
        fp.write("\n")
