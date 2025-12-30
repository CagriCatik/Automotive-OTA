import requests
import hashlib
import os
import logging

class ArtifactDownloader:
    def download(self, url, target_path, expected_hash, expected_size):
        if os.path.exists(target_path):
            # Simple resume check: if size matches, assume good (in prod verify hash)
            if os.path.getsize(target_path) == expected_size:
                logging.info(f"Artifact {target_path} already exists. Verifying...")
                if self.verify_hash(target_path, expected_hash):
                    return True
        
        logging.info(f"Downloading {url} to {target_path}...")
        try:
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                with open(target_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            
            return self.verify_hash(target_path, expected_hash)
        except Exception as e:
            logging.error(f"Download failed: {e}")
            return False

    def verify_hash(self, path, expected_hash):
        if expected_hash is None:
            return True
        sha256 = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
        calc_hash = sha256.hexdigest()
        if calc_hash == expected_hash:
            logging.info(f"Hash verified for {path}")
            return True
        else:
            logging.error(f"Hash mismatch! Expected {expected_hash}, got {calc_hash}")
            return False
