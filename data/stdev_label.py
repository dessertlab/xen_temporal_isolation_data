import statistics
import os

text_file = ["start.txt","finish.txt","start2.txt"]
output = ["start_stdev.txt","finish_stdev.txt","start2_stdev.txt"]
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

			#calculate stdev of data in *.txt file
            lines = [line.rstrip('\n') for line in open(filepath)]
            stdev = statistics.stdev(map(float,lines))
            print("Standard Deviation of sample is % s " % (stdev))

			# write result on file
            print("writing file ... path:%s "%(os.path.join(root, output[i])))
            try:
                with open(os.path.join(root, output[i]), 'w') as f:
                    new_line = "%s;%s;%s;%s;%s;%s" % (root_base5,root_base4, root_base3, root_base2, root_base, stdev)
                    f.write(new_line)
            except FileNotFoundError:
                    print("The 'docs' directory does not exist")
