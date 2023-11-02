#!/usr/bin/env python3
"""This module showcases password encryption with bcrypt"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Salts and hashes a password"""
    if password is not None and isinstance(password, str):
        return bcrypt.hashpw(bytes(password, 'UTF-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Salts and hashes a password"""
    if isinstance(hashed_password, bytes) and isinstance(password, str):
        return bcrypt.checkpw(bytes(password, 'UTF-8'), hashed_password)
    return False


if __name__ == '__main__':
    """Tests the code in this module"""
    pwd = 'This is some text'
    print(f'[{pwd}]: {hash_password(pwd)}')
    print(is_valid(hash_password(pwd), pwd), '\n')

    pwd = '1 l0v3 7h3 w1ld!'
    print(f'[{pwd}]: {hash_password(pwd)}')
    print(is_valid(hash_password(pwd), pwd), '\n')

    pwd = ''
    print(f'[{pwd}]: {hash_password(pwd)}')
    print(is_valid(hash_password(pwd), pwd), '\n')

    pwd = 2
    print(f'[{pwd}]: {hash_password(pwd)}')
    print(is_valid(hash_password(pwd), str(pwd)))
