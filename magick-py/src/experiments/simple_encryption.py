# -*- encoding: utf-8 -*-
# src/experiments/simple_encryption.py
# Experiment with secret key Regev encryption.


from src.primitives.regev import Regev


def linear_secret_key_regev_encryption_with_error() -> None:
    """ 
        This method runs a secret key Regev encryption and decryption 
        experiment for a msg vector with a sampled error vector.

        In this simple example of learning with error (LWE), we operate
        our message vector over a ring modulo mod, such that some
        information is lost. This is not a problem since gaussian elimination
        can be used to recover the original message vector (i.e., it works
        over a ring modulo mod).

        We represent the message vector m0 of size m where each element is
        modulus mod. The cipertext c is B = A * s + e + m0, which can be
        decrypted as c = (B, A).
    """

    ########################################################################
    # 1. Key generation
    ########################################################################
    regev = Regev()
    m0, A, e = regev.create_message_setup()
    s = regev.create_secret_key()

    ########################################################################
    # 2. Encryption by calculating B and ciphertext c
    ########################################################################
    c = regev.calculate_encryption(A, s, e, m0)

    ########################################################################
    # 3. Calculate the decryption of the ciphertext c
    ########################################################################
    m1 = regev.calculate_decryption(s, c)

    ########################################################################
    # 4. The message vector m1 should be equal to m0 plus the error vector e
    ########################################################################
    regev.print_results(m0, m0 + e, 'm0', 'm0 + e')


def linear_secret_key_regev_encryption_scaled() -> None:
    """ 
        This method runs a secret key regev encryption and decryption experiment
        for a msg vector with a scaled msg vector.

        In this another simple example of learning with error (LWE), we loose
        information on least significant bits by adding noise, i.e., by scaling 
        the message vector by delta = mod / p before adding it to encryption. 
        Then, during the decryption, we scale the message vector by 1 / delta.

        The scaling ensures that m is in the highest bits of the message vector,
        without losing information with the addition of the error vector e.

        Now, the message m0 vector has each element module p (not mod), where
        p < q. The scaled message is now m0_scaled = m0 * delta = m0 * mod / p.
        The cipertext c is B = A * s + e + m0_scaled, which can be decrypted as
        c = (B, A), i.e., m0 = (B - A * s) / delta = (delta * m0 + e) / delta.
    """

    ########################################################################
    # 1. Key generation
    ########################################################################
    regev = Regev()
    m0, A, e = regev.create_message_setup(this_mod = regev.p)
    s = regev.create_secret_key()

    ########################################################################
    # 2. Scale message vector by delta = mod / p
    ########################################################################
    scaled_m0 = m0.calculate_scaling(regev.mod, regev.p, regev.mod)

    ########################################################################
    # 3. Encryption by calculating B and ciphertext c
    ########################################################################
    c = regev.calculate_encryption(A, s, e, scaled_m0)

    ########################################################################
    # 4. Calculate the decryption of the ciphertext c
    ########################################################################
    m1 = regev.calculate_decryption(s, c)

    ########################################################################
    # 5. Scale m1 vector by 1/ delta = p / mod
    ########################################################################
    scaled_m1 = m1.calculate_scaling(regev.p, regev.mod, regev.p)

    ########################################################################
    # 6. The message vector m0 should be equal to m1
    ########################################################################
    regev.print_results(m0, scaled_m1, 'm0', 'scaled m1')
