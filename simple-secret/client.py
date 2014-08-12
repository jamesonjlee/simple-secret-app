from util import get_or_gen_gpg
import getpass

passphrase = getpass.getpass(prompt = 'Passphrase: ')
gpg, fp = get_or_gen_gpg(passphrase)

# encrypt and sign
encrypted_data = gpg.encrypt('stuff to encrypt', recipients=[fp], sign=fp, passphrase=passphrase)
print encrypted_data

# decrypt and verify
decrypted_data = gpg.decrypt(str(encrypted_data), passphrase=passphrase)
print decrypted_data
