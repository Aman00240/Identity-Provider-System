import os

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


def generate_rsa_key_pair():
    os.makedirs("certs", exist_ok=True)

    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )

    with open("certs/private.pem", "wb") as f:
        f.write(private_pem)

    public_key = private_key.public_key()

    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    with open("certs/public.pem", "wb") as f:
        f.write(public_pem)

    print("RSA Key pair generated successfully")


if __name__ == "__main__":
    generate_rsa_key_pair()
