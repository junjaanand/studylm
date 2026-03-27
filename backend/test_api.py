import requests
import json
import os

BASE_URL = "http://localhost:8000/api"

# 1. Create a dummy text file
with open("test_doc.txt", "w") as f:
    f.write("Artificial intelligence (AI) is intelligence demonstrated by machines, as opposed to the natural intelligence displayed by animals including humans. AI research has been defined as the field of study of intelligent agents, which refers to any system that perceives its environment and takes actions that maximize its chance of achieving its goals.")

print("Uploading document...")
with open("test_doc.txt", "rb") as f:
    files = {"file": ("test_doc.txt", f, "text/plain")}
    res = requests.post(f"{BASE_URL}/documents/upload", files=files)

print("Upload Response:", res.status_code)
if res.status_code == 200:
    doc_id = res.json()["id"]
    print("Upload SUCCESS! Document ID:", doc_id)
    
    print("\nTesting Chat Q&A...")
    chat_payload = {"document_id": doc_id, "question": "What is AI?"}
    chat_res = requests.post(f"{BASE_URL}/chat/ask", json=chat_payload)
    print("Chat Response:", chat_res.status_code)
    try:
        print("Chat Content:", chat_res.json()["answer"])
    except:
        print("Raw Chat Content:", chat_res.text)
else:
    print("Upload FAILED:", res.text)
