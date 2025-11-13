import pandas as pd
from pathlib import Path
import pyarrow.parquet as pq
import pyarrow as pa
from tqdm import tqdm
import os

# Configuration
ROOT_DIR = Path('').resolve()
DATA_DIR = ROOT_DIR / 'data'
CSV_FILE = DATA_DIR / 'b0cd514b-b9cc-4972-a0c2-c91726e6d825.csv'
PARQUET_FILE = DATA_DIR / 'data.parquet'
CSV_DELIMITER = ','
CHUNK_SIZE = 100000  # Adjust based on your system's memory

def convert_csv_to_parquet():
    """
    Convert a large CSV file to Parquet format in chunks.
    """
    if PARQUET_FILE.exists():
        print(f"Parquet file already exists at {PARQUET_FILE}")
        return
    
    print(f"Converting {CSV_FILE} to Parquet format...")
    
    # Get the total number of rows for progress tracking
    total_rows = sum(1 for _ in open(CSV_FILE, 'r', encoding='utf-8')) - 1  # Subtract header
    
    # Create a Parquet writer object
    parquet_writer = None
    
    # Read and process the CSV in chunks
    n_chunks = total_rows // CHUNK_SIZE + 1
    for i, chunk in enumerate(tqdm(
        pd.read_csv(CSV_FILE, delimiter=CSV_DELIMITER, chunksize=CHUNK_SIZE),
        total=(total_rows // CHUNK_SIZE) + 1,
        desc="Processing chunks"
    )):
        print(f"Processing chunk {i+1}/{n_chunks}")
        # Convert the chunk to a PyArrow table
        table = pa.Table.from_pandas(chunk)
        
        # Write the first chunk with the schema
        if i == 0:
            parquet_writer = pq.ParquetWriter(
                PARQUET_FILE,
                table.schema,
                compression='snappy',
                version='2.6'
            )
        
        # Write the chunk to the Parquet file
        parquet_writer.write_table(table)
    
    # Close the Parquet writer
    if parquet_writer:
        parquet_writer.close()
    
    print(f"Successfully converted to {PARQUET_FILE}")
    print(f"Original CSV size: {os.path.getsize(CSV_FILE) / (1024**2):.2f} MB")
    print(f"Parquet file size: {os.path.getsize(PARQUET_FILE) / (1024**2):.2f} MB")

if __name__ == "__main__":
    # Create necessary directories if they don't exist
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    # Convert the CSV file to Parquet
    convert_csv_to_parquet()

