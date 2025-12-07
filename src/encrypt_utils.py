#-------------------
# Encryption Utilities
# AES-256 encryption for sensitive data
#-------------------
import cryptolib
import os
import json
import ubinascii

ENCRYPTION_PASSWORD = '5cb02ec404a8777e5ab9523600e3b7e343b93e25cafe392b539b67cf93c10d79'
ENCRYPTION_KEY = ubinascii.unhexlify(ENCRYPTION_PASSWORD)

def pad_data(data):
    """Add PKCS7 padding for AES block cipher."""
    pad_len = 16 - (len(data) % 16)
    return data + bytes([pad_len] * pad_len)

def unpad_data(data):
    """Remove PKCS7 padding."""
    pad_len = data[-1]
    return data[:-pad_len]

def encrypt_data(plaintext):
    """Encrypt string data with AES-256 CBC mode."""
    try:
        iv = os.urandom(16)
        data_bytes = plaintext.encode('utf-8')
        padded = pad_data(data_bytes)
        cipher = cryptolib.aes(ENCRYPTION_KEY, 2, iv)
        encrypted = cipher.encrypt(padded)
        combined = iv + encrypted
        result = ubinascii.b2a_base64(combined).decode('utf-8').strip()
        return result
    except Exception as e:
        print(f'[CRYPTO] Encryption error: {e}')
        return None

def decrypt_data(ciphertext):
    """Decrypt AES-256 CBC encrypted data."""
    try:
        data = ubinascii.a2b_base64(ciphertext)
        iv = data[:16]
        encrypted = data[16:]
        cipher = cryptolib.aes(ENCRYPTION_KEY, 2, iv)
        decrypted = cipher.decrypt(encrypted)
        unpadded = unpad_data(decrypted)
        result = unpadded.decode('utf-8')
        return result
    except Exception as e:
        print(f'[CRYPTO] Decryption error: {e}')
        return None

def encrypt_sensor_data(temp, pressure, timestamp):
    """Encrypt sensor data as JSON payload."""
    data = {
        'temperature': temp,
        'pressure': pressure,
        'timestamp': timestamp
    }
    json_str = json.dumps(data)
    return encrypt_data(json_str)

def decrypt_sensor_data(encrypted_payload):
    """Decrypt sensor data JSON payload."""
    json_str = decrypt_data(encrypted_payload)
    if json_str:
        return json.loads(json_str)
    return None
