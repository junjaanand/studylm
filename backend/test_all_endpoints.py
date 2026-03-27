import requests

BASE_URL = "http://localhost:8000/api"

# Get the latest document ID
docs_res = requests.get(f"{BASE_URL}/documents/")
docs = docs_res.json()
if not docs:
    print("No documents found. Please upload one first.")
    exit(1)

doc_id = docs[0]["id"]
print(f"Using document ID: {doc_id}")

endpoints = [
    ("/notes/generate", {"document_id": doc_id, "topic": "General"}),
    ("/mcq/generate", {"document_id": doc_id, "num_questions": 3}),
    ("/summary/generate", {"document_id": doc_id}),
    ("/flashcards/generate", {"document_id": doc_id, "num_cards": 3}),
    ("/quiz/start", {"document_id": doc_id, "num_questions": 3}),
    ("/chat/ask", {"document_id": doc_id, "question": "What is AI?"})
]

for url, payload in endpoints:
    print(f"\n--- Testing {url} ---")
    try:
        res = requests.post(f"{BASE_URL}{url}", json=payload)
        print("Status code:", res.status_code)
        if res.status_code != 200:
            print("Error:", res.text)
        else:
            print("Success!")
            print(res.text[:100] + "...")
    except Exception as e:
        print("Exception:", e)
