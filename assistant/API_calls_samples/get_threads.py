import requests as req

url = "https://api.openai.com/v1/threads"
headers = {
    "Authorization": f"Bearer sess-d4LXCiLr66yQKOjLM7Px4uJld2L82CSCNEMmC2pS", 
    # "Openai-Organization": f"{org}", 
    "OpenAI-Beta": "assistants=v1"
}

resp = req.get(url, headers=headers)
print(resp)