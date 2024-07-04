import statistics
import os
import pandas as pd
import numpy as np

def reject_outliers(data, m=2):
    return data[abs(data - np.mean(data)) < m * np.std(data)]

text_file = ["start.txt","finish.txt","start2.txt"]
output = ["start_max.txt","finish_max.txt","start2_max.txt"]
cwd = os.path.curdir # '.'

for i in range(3):
    print("input: %s" %(text_file[i]))
    print("output: %s" %(output[i]))
    # Walk thru each directory starting at '.' and if the directory contains 
    # 'start.txt' calculate stdev of data
    for root, dirs, files in os.walk(cwd):
        if text_file[i] in files: 						# We only care IF the file is in this directory.
            filepath = os.path.join(root, text_file[i])	# './the_peasant/text.txt'
            root_base = os.path.basename(root)			# './the_peasant' => 'the_peasant'
            root_split = os.path.split(root)[0]
            root_base2 = os.path.basename(root_split)
            root_split2 = os.path.split(root_split)[0]
            root_base3 = os.path.basename(root_split2)
            root_split3 = os.path.split(root_split2)[0]
            root_base4 = os.path.basename(root_split3)     	 
            root_split4 = os.path.split(root_split3)[0]
            root_base5 = os.path.basename(root_split4)   

            # Remove Outliers
            lines = [line.rstrip('\n') for line in open(filepath)]
            int_lines = list(map(int, lines))
            int_lines = np.array(int_lines)

            Premax = np.amax(int_lines)
            print("PRE-Max of sample is % s " % (Premax))

            # remove outlier    
            int_lines = reject_outliers(int_lines,2)
            print("N Outliers: % s" % (2000-int_lines.size))
			# calculate max of data in *.txt file
            max = np.amax(int_lines)
            print("Max of sample is % s " % (max))

			# write result on file
            print("writing file ... path:%s "%(os.path.join(root, output[i])))
            try:
                with open(os.path.join(root, output[i]), 'w') as f:
                    new_line = "%s;%s;%s;%s;%s;%s" % (root_base5,root_base4, root_base3, root_base2, root_base, max)
                    f.write(new_line)
            except FileNotFoundError:
                    print("The 'docs' directory does not exist")
