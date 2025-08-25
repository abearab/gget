import os
import requests
from tqdm import tqdm
import pandas as pd
from .utils import set_up_logger
from .constants import DATAVERSE_GET_URL

logger = set_up_logger()

def dataverse_downloader(url, path, file_name, verbose=True):
    """dataverse download helper with progress bar

    Args:
        url (str): the url of the dataset to download
        path (str): the path to save the dataset locally
        file_name (str): the name of the file to save locally
        verbose (bool): whether to show progress and logging
    """
    save_path = os.path.join(path, file_name)
    
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        total_size_in_bytes = int(response.headers.get("content-length", 0))
        block_size = 1024
        
        if verbose:
            progress_bar = tqdm(total=total_size_in_bytes, unit="iB", unit_scale=True)
        
        with open(save_path, "wb") as file:
            for data in response.iter_content(block_size):
                if verbose:
                    progress_bar.update(len(data))
                file.write(data)
        
        if verbose:
            progress_bar.close()
            
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to download file from {url}: {e}")
    except OSError as e:
        raise RuntimeError(f"Failed to save file to {save_path}: {e}")


def download_wrapper(entry, path, return_type=None, verbose=True):
    """wrapper for downloading a dataset given the name and path, for csv,pkl,tsv or similar files

    Args:
        entry (dict): the entry of the dataset to download. Must include 'id', 'name', 'type' keys
        path (str): the path to save the dataset locally
        return_type (str, optional): the return type. Defaults to None. Can be "url", "filename", or ["url", "filename"]
        verbose (bool): whether to show progress and logging

    Returns:
        str: the exact dataset query name
    """
    # Validate entry has required keys
    required_keys = ['id', 'name', 'type']
    missing_keys = [key for key in required_keys if key not in entry]
    if missing_keys:
        raise ValueError(f"Entry missing required keys: {missing_keys}. Entry must contain 'id', 'name', and 'type' columns.")
    
    url = DATAVERSE_GET_URL + str(entry['id'])

    try:
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
    except OSError as e:
        raise RuntimeError(f"Failed to create directory {path}: {e}")

    filename = f"{entry['name']}.{entry['type']}"

    if os.path.exists(os.path.join(path, filename)):
        if verbose:
            logger.info(f"Found local copy for {entry['id']} datafile as {filename}")
    else:
        if verbose:
            logger.info(f"Downloading {entry['id']} datafile as {filename}")
        dataverse_downloader(url, path, filename, verbose)
    
    if return_type == "url":
        return url
    elif return_type == "filename":
        return filename
    elif return_type == ["url", "filename"]:
        return url, filename


def dataverse(df, path=".", sep=",", verbose=True):
    """download datasets from dataverse for a given dataframe
    Input dataframe must have 'name', 'id', 'type' columns.
    - 'name' is the dataset name for single file
    - 'id' is the unique identifier for the file
    - 'type' is the file type (e.g. csv, tsv, pkl)

    Args:
        df (pd.DataFrame or str): the dataframe or path to the csv/tsv file
        path (str): the path to save the dataset locally. Default: current working directory
        sep (str): separator for CSV/TSV files. Default: ","
        verbose (bool): whether to show progress and logging. Default: True
        
    Returns:
        None
        
    Raises:
        FileNotFoundError: if input file doesn't exist
        ValueError: if input is not a DataFrame or file path, or if required columns are missing
        RuntimeError: if download or file operations fail
    """
    if isinstance(df, str):
        if not os.path.exists(df):
            raise FileNotFoundError(f"File {df} not found")
        try:
            df = pd.read_csv(df, sep=sep)
        except Exception as e:
            raise ValueError(f"Failed to read file {df}: {e}")
    elif isinstance(df, pd.DataFrame):
        pass
    else:
        raise ValueError("Input must be a pandas DataFrame or a path to a csv/tsv file")
    
    # Validate required columns
    required_columns = ['id', 'name', 'type']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Input dataframe missing required columns: {missing_columns}. Required columns are: {required_columns}")
    
    if len(df) == 0:
        raise ValueError("Input dataframe is empty")
    
    if verbose:
        logger.info(f"Searching for {len(df)} datafiles in dataverse")

    # run the download wrapper for each entry in the dataframe
    for _, entry in df.iterrows():
        try:
            download_wrapper(entry, path, verbose=verbose)
        except Exception as e:
            if verbose:
                logger.error(f"Failed to download entry {entry.get('id', 'unknown')}: {e}")
            raise
    
    if verbose:
        logger.info(f"Download completed, saved to `{path}`")