import sys
import os
from app import app
from config import Config

if __name__ == "__main__":

    port = 5000
    try:
        port = sys.argv[1]
    except:
        pass

    print("Starting FlexLM license monitor service on port %s with %s", (port,os.environ['LICENSE']))

    app.run(host='0.0.0.0', port=port, debug=True)

# That's all!
