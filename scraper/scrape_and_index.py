import os
import time
import requests
from elasticsearch import Elasticsearch, helpers


ES_URL = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")
ES_INDEX = os.getenv("ES_INDEX", "products")


def es_client():
    return Elasticsearch([ES_URL])


def ensure_index(es):
    if es.indices.exists(index=ES_INDEX):
        return
    es.indices.create(
        index=ES_INDEX,
        body={
            "settings": {
                "analysis": {"analyzer": {"default": {"type": "standard"}}}
            },
            "mappings": {
                "properties": {
                    "title": {"type": "text", "fields": {"raw": {"type": "keyword"}}},
                    "description": {"type": "text"},
                    "category": {"type": "keyword"},
                    "price": {"type": "float"},
                    "url": {"type": "keyword", "index": False},
                    "image_url": {"type": "keyword", "index": False},
                    "source": {"type": "keyword"},
                    "source_id": {"type": "keyword"}
                }
            },
        },
    )


def fetch_products():
    # Public sample dataset of products
    url = "https://dummyjson.com/products?limit=200"
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    products = data.get("products", [])
    for p in products:
        yield {
            "_index": ES_INDEX,
            "_id": f"dummy-{p['id']}",
            "_source": {
                "title": p.get("title"),
                "description": p.get("description"),
                "category": p.get("category"),
                "price": float(p.get("price", 0)),
                "url": f"https://dummyjson.com/products/{p['id']}",
                "image_url": (p.get("thumbnail") or (p.get("images") or [None])[0]),
                "source": "dummyjson",
                "source_id": str(p.get("id")),
            },
        }


def main():
    es = es_client()
    # Wait for ES to come up in Docker scenarios
    for i in range(30):
        try:
            if es.ping():
                break
        except Exception:
            pass
        time.sleep(1)

    ensure_index(es)
    actions = list(fetch_products())
    helpers.bulk(es, actions)
    print(f"Indexed {len(actions)} products into '{ES_INDEX}' at {ES_URL}")


if __name__ == "__main__":
    main()

