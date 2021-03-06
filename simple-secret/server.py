from flask import Flask, json, g, request
from flask.ext.sqlalchemy import SQLAlchemy
import config
import util
import itsdangerous

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)
passphrase = config.SERVER_PASSPHRASE


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipient = db.Column(db.String(128), index=True, nullable=False)
    message = db.Column(db.Text, nullable=False)

    def __init__(self, recipient, message):
        self.recipient = recipient
        self.message = message

class PubKey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fingerprint = db.Column(db.String(128), index=True, nullable=False)
    pub_key = db.Column(db.Text, nullable=False)

    def __init__(self, fingerprint, pub_key):
        self.fingerprint = fingerprint
        self.pub_key = pub_key

@app.route('/message/<string:recipient_id>', methods=['GET'])
def get_message_by_sig(recipient_id):
    messages = Message.query.filter(Message.recipient == recipient_id).all()
    return json.dumps([msg.message for msg in messages]), 200

@app.route('/message/<string:recipient_id>', methods=['POST'])
def add_message_by_sig(recipient_id):
    message = request.form.get('message')
    message = Message(recipient=recipient_id, message=message)
    db.session.add(message)
    db.session.commit()
    return 'OK', 200

@app.route('/authenticate/<string:recipient_id>', methods=['POST'])
def authenticate_person(recipient_id):
    key = util.gpg_decrypt(app.gpg, request.data, config.SERVER_PASSPHRASE)
    key2 = util.generate_random_string(32)
    body = {
        'key': str(key),
        'key2': key2
    }
    msg = json.dumps(body)
    server_fp = util.get_fp_from_gpg(app.gpg, config.SERVER_KEY_FP)
    encrypted = util.gpg_encrypt(
        app.gpg,
        server_fp,
        msg,
        recipient_id,
        config.SERVER_PASSPHRASE)
    return str(encrypted), 200

@app.route('/identify/<string:fingerprint>', methods=['GET'])
def get_fingerprint_pub_key(fingerprint):
    pub_key = PubKey.query.filter(PubKey.fingerprint==fingerprint).first()
    if pub_key:
        return pub_key.pub_key, '200'
    else:
        return 'Unknown Fingerprint', 404

@app.route('/identify/<string:fingerprint>', methods=['POST'])
def add_fingerprint_pub_key(fingerprint):
    pub_key = PubKey(fingerprint, request.form.get('keyfile'))
    db.session.add(pub_key)
    db.session.commit()
    return 'OK', 200

@app.before_first_request
def register_self_gpg(*arg, **kwargs):
    app.gpg, app.fp = util.get_or_gen_gpg(passphrase, config.SERVER_GPG_HOME)

if __name__ == '__main__':
    db.create_all()
    app.run(host='127.0.0.1', port=12345)
