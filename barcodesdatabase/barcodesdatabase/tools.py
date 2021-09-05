def decode_email(e):
    """
        This method decrypts an email protected by a CF tag
        A CF tag encrypts the email address in the HTML and uses JavaScript to decrypt it.
        Hence, we can see the email in the browser, but using requests we won't.

        Args:
            e (str): encrypted (ecoded) email

        Returns:
            str: the decrypted (decoded) email
    """

    de = ""
    k = int(e[:2], 16)

    for i in range(2, len(e)-1, 2):
        de += chr(int(e[i:i+2], 16)^k)

    return de