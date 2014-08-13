import getpass
import requests
import config
import util
from flask import json


class Client(object):
    def __init__(self, host, port, passphrase):
        self.host = "{host}:{port}".format(host=host, port=port)
        self.passphrase = passphrase
        self.gpg, self.fp = util.get_or_gen_gpg(passphrase, config.CLIENT_GPG_HOME)
        self.server_fp = config.SERVER_KEY_FP
        self.secret = util.generate_random_string()
        self.session = False

    def authenticate(self):
        if not self.secret:
            self.secret = util.generate_random_string()
        if not self.session:
            self._challenge_server()
        return self.secret

    def _challenge_server(self):
        url = self.host + "/authenticate/{}".format(self.fp)
        message = str(self._encrypt(self.secret, self.server_fp))
        response = requests.post(url, data=message)
        if response.ok:
            msg = json.loads(str(self._decrypt(response.text)))
            if msg['key'] == self.secret:
                self.secret = msg['key2']
                self.session = True
                return self.secret
        else:
        #self.authenticate()
            raise Exception('Bad Server Authentication')

    def get_messages(self):
        self._challenge_server()
        url = self.host + "/message/{}".format(self.fp)
        resp = requests.get(url, auth=(self.secret, ''))
        decrypted = []
        for message in resp.json():
            decrypted.append(self._decrypt(message))
        print decrypted

    def send_message(self, message):
        self._challenge_server()
        url = self.host + "/message/{}".format(self.fp)
        encrypted_message = self._encrypt(message, self.server_fp)
        payload = json.dumps(encrypted_message)
        resp = requests.post(url, payload=payload, auth=Basic(self.secret, ''))
        print resp.json()

    def _encrypt(self, message, recipient):
        encrypted_data = util.gpg_encrypt(
            self.gpg,
            sender=self.fp,
            message=message,
            recipient=recipient,
            passphrase=self.passphrase
        )
        return encrypted_data

    def _decrypt(self, message):
        decrypted_data = util.gpg_decrypt(
            self.gpg,
            str(message),
            passphrase=self.passphrase)
        return decrypted_data

if __name__ == '__main__':
    passphrase = getpass.getpass(prompt = 'Passphrase: ')
    client = Client(config.MESSAGE_HOST, config.MESSAGE_PORT, passphrase)
    client.get_messages()
