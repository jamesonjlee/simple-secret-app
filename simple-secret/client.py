from util import get_or_gen_gpg
import getpass
import requests

MESSAGE_HOST = 'http://127.0.0.1'
MESSAGE_PORT = 12345

class Client(object):
    def __init__(self, host, port, passphrase):
        self.host = "{host}:{port}".format(host=host, port=port)
        self.passphrase = passphrase
        self.gpg, self.fp = get_or_gen_gpg(passphrase)
        self.secret = ''

    def authenticate(self):
        if not self.secret:
            pass

    def get_messages(self):
        url = self.host + "/message/{}".format(self.fp)
        resp = requests.get(url, auth=(self.secret, ''))
        decrypted = []
        for message in resp.json():
            decrypted.append(self._decrypt(message))
        print decrypted

    def send_message(self, message):
        url = self.host + "/message/{}".format(self.fp)
        encrypted_message = self._encrypt(message)
        payload = json.dumps(encrypted_message)
        resp = requests.post(url, payload=payload, auth=Basic(self.secret, ''))
        print resp.json()

    def _encrypt(self, message, recipient):
        encrypted_data = self.gpg.encrypt(
            message,
            recipients=[recipient],
            sign=self.fp,
            passphrase=passphrase)
        return encrypted_data

    def _decrypt(self, message):
        decrypted_data = gpg.decrypt(
            str(encrypted_data),
            passphrase=passphrase)
        return decrypted_data

passphrase = getpass.getpass(prompt = 'Passphrase: ')
client = Client(MESSAGE_HOST, MESSAGE_PORT, passphrase)
client.get_messages()
