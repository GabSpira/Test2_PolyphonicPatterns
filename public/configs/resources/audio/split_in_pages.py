import argparse
import os
import shutil
import random

# Use this code in a folder with a group of files that you want to randomly but evenly split in sub-folders

# To split in 4 pages the 40 samples of each dataset:
# In this context I use it placed in /audio/ and i give the parser argument ./patterns/dataset_00i
# So to execute the code, run the command 'py split_in_pages.py ./patterns/dataset_00i' once you are in configs/resources/audio



N = 10  # the number of files in each sub-folder

def move_files(abs_dirname):

    # Set your directory here
    direc = './patterns'

    files = [os.path.join(abs_dirname, f) for f in os.listdir(abs_dirname)]

    # create sub-folders
    num_folders = len(files) // N
    for j in range(1,num_folders+1):
        subdir_name = os.path.join(abs_dirname, 'page_{0:03d}'.format(j))
        os.mkdir(subdir_name)

    dir_list = next(os.walk(direc))[1]

    
    for f in files:
        
        # for each file
        f_base = os.path.basename(f)

        # choose a random folder
        subdir1 = random.choice(dir_list)
        subdir2 = random.choice([item for item in dir_list if item != subdir1])
        # subdir3 = random.choice([item for item in dir_list if ((item != subdir1) & (item != subdir2))])
        # subdir4 = random.choice([item for item in dir_list if ((item != subdir1) & (item != subdir2) & (item != subdir3))])

        # count the files in it and in another one (there will be 3 folders in total)
        files_in_subdir1 = [os.path.join(direc, subdir1, j) for j in os.listdir(os.path.join(direc, subdir1))]
        files_in_subdir2 = [os.path.join(direc, subdir2, j) for j in os.listdir(os.path.join(direc, subdir2))]
        # files_in_subdir3 = [os.path.join(direc, subdir3, j) for j in os.listdir(os.path.join(direc, subdir3))]

        # move the file to the randomly selected folder, or if it's already full, move it to another one
        if len(files_in_subdir1)<N:
            shutil.move(f, os.path.join(direc, subdir1, f_base))
        elif len(files_in_subdir2)<N:           
            shutil.move(f, os.path.join(direc, subdir2, f_base)) 
        # elif len(files_in_subdir3)<N: 
        #     shutil.move(f, os.path.join(direc, subdir3, f_base))
        # else:
        #     shutil.move(f, os.path.join(direc, subdir4, f_base))

    



def parse_args():
    """Parse command line arguments passed to script invocation."""
    parser = argparse.ArgumentParser(
        description='Split files into multiple subfolders.')

    parser.add_argument('src_dir', help='source directory')

    return parser.parse_args()


def main():
    """Module's main entry point (zopectl.command)."""
    args = parse_args()
    src_dir = args.src_dir

    if not os.path.exists(src_dir):
        raise Exception('Directory does not exist ({0}).'.format(src_dir))

    move_files(os.path.abspath(src_dir))


if __name__ == '__main__':
    main()