import os
from datetime import datetime
import zipfile
import sys
import numpy as np
import json

def create_folder(fullpath, verbose=True):    
    """
    Creates a folder whether it does not exist
        :param fullpath: full path containing folder name
        :param verbose: boolean indicating printing log
    """
    
    if not os.path.exists(fullpath):
        if verbose:
            print ("Folder does not exist. Creating folder at " + fullpath)
        os.makedirs(fullpath)
    else:
        print ("Folder " + fullpath + " already exists.") if verbose else ''
    
def unzip_file(input_filepath, output_folder, verbose = True):
    """
    Function to unzip files
        :param input_filepath: path to zipped file
        :param output_folder: path to output folder
        :param verbose=True: boolean indicating printing log
    """

    print ("Unzipping file {} to folder {}".format(
        input_filepath, output_folder)) if verbose else ''

    create_folder(output_folder, verbose=verbose)

    check_file(input_filepath, verbose=True)

    with zipfile.ZipFile(input_filepath, 'r') as zip_ref:
        zip_ref.extractall(output_folder)

def check_file(filepath, verbose = True):
    """
    Checks if file in filepath exists
        :param filepath: path to file
        :param verbose: boolean indicating printing log
    """

    if os.path.isfile(filepath):
        print ('File exists in ' + filepath) if verbose else ''
        return True

    print ('File does NOT exist in ' + filepath) if verbose else ''
    return False

def load_json_file(filepath, verbose = False):
    """
    Loads json from *.json file into a variable. If file not found, returns None
        :param filepath: path to file
        :param verbose: boolean indicating printing log
    """
    if not check_file(filepath, verbose=verbose):
        return None
    
    with open(filepath) as json_file:
        data = json.load(json_file)
        
    return data


def mean_absolute_error(df):
    """ Calculates the mean absolute error between true and predicted items
    
    Arguments:
        df {pd.DataFrame} -- dataframe with columns 'rating' and 'predition'
    
    Returns:
        [float] -- mean absolute error
    """    

    return np.mean(np.absolute(df["rating"]-df["prediction"]))


def root_mean_squared_error(df):
    """ Calculates the root mean squared error between true and predicted items
    
    Arguments:
        df {pd.DataFrame} -- dataframe with columns 'rating' and 'predition'
    
    Returns:
        [float] -- root mean squared error
    """    
    
    return np.sqrt(np.mean((np.absolute(df["rating"]-df["prediction"]))**2))


def precision_at_k(df, k, threshold = 7.0):
    """ Calculates the precision@k for recommended items
    
    Arguments:
        df {pd.DataFrame} -- dataframe with columns 'rating' and 'predition'
        k {int} -- maximum rank to analyze
        threshold {float} -- minimum prediction value to recommend
    
    Returns:
        [float] -- precision@k value
    """  

    # removing items where true rating is unknown
    df = df.query("rating > 0").copy()
    
    df.sort_values(by=["u_id", "prediction"], ascending=False, inplace=True)

    for column in ["prediction", "rating"]:
        df[column + "_rank"] = df.groupby(["u_id"])[column].rank(ascending=False).astype(int)

    df["recommended"] = df["prediction"].apply(lambda x: 1 if x >= threshold else 0)
    df["consumed"] = df["rating"].apply(lambda x: 1 if x >= threshold else 0)
    df["hit"] = df["recommended"]*df["consumed"]
    
    return df.query("prediction_rank <= @k").groupby("u_id")["hit"].mean().mean()

def recall_at_k(df, k, threshold = 7):        

    df = df.query("rating > 0").copy()
    
    df.sort_values(by=["u_id", "prediction"], ascending=False, inplace=True)

    for column in ["prediction", "rating"]:
        df[column + "_rank"] = df.groupby(["u_id"])[column].rank(ascending=False).astype(int)

    df["recommended"] = df["prediction"].apply(lambda x: 1 if x >= threshold else 0)
    df["consumed"] = df["rating"].apply(lambda x: 1 if x >= threshold else 0)
    df["hit"] = df["recommended"]*df["consumed"]
    
    return df.query("rating_rank <= @k").groupby("u_id")["hit"].mean().mean()

class ProgressBar:
    def __init__(self, bar_length = 10, bar_fill = '#', elapsed_time=False):                
        
        self.bar_length = bar_length
        self.bar_fill = bar_fill
        self.status = ""
        self.last_progress = 0
        self.elapsed_time = elapsed_time

        if (elapsed_time):
            self.last_update = None
            self.start_time = None

    def update_progress(self, progress):
        
        self.status = ""
        self.last_progress = progress

        if isinstance(progress, int):
            progress = float(progress)

        if not isinstance(progress, float):
            progress = 0
            self.status = "error: progress var must be float\r\n"

        if progress < 0:
            progress = 0
            self.status = "Halt...\r\n"

        if progress >= 1:
            progress = 1
            self.status = "Done...\r\n"

        block = int(round(self.bar_length*progress))

        if (self.elapsed_time):
            if (progress == 0):
                self.start_time = datetime.now()

            self.last_update = datetime.now()

        if (self.elapsed_time and self.last_update is not None):
            text = "\r[{0}][{1}] {2:.2f}% {3}".format(str(self.last_update-self.start_time).split('.')[0], self.bar_fill*block + "-"*(self.bar_length-block), progress*100, self.status)
        else:
            text = "\rPercent: [{0}] {1:.2f}% {2}".format( self.bar_fill*block + "-"*(self.bar_length-block), progress*100, self.status)
        sys.stdout.write(text)
        sys.stdout.flush()

        
    
    def get_last_progress(self):
        return self.last_progress

    def get_elapsed_time(self):
        return str(self.last_update-self.start_time).split('.')[0]

if __name__ == "__main__":
    # create_folder('./../data')
    # check_file('./../data/brazilian-ecommerce.zip')
    # unzip_file('./../data/brazilian-ecommerce.zip', './../data')
    
    print (load_json_file("./config.json")["palette"])