import gzip
import shutil
import os
import pandas as pd

def process_tox21():
    gz_path = os.path.join(os.path.dirname(__file__), 'tox21.csv.gz')
    csv_path = os.path.join(os.path.dirname(__file__), 'tox21.csv')
    
    if os.path.exists(gz_path):
        print(f"Unzipping {gz_path}...")
        try:
            with gzip.open(gz_path, 'rb') as f_in:
                with open(csv_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            print(f"Unzipped to {csv_path}")
            
            # Now load and keep 100%
            df = pd.read_csv(csv_path)
            print(f"Original Row Count: {len(df)}")
            
            # Use all labels for training
            toxicity_cols = [c for c in df.columns if c != 'smiles' and c != 'mol_id']
            df['toxicity'] = df[toxicity_cols].any(axis=1).astype(int)
            
            final_df = df[['smiles', 'toxicity']]
            output_path = os.path.join(os.path.dirname(__file__), 'tox21_full.csv')
            final_df.to_csv(output_path, index=False)
            print(f"Final full dataset (100%) saved with {len(final_df)} rows.")
            return True
        except Exception as e:
            print(f"Error processing data: {e}")
            return False
    else:
        print("GZ file not found.")
        return False

if __name__ == "__main__":
    process_tox21()
