import ssl
import sys

import tools

from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/<query>')
def query(query:str):
    rc= tools.queryPixabay(query)
    return jsonify(rc)


if __name__ == '__main__':
    _port=5600
    if "debug" in sys.argv:
        app.run(host="0.0.0.0",port=_port,debug=True)
    else:
        if "ssl" in sys.argv:
            print("Activation du ssl")
            context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            context.load_cert_chain("/app/certs/fullchain.pem", "/app/certs/privkey.pem")
            app.run(host="0.0.0.0", port=_port, debug=False, ssl_context=context)
        else:
            app.run(host="0.0.0.0", port=_port, debug=False)



