#!/usr/bin/env python3
"""
Add GitHub Secret via API

This script adds the OLLAMA_PROXY_API_KEY secret to the GrumpiBlogged repository.

Requirements:
- PyNaCl: pip install PyNaCl
- GitHub Personal Access Token with 'repo' scope

Usage:
    python add_github_secret.py
"""

import base64
import requests
from nacl import encoding, public


def get_public_key(owner, repo, token):
    """Get the repository's public key for encrypting secrets"""
    url = f"https://api.github.com/repos/{owner}/{repo}/actions/secrets/public-key"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def encrypt_secret(public_key: str, secret_value: str) -> str:
    """Encrypt a secret using the repository's public key"""
    public_key_bytes = base64.b64decode(public_key)
    sealed_box = public.SealedBox(public.PublicKey(public_key_bytes))
    encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
    return base64.b64encode(encrypted).decode("utf-8")


def create_or_update_secret(owner, repo, token, secret_name, secret_value):
    """Create or update a repository secret"""
    # Get public key
    public_key_data = get_public_key(owner, repo, token)
    
    # Encrypt the secret
    encrypted_value = encrypt_secret(public_key_data["key"], secret_value)
    
    # Create/update the secret
    url = f"https://api.github.com/repos/{owner}/{repo}/actions/secrets/{secret_name}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    data = {
        "encrypted_value": encrypted_value,
        "key_id": public_key_data["key_id"]
    }
    
    response = requests.put(url, headers=headers, json=data)
    response.raise_for_status()
    
    return response.status_code


def main():
    """Main function"""
    print("🔐 GitHub Secret Setup for GrumpiBlogged")
    print("=" * 60)
    
    # Configuration
    OWNER = "Grumpified-OGGVCT"
    REPO = "GrumpiBlogged"
    SECRET_NAME = "OLLAMA_PROXY_API_KEY"
    SECRET_VALUE = "op_2e0efc5f37c6c1b4_da2701b13246163ae6c8f4ece6d0e5f9082b9ac1849f7109"
    
    # Get GitHub token
    print("\n📝 You need a GitHub Personal Access Token with 'repo' scope")
    print("   Create one at: https://github.com/settings/tokens/new")
    print("   Required scopes: repo (Full control of private repositories)")
    print()
    
    token = input("Enter your GitHub Personal Access Token: ").strip()
    
    if not token:
        print("❌ No token provided. Exiting.")
        return 1
    
    try:
        print(f"\n🔑 Adding secret '{SECRET_NAME}' to {OWNER}/{REPO}...")
        
        status_code = create_or_update_secret(
            owner=OWNER,
            repo=REPO,
            token=token,
            secret_name=SECRET_NAME,
            secret_value=SECRET_VALUE
        )
        
        if status_code in [201, 204]:
            print(f"✅ Secret '{SECRET_NAME}' added successfully!")
            print(f"\n📍 Verify at: https://github.com/{OWNER}/{REPO}/settings/secrets/actions")
            print("\n🎉 Next steps:")
            print("   1. Verify the secret appears in repository settings")
            print("   2. Trigger a test workflow run")
            print("   3. Check workflow logs for AI editing output")
            return 0
        else:
            print(f"⚠️  Unexpected status code: {status_code}")
            return 1
    
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error: {e}")
        print(f"   Response: {e.response.text}")
        return 1
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())

