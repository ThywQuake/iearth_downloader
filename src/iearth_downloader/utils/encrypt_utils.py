import json
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import base64

def encrypt4long(obj):

    public_key_pem = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAnPek4vyIGd2F9PpRqm3U
D3+LH2kTdhvUXIovKwaRIYUX73ruFFq6dUnnFy3Wyrv2tGsGsEAISGr5+CyL2nRc
Ow4kWVzJhkemgNXt6dkLNEyq7pYxKAAPtGUbBZYh74Ye2nag+Ffd5LTY8NvZ05NS
IhwsqqaEmyrDElzsH+i84WYpULguxk5di1tTU9RQeQkZRGkxctmKjXc+uhNHW5F9
0Qoy+/P0+T48bmHoTCKjTl8dpk5RJOivCyjHUkQRZJolBnwa4NWIJWTSBt7ioKrI
ObfDM8zQk//KQib8gtw7UDUFsRMOG0khIxBX4g7qESdvGszg+5BIRBsyyxRJqqjt
NwIDAQAB
-----END PUBLIC KEY-----"""
    
    try:
        rsa_key = RSA.importKey(public_key_pem)
        cipher = PKCS1_v1_5.new(rsa_key)
        json_str = json.dumps(obj, ensure_ascii=False, separators=(',', ':')) 
        encrypted = cipher.encrypt(json_str.encode('utf-8'))
        return base64.b64encode(encrypted).decode('utf-8')
        
    except Exception as e:
        raise Exception(f"encrypted fail: {str(e)}")

def encrypt_auth(obj):
    public_key_pem2 = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAvrzz4DGWHc6YmK0BZ30LM
qZvWTLOsuIzPJn9LrJ++5416UwqpnnR5DxI4NOAdwwAOv7aOdiZ6ny5u8BX5potv+c
B3evrcpw5HbxSbj1kUzfOv4VCnGSdPMRnx/i3DCaQN1ubliJrm/jfGBEVioTNkT+iN
xcZZYxazgP1PHJOpmUwu7LME+zdGSB+y0MIZasmKi6aVFBIHug83ku0lNpA+hdWTJu
+Unsl6cD58wf7fSF3zLbb9Cmy/kg+qcS0QzzBajSXh1UuRm+4KuQZfDRDuIagICtXv
rY/u2Ow3Kdw4YGqEMe+TLiuxFoCQO9smGCOi9sCFAVrC3DaGPhGYT422QIDAQAB
-----END PUBLIC KEY-----"""
    
    try:
        rsa_key = RSA.importKey(public_key_pem2)
        cipher = PKCS1_v1_5.new(rsa_key)
        json_str = json.dumps(obj, ensure_ascii=False, separators=(',', ':')) 
        encrypted = cipher.encrypt(json_str.encode('utf-8'))
        return base64.b64encode(encrypted).decode('utf-8')
        
    except Exception as e:
        raise Exception(f"encrypted fail: {str(e)}")
