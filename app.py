import sys
from app import app, CreateApp
from config import Config

if __name__ == "__main__":

    port = Config.PORT
    print("Starting license monitor service on port", port)

    app = CreateApp()
    app.run(host='0.0.0.0', port=port, debug=True)

# That's all!
