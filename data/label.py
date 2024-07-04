#!/usr/bin/env python

import os

text_file = ["start.txt","finish.txt","start2.txt"]
output = ["labeled_start.txt","labeled_finish.txt","labeled_start2.txt"]
cwd = os.path.curdir # '.'

for i in range(3):
    # Walk thru each directory starting at '.' and if the directory contains
    # 'start.txt', print each line of the file prefixed by the name containing
    # directory.
    for root, dirs, files in os.walk(cwd):
        if text_file[i] in files: # We only care IF the file is in this directory.
            print ('Found %s!' %(root))
            filepath = os.path.join(root, text_file[i]) # './the_peasant/text.txt'
            root_base = os.path.basename(root)       # './the_peasant' => 'the_peasant'
            root_split = os.path.split(root)[0]
            root_base2 = os.path.basename(root_split)
            root_split2 = os.path.split(root_split)[0]
            root_base3 = os.path.basename(root_split2)
            root_split3 = os.path.split(root_split2)[0]
            root_base4 = os.path.basename(root_split3)
            root_split4 = os.path.split(root_split3)[0]
            root_base5 = os.path.basename(root_split4)

            out_filepath = os.path.join(root, output[i])
            out = open(out_filepath, 'w')

            with open(filepath, 'r') as reader:				# Open file for read/write
                for line in reader:						# Iterate the lines of the file
                    new_line = "%s;%s;%s;%s;%s;%s" % (root_base5,root_base4, root_base3, root_base2, root_base, line)
                    out.write(new_line)                # Write to the file
            out.close()
