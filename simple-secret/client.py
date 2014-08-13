from util import get_or_gen_gpg, generate_random_string
import getpass
import requests
import config


class Client(object):
    def __init__(self, host, port, passphrase):
        self.host = "{host}:{port}".format(host=host, port=port)
        self.passphrase = passphrase
        self.gpg, self.fp = get_or_gen_gpg(passphrase)
        self.server_fp = get_fp_from_gpg(self.gpg, Config.SERVER_KEY_ID)
        self.secret = generate_random_string()
        self.session = False

    def authenticate(self):
        if not self.secret:
            self.secret = generate_random_string()
        if not self.session:
            self._challenge_server()
        return self.secret

    def _challenge_server(self):
        url = self.host + "/authenticate/{}".format(self.fp)
        message = self._encrypt(self.secret, self.server_fp)
        response = request.post(url, data=payload)
        if response.ok:
            msg = json.loads(self._decrypt(response.text))
            if msg['key'] == self.secret:
                self.secret = msg['key2']
                self.session = True
            else:
                raise Exception('Bad Server Authentication')
        else:
            self.authenticate()

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

if __name__ == '__main__':
    passphrase = getpass.getpass(prompt = 'Passphrase: ')
    client = Client(config.MESSAGE_HOST, config.MESSAGE_PORT, passphrase)
    client.get_messages()
