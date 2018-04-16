import os
from app import app
from intro_to_flask import app

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=True, port=port, host='0.0.0.0')
#     print("Starting app on port %d" % port)