from services.chat_service.services.encryption import (
    encrypt_message, decrypt_message
)


def test_encryption_and_decryption_success():
    message = "Secret chat message"
    password = "strongpassword123"

    encrypted = encrypt_message(message, password)
    decrypted = decrypt_message(encrypted, password)

    assert decrypted == message


def test_decryption_fails_with_wrong_password():
    message = "Another secret"
    password = "correct"
    wrong_password = "wrong"

    encrypted = encrypt_message(message, password)
    decrypted = decrypt_message(encrypted, wrong_password)

    assert decrypted != message
    assert decrypted.startswith("Decryption failed")


def test_encryption_empty_message():
    message = ""
    password = "abc"

    encrypted = encrypt_message(message, password)
    decrypted = decrypt_message(encrypted, password)

    assert decrypted == message


def test_encryption_unicode_characters():
    message = "Тестовое сообщение с юникодом"
    password = "пароль"

    encrypted = encrypt_message(message, password)
    decrypted = decrypt_message(encrypted, password)

    assert decrypted == message


def test_encryption_same_input_produces_different_output():
    message = "Same message"
    password = "samepass"

    encrypted1 = encrypt_message(message, password)
    encrypted2 = encrypt_message(message, password)

    assert encrypted1 != encrypted2


def test_decryption_with_corrupted_data():
    message = "Sensitive data"
    password = "key123"

    encrypted = encrypt_message(message, password)
    corrupted = encrypted[:-4] + "abcd"

    decrypted = decrypt_message(corrupted, password)

    assert decrypted.startswith("Decryption failed")
