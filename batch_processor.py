import os
from pathlib import Path
from pageindex.client import PageIndexClient


def build_pageindex_workspace(input_folder: str, model_name: str, workspace_path: str, verbose=False, force=False):
    client = PageIndexClient(
        model=model_name,
        workspace=workspace_path
    )

    if verbose:
        print("Starting processing...")

    indexed_files = set()
    for doc in client.documents.values():
        if 'path' in doc:
            indexed_files.add(os.path.abspath(doc['path']))

    input_dir = Path(input_folder)

    for file_path in input_dir.iterdir():
        if file_path.suffix.lower() in ['.pdf', '.md', '.markdown']:
            abs_path = os.path.abspath(file_path)

            is_indexed = abs_path in indexed_files

            if is_indexed and not force:
                if verbose:
                    print(f"Skipped {file_path.name} (already indexed).")
                continue

            if verbose:
                action = "Re-indexing" if is_indexed else "Generating tree for"
                print(f"{action} {file_path.name}...")

            try:
                doc_id = client.index(str(file_path))
                if verbose:
                    print(f"Done! Doc ID: {doc_id}")
            except Exception as e:
                print(f"Error {file_path.name}: {e}")



build_pageindex_workspace(
    input_folder="./examples/documents/test",
    model_name="gpt-5-mini",
    # model_name="gemma4:e4b",
    workspace_path="./workspace_test",
    force=True
)