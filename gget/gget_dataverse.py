import os
import hashlib
import requests
from tqdm import tqdm
import pandas as pd
from .utils import set_up_logger
from .constants import DATAVERSE_GET_URL

logger = set_up_logger()

def calculate_md5_checksum(file_path):
    """Calculate MD5 checksum of a local file
    
    Args:
        file_path (str): path to the local file
        
    Returns:
        str: MD5 checksum as hexadecimal string
    """
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except OSError as e:
        raise RuntimeError(f"Failed to calculate checksum for {file_path}: {e}")


def get_file_metadata(file_id):
    """Get file metadata from Dataverse API including checksum
    
    Args:
        file_id (str or int): the file ID in Dataverse
        
    Returns:
        dict: metadata containing checksum info, or None if unavailable
    """
    metadata_url = f"https://dataverse.harvard.edu/api/files/{file_id}/metadata"
    try:
        response = requests.get(metadata_url, timeout=30)
        response.raise_for_status()
        metadata = response.json()
        
        # Extract checksum information if available
        if "data" in metadata and isinstance(metadata["data"], dict):
            data = metadata["data"]
            if "checksum" in data:
                return {
                    "checksum_type": data["checksum"].get("type"),
                    "checksum_value": data["checksum"].get("value"),
                    "filesize": data.get("filesize")
                }
    except (requests.exceptions.RequestException, KeyError, ValueError) as e:
        logger.warning(f"Could not retrieve metadata for file {file_id}: {e}")
    
    return None


def verify_file_checksum(file_path, file_id, verbose=True):
    """Verify that a local file matches its remote checksum
    
    Args:
        file_path (str): path to the local file
        file_id (str or int): the file ID in Dataverse
        verbose (bool): whether to log verification results
        
    Returns:
        bool: True if checksum matches or verification not possible, False if mismatch
    """
    if not os.path.exists(file_path):
        if verbose:
            logger.error(f"File {file_path} not found for checksum verification")
        return False
    
    # Get remote metadata
    metadata = get_file_metadata(file_id)
    if not metadata or not metadata.get("checksum_value"):
        if verbose:
            logger.info(f"Checksum not available for file {file_id}, skipping verification")
        return True  # Return True if verification is not possible
    
    checksum_type = metadata.get("checksum_type", "").upper()
    remote_checksum = metadata.get("checksum_value", "").lower()
    
    # Currently only support MD5
    if checksum_type != "MD5":
        if verbose:
            logger.info(f"Unsupported checksum type '{checksum_type}' for file {file_id}, skipping verification")
        return True
    
    # Calculate local checksum
    try:
        local_checksum = calculate_md5_checksum(file_path)
        
        if local_checksum == remote_checksum:
            if verbose:
                logger.info(f"✓ Checksum verified for {os.path.basename(file_path)}")
            return True
        else:
            if verbose:
                logger.error(f"✗ Checksum mismatch for {os.path.basename(file_path)}")
                logger.error(f"  Expected: {remote_checksum}")
                logger.error(f"  Got:      {local_checksum}")
            return False
            
    except Exception as e:
        if verbose:
            logger.error(f"Failed to verify checksum for {file_path}: {e}")
        return False

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


def download_wrapper(entry, path, return_type=None, verify_checksum=False, verbose=True):
    """wrapper for downloading a dataset given the name and path, for csv,pkl,tsv or similar files

    Args:
        entry (dict): the entry of the dataset to download. Must include 'id', 'name', 'type' keys
        path (str): the path to save the dataset locally
        return_type (str, optional): the return type. Defaults to None. Can be "url", "filename", or ["url", "filename"]
        verify_checksum (bool): whether to verify file checksum after download. Default: False
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
    file_path = os.path.join(path, filename)

    # Check if file already exists
    file_exists = os.path.exists(file_path)
    should_verify = verify_checksum and file_exists

    if file_exists:
        if verbose:
            logger.info(f"Found local copy for {entry['id']} datafile as {filename}")
    else:
        if verbose:
            logger.info(f"Downloading {entry['id']} datafile as {filename}")
        dataverse_downloader(url, path, filename, verbose)
        should_verify = verify_checksum  # Always verify after fresh download

    # Verify checksum if requested
    if should_verify:
        if not verify_file_checksum(file_path, entry['id'], verbose):
            if verbose:
                logger.warning(f"Checksum verification failed for {filename}")
            # Note: We don't raise an error here to allow users to decide what to do
    
    if return_type == "url":
        return url
    elif return_type == "filename":
        return filename
    elif return_type == ["url", "filename"]:
        return url, filename


def dataverse(df, path=".", sep=",", verify_checksum=False, verbose=True):
    """download datasets from dataverse for a given dataframe
    Input dataframe must have 'name', 'id', 'type' columns.
    - 'name' is the dataset name for single file
    - 'id' is the unique identifier for the file
    - 'type' is the file type (e.g. csv, tsv, pkl)

    Args:
        df (pd.DataFrame or str): the dataframe or path to the csv/tsv file
        path (str): the path to save the dataset locally. Default: current working directory
        sep (str): separator for CSV/TSV files. Default: ","
        verify_checksum (bool): whether to verify file checksums after download. Default: False
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
        if verify_checksum:
            logger.info("Checksum verification enabled")

    # run the download wrapper for each entry in the dataframe
    for _, entry in df.iterrows():
        try:
            download_wrapper(entry, path, verify_checksum=verify_checksum, verbose=verbose)
        except Exception as e:
            if verbose:
                logger.error(f"Failed to download entry {entry.get('id', 'unknown')}: {e}")
            raise
    
    if verbose:
        logger.info(f"Download completed, saved to `{path}`")