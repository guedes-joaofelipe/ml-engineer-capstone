import os
import sys
sources_path = './../sources'
if sources_path not in sys.path:
    sys.path.append(sources_path)
import utils

if __name__ == "__main__":
    
    verbose = True
    ecommerce_filepath = "./../data/brazilian-ecommerce.zip"
    marketing_funnel_filepath = './../data/marketing-funnel-olist.zip'
    output_dir = './../data'
    
    for filepath in [ecommerce_filepath, marketing_funnel_filepath]:
        if not utils.check_file(filepath, verbose=False):
            print ("ERROR: file " + ecommerce_filepath + " does not exist")
            exit()

        utils.unzip_file(filepath, output_dir, verbose)