import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


current_dir = Path.cwd()
sys.path.insert(0, str(current_dir))

from pageindex import PageIndexClient
from pageindex.utils import ConfigLoader

PDF_FOLDER = current_dir / "files_pdf"
WORKSPACE = current_dir / "workspace"
LOG_DIR = current_dir / "logs"

# Assicurati che le cartelle esistano
PDF_FOLDER.mkdir(parents=True, exist_ok=True)
WORKSPACE.mkdir(parents=True, exist_ok=True)


def run_local_indexing():
    # Inizializza il client SOLO con il workspace.
    # La chiave API verrà presa in automatico dal file .env grazie a utils.py
    client = PageIndexClient(workspace=str(WORKSPACE))

    print(f"model: {client.model}")
    print(f"documents directory: {PDF_FOLDER}")
    print(f"workspace: {WORKSPACE}")

    pdf_files = list(PDF_FOLDER.glob("*.pdf"))

    if not pdf_files:
        print(f"no pdfs in {PDF_FOLDER}")
        return

    for pdf_path in pdf_files:
        already_indexed = False
        for doc_id, info in client.documents.items():
            if info.get('doc_name') == pdf_path.name:
                print(f"[{pdf_path.name}] already indexded ID: {doc_id}")
                already_indexed = True
                break

        if already_indexed:
            continue

        print(f"indexing: {pdf_path.name}...")
        try:
            doc_id = client.index(str(pdf_path))
            print(f"done, doc id: {doc_id}")
        except Exception as e:
            print(f"error {pdf_path.name}: {e}")

    print(f" {len(client.documents)} documents loaded")


if __name__ == "__main__":
    run_local_indexing()