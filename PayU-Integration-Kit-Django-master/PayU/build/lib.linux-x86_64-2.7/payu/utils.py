from hashlib import sha512
from django.conf import settings
KEYS = ['key', 'txnid', 'amount', 'productinfo', 'firstname', 'email',
        'udf1', 'udf2', 'udf3', 'udf4', 'udf5',  'udf6',  'udf7', 'udf8',
        'udf9',  'udf10']

def generate_hash(data,delegate):
    keys = ['key', 'txnid', 'amount', 'productinfo', 'firstname', 'email',
            'udf1', 'udf2', 'udf3', 'udf4', 'udf5',  'udf6',  'udf7', 'udf8',
            'udf9',  'udf10']
    hash = sha512('')
    if delegate=="Indian Delegate":
        #amount=((int(number_of_person)-1)*3000)+5000
        #cc="rupee"
        merchant_key=settings.PAYU_INFO['merchant_key_rupee']
        salt=settings.PAYU_INFO['salt_rupee']
    elif delegate=="Foreign Delegate":
        #amount=int(number_of_person)*100
        #cc="dollar"
        merchant_key=settings.PAYU_INFO['merchant_key_usd']
        salt=settings.PAYU_INFO['salt_usd']    

    for key in keys:
        hash.update("%s%s" % (str(data.get(key, '')), '|'))
    hash.update(salt)
    return hash.hexdigest().lower()

def verify_hash(data, SALT):    
    KEYS.reverse()
    additionalCharges=str(data.get('additionalCharges', ''))
    if additionalCharges!="":
        hash = sha512(additionalCharges)
        hash.update("%s%s" % ('|',SALT))
    else:
        hash = sha512(SALT)
    hash.update("%s%s" % ('|', str(data.get('status', ''))))
    for key in KEYS:
        hash.update("%s%s" % ('|', str(data.get(key, ''))))
    return (hash.hexdigest().lower() == data.get('hash'))
