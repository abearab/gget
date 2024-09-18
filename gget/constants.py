import uuid

# Ensembl REST API server for gget seq and info
ENSEMBL_REST_API = "http://rest.ensembl.org/"
ENSEMBL_FTP_URL = "http://ftp.ensembl.org/pub/"
ENSEMBL_FTP_URL_GRCH37 = "http://ftp.ensembl.org/pub/grch37/"
# Non-vertebrate server
ENSEMBL_FTP_URL_NV = "http://ftp.ensemblgenomes.org/pub/"

# NCBI URL for gget info
NCBI_URL = "https://www.ncbi.nlm.nih.gov"

# UniProt REST API server for gget seq and info
UNIPROT_REST_API = "https://rest.uniprot.org/uniprotkb/search?query="
UNIPROT_IDMAPPING_API = "https://rest.uniprot.org/idmapping"

# RCSB PDB API for gget pdb
RCSB_PDB_API = "https://data.rcsb.org/rest/v1/core/"

# API to get PDB entries from Ensembl IDs
ENS_TO_PDB_API = "https://www.ebi.ac.uk/pdbe/aggregated-api/mappings/ensembl_to_pdb/"

# BLAST API endpoints
BLAST_URL = "https://blast.ncbi.nlm.nih.gov/Blast.cgi"
# Generate a random UUID
BLAST_CLIENT = "gget_client-" + str(uuid.uuid4())

# MUSCLE Github repo
MUSCLE_GITHUB_LINK = "https://github.com/rcedgar/muscle.git"

# Enrichr API endpoints
POST_ENRICHR_URL = "https://maayanlab.cloud/speedrichr/api/addList"
GET_ENRICHR_URL = "https://maayanlab.cloud/speedrichr/api/enrich"
POST_BACKGROUND_ID_ENRICHR_URL = "https://maayanlab.cloud/speedrichr/api/addbackground"
GET_BACKGROUND_ENRICHR_URL = "https://maayanlab.cloud/speedrichr/api/backgroundenrich"

# ARCHS4 API endpoints
GENECORR_URL = "https://maayanlab.cloud/matrixapi/coltop"
EXPRESSION_URL = "https://maayanlab.cloud/archs4/search/loadExpressionTissue.php?"

# Download links for ELM database
ELM_INSTANCES_FASTA_DOWNLOAD = (
    "http://elm.eu.org/instances.fasta?q=*&taxon=&instance_logic="
)
ELM_INSTANCES_TSV_DOWNLOAD = (
    "http://elm.eu.org/instances.tsv?q=*&taxon=&instance_logic="
)
ELM_CLASSES_TSV_DOWNLOAD = "http://elm.eu.org/elms/elms_index.tsv"
ELM_INTDOMAINS_TSV_DOWNLOAD = "http://elm.eu.org/interactiondomains.tsv"

# COSMIC API endpoint
COSMIC_GET_URL = "https://cancer.sanger.ac.uk/cosmic/search/"
COSMIC_RELEASE_URL = "https://cancer.sanger.ac.uk/cosmic/release_notes"

# Codon to amino acid mapping
CODON_TABLE = {
    'TTT': 'F', 'TTC': 'F', 'TTA': 'L', 'TTG': 'L',
    'CTT': 'L', 'CTC': 'L', 'CTA': 'L', 'CTG': 'L',
    'ATT': 'I', 'ATC': 'I', 'ATA': 'I', 'ATG': 'M',
    'GTT': 'V', 'GTC': 'V', 'GTA': 'V', 'GTG': 'V',
    'TCT': 'S', 'TCC': 'S', 'TCA': 'S', 'TCG': 'S',
    'CCT': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
    'ACT': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T',
    'GCT': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',
    'TAT': 'Y', 'TAC': 'Y', 'TAA': '*', 'TAG': '*',
    'CAT': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q',
    'AAT': 'N', 'AAC': 'N', 'AAA': 'K', 'AAG': 'K',
    'GAT': 'D', 'GAC': 'D', 'GAA': 'E', 'GAG': 'E',
    'TGT': 'C', 'TGC': 'C', 'TGA': '*', 'TGG': 'W',
    'CGT': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R',
    'AGT': 'S', 'AGC': 'S', 'AGA': 'R', 'AGG': 'R',
    'GGT': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G',
    '---': '-'
}
