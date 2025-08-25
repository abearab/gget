> Python arguments are equivalent to long-option arguments (`--arg`), unless otherwise specified. Flags are True/False arguments in Python. The manual for any gget tool can be called from the command-line using the `-h` `--help` flag.  
# gget dataverse 🗄️
Download datasets from [Dataverse](https://dataverse.harvard.edu/) repositories using dataset IDs.  
Return format: Files downloaded to specified directory.

**Positional argument**  
`table`  
File containing the dataset IDs to download (CSV/TSV format). The file must contain the following columns:
- `id`: The unique identifier for the datafile in Dataverse
- `name`: The dataset name for the single file
- `type`: The file type (e.g., csv, tsv, pkl, tab)

**Optional arguments**  
`-o` `--out`    
Path to the directory where the datasets will be saved. Default: current working directory.

`-c` `--checksum`  
Verify MD5 checksums of downloaded files against remote checksums. This ensures file integrity by comparing the local file's checksum with the checksum stored in Dataverse. Note: This requires additional API calls and may slow down the process.

**Flags**   
`-q` `--quiet`   
Command-line only. Prevents progress information from being displayed.  
Python: Use `verbose=False` to prevent progress information from being displayed.

Python-only flags:  
`verify_checksum`  
Verify MD5 checksums of downloaded files against remote checksums. Default: False.
  
  
### Examples

**Download datasets from a CSV file**

```bash
gget dataverse datasets.csv
```

```python
import gget
gget.dataverse("datasets.csv")
```

Where `datasets.csv` contains:
```
id,name,type
6180617,protein_network_nodes,tab
6180618,protein_interactions,csv
```

&rarr; Downloads the specified datafiles from Dataverse to the current directory.

<br/><br/>

**Download datasets to a specific directory**

```bash
gget dataverse datasets.tsv -o /path/to/download/directory
```

```python
import gget
gget.dataverse("datasets.tsv", path="/path/to/download/directory")
```

&rarr; Downloads the specified datafiles from Dataverse to the specified directory.

<br/><br/>

**Download datasets using a DataFrame (Python only)**

```python
import gget
import pandas as pd

# Create DataFrame with dataset information
df = pd.DataFrame({
    'id': ['6180617', '6180618'],
    'name': ['protein_nodes', 'protein_edges'],
    'type': ['tab', 'csv']
})

gget.dataverse(df, path="./data")
```

&rarr; Downloads the specified datafiles from Dataverse using a pandas DataFrame.

<br/><br/>

**Download datasets with checksum verification**

```bash
gget dataverse datasets.csv --checksum
```

```python
import gget
gget.dataverse("datasets.csv", verify_checksum=True)
```

&rarr; Downloads the specified datafiles and verifies their MD5 checksums against the remote checksums stored in Dataverse to ensure file integrity.

<br/><br/>

### Notes

- Files are downloaded with progress bars showing download status
- If a file already exists locally, the download is skipped
- The module validates that the input table contains the required columns (`id`, `name`, `type`)
- Supports both CSV (comma-separated) and TSV (tab-separated) input files
- Error handling provides clear messages for common issues like missing files or invalid formats
- **Checksum verification**: When enabled, files are verified against their remote MD5 checksums stored in Dataverse. This feature:
  - Ensures downloaded files are complete and uncorrupted
  - Works for both newly downloaded files and existing local files  
  - Requires additional API calls to retrieve metadata
  - Shows verification results in the log output
  - Currently supports MD5 checksums only
