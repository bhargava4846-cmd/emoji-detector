import chromadb
from emoji_data import EMOJI_DATA

# ChromaDB saves its data to this folder (auto-created on first run)
_client = chromadb.PersistentClient(path="./.chroma")


def _get_collection():
    collection = _client.get_or_create_collection(
        name="emojis",
        metadata={"hnsw:space": "cosine"}
    )

    # Only populate on first run (when collection is empty)
    if collection.count() == 0:
        print("Building emoji database for the first time — this takes a few seconds...")

        documents = []
        metadatas = []
        ids = []

        for i, item in enumerate(EMOJI_DATA):
            # Combine all text fields so ChromaDB can search by meaning
            document = f"{item['name']}. Emotions: {item['emotions']}. Tags: {item['tags']}"
            documents.append(document)
            metadatas.append({
                "emoji": item["emoji"],
                "name": item["name"],
                "content_rating": item["content_rating"]
            })
            ids.append(f"emoji_{i}")

        collection.add(documents=documents, metadatas=metadatas, ids=ids)
        print(f"Loaded {len(EMOJI_DATA)} emojis into the database.")

    return collection


def find_relevant_emojis(text: str, safe_search: bool = True, n_results: int = 10):
    collection = _get_collection()

    results = collection.query(
        query_texts=[text],
        n_results=min(n_results, collection.count())
    )

    emojis = []
    for metadata in results["metadatas"][0]:
        if safe_search and metadata["content_rating"] == "adult":
            continue
        emojis.append(metadata)

    return emojis
