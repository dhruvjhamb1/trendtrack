import os
import sys

# Add the social_media_insights directory to Python path
sys.path.append(os.path.abspath("trendtrack"))

from app import app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port) 