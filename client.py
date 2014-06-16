import gnupg
import getpass
import os

# pylint: disable-msg=C0103

# config
GPG_HOME = './gpg'
#GPG_PUB_KEY = './gpg_pub_key'
#GPG_PRIV_KEY = './gpg_priv_key'

GENERATE_KEYS = not os.path.isdir(GPG_HOME)
#GENERATE_KEYS = not os.path.isfile(GPG_PRIV_KEY)
gpg = gnupg.GPG(gnupghome=GPG_HOME)

def gen_key_info(name, email, passphrase):
    GPG_KEY_TYPE = 'RSA'
    GPG_KEY_LENGTH = 4096

    input_data = gpg.gen_key_input(
        key_type=GPG_KEY_TYPE,
        key_length=GPG_KEY_LENGTH,
        name_real=name,
        name_email=email,
        name_comment='Autogenerated Key',
        #subkey_type=GPG_KEY_TYPE,
        #subkey_length=GPG_KEY_LENGTH,
        expire_date=0,
        passphrase=passphrase,
        )
    return input_data

if GENERATE_KEYS:
    passphrase = getpass.getpass(prompt = 'Passphrase: ')
    key_info = gen_key_info(
        name='User Example',
        email='user@example.com',
        passphrase=passphrase,
        )

    print('Generating Key, go do something random...')
    key = gpg.gen_key(key_info)

    # export the two ASCII keys
    #public_key = gpg.export_keys(key.fingerprint)
    #private_key = gpg.export_keys(key.fingerprint, True)
    #pub_key_file = open(GPG_PUB_KEY, mode='w').write(public_key)
    #priv_key_file = open(GPG_PRIV_KEY, mode='w').write(private_key)
    #self_key = key
    self_fp = key.fingerprint
else:
    passphrase = getpass.getpass('Passphrase: ')
    self_fp = gpg.list_keys(secret=True)[0]['fingerprint']
    #pub_key_file = open(GPG_PUB_KEY, mode='r').read()
    #gpg.import_keys(pub_key_file)
    #priv_key_file = open(GPG_PRIV_KEY, mode='r').read()
    #res = gpg.import_keys(pub_key_file)
    #self_key = res.key

# now you can do stuff with gpg
# encrypt and sign
encrypted_data = gpg.encrypt('stuff to encrypt', recipients=[self_fp], sign=self_fp, passphrase=passphrase)
print encrypted_data

# decrypt and verify
def print_info(decrypted):
    print('User name: %s' % decrypted.username)
    print('Key id: %s' % decrypted.key_id)
    print('Signature id: %s' % decrypted.signature_id)
    #print('Signature timestamp: %s' % decrypted.sig_timestamp)
    print('Fingerprint: %s' % decrypted.fingerprint)
    print('Trust level: %s' % decrypted_data.trust_text)
    print('Data: %s' % decrypted)

decrypted_data = gpg.decrypt(str(encrypted_data), passphrase=passphrase)
print_info(decrypted_data)
