import sys
from app import app
from config import Config

if __name__ == "__main__":

    port = Config.PORT
    print("Starting license monitor service on port", port)
    app.run(host='0.0.0.0', port=port, debug=True)

# That's all!
