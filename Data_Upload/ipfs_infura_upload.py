import requests
import json

def upload_file_to_ipfs_infura(file_path, infura_api_key):
  """Uploads a file to IPFS using Infura.

  Args:
    file_path: The path to the file to upload.
    infura_api_key: The Infura API key.

  Returns:
    The IPFS hash of the uploaded file.
  """

  with open(file_path, "rb") as f:
    file_data = f.read()

  headers = {
    "Authorization": f"Bearer {infura_api_key}"
  }

  files = {
    "file": file_data
  }

  response = requests.post(
    "https://ipfs.infura.io/v0/add",
    headers=headers,
    files=files
  )

  response.raise_for_status()

  data = json.loads(response.content)

  return data["Hash"]


# Example usage:

file_path = "/path/to/file.txt"
infura_api_key = "YOUR_INFURA_API_KEY"

ipfs_hash = upload_file_to_ipfs_infura(file_path, infura_api_key)

print(ipfs_hash)
