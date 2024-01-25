# -*- encoding: utf-8 -*-
# src/experiments/additive_homomorphism.py
# Experiment with secret key Regev encryption.


from src.primitives.regev import Regev


def additive_homomorphism() -> None:
    """ 
        This method proves that the secret key Regev encryption scheme is
        additive homomorphic, i.e., if c0 encrypts m0 and c1 encrypts m1,
        both under s, then c0 + c1 decrypts to m0 + m1. 
    """

    ########################################################################
    # 1. Key generation for two independent messages m0 and m1
    ########################################################################
    
    r0 = Regev()
    m0, A0, e0 = r0.create_message_setup(this_mod = r0.p)

    r1 = Regev()
    m1, A1, e1 = r1.create_message_setup(this_mod = r1.p)

    s = r0.create_secret_key()

    ########################################################################
    # 3. Scale message vectors by delta = mod / p
    ########################################################################
    scaled_m0 = m0.calculate_scaling(r0.mod, r0.p, r0.mod)
    scaled_m1 = m1.calculate_scaling(r1.mod, r1.p, r1.mod)

    ########################################################################
    # 4. Encryption by calculating B and ciphertext c for each message
    ########################################################################
    c0 = r0.calculate_encryption(A0, s, e0, scaled_m0)
    c1 = r1.calculate_encryption(A1, s, e1, scaled_m1)

    ########################################################################
    # 5. Add the ciphertexts, with c2 = c0 + c1
    ########################################################################
    c2 = (c0[0] + c1[0], c0[1] + c1[1])

    ########################################################################
    # 6. Decrypt the sum of the ciphertexts
    ########################################################################
    r2 = Regev()
    m2 = r2.calculate_decryption(s, c2)

    ########################################################################
    # 5. Scale m1 vector by 1/ delta = p / mod
    ########################################################################
    scaled_m2 = m2.calculate_scaling(r2.p, r2.mod, r2.p)

    ########################################################################
    # 6. The sum of the message vectors m0 and m1 should be equal to m2
    ########################################################################
    r2.print_results(m0 + m1, scaled_m2, 'm0 + m1', 'm2')


def plaintext_inner_product() -> None:
    """ 
        This method proves that the secret key Regev encryption scheme is
        supports plaintext inner product, i.e., if c0 encrypts m0 and c1
        encrypts m1, both under s, then c0 * c1 decrypts to m0 * m1.
    """

    ########################################################################
    # 1. Key generation
    ########################################################################
    r0 = Regev()
    m0, A, e = r0.create_message_setup(this_mod = r0.p)
    s = r0.create_secret_key(this_mod = r0.p)

    ########################################################################
    # 2. Scale message vector by delta = mod / p
    ########################################################################
    scaled_m0 = m0.calculate_scaling(r0.mod, r0.p, r0.mod)

    ########################################################################
    # 3. Encryption by calculating B and ciphertext c
    ########################################################################
    c = r0.calculate_encryption(A, s, e, scaled_m0)

    ########################################################################
    # 4. Calculate a plaintext vector transposed k and then scale it by
    #    delta = mod / p
    ########################################################################
    rk = Regev()
    k = m0.create_random_message(rk.p, 1, rk.m )
    scaled_k = m0.calculate_scaling(1, 1, rk.mod)

    ########################################################################
    # 5. Calculate the noise growth 
    ########################################################################
    noise_growth = scaled_k * e

    ########################################################################
    # 6. Define the ciphertext of the inner product of m0 and k
    ########################################################################
    c1 = (scaled_k * c[0], scaled_k * c[1])

    ########################################################################
    # 7. Decrypt the ciphertext of the inner product of m0 and k
    ########################################################################
    m1 = r0.calculate_decryption(s, c1)

    ########################################################################
    # 8. Scale m1 vector by 1/ delta = p / mod
    ########################################################################
    m1_scaled = m1.calculate_scaling(r0.p, r0.mod, r0.p)

    ########################################################################
    # 9. Scale back the plaintext vector k by 1/ delta = p / mod
    ########################################################################
    scaled_scaled_k = scaled_k.calculate_scaling(1, 1, rk.p)

    ########################################################################
    # 10. The message vector m1 scaled should be equal scaled k * m0
    ########################################################################
    r0.print_results(m1_scaled, scaled_scaled_k * m0, 'scaled m1', 'scaled k * m0')

    ########################################################################
    # 11. Print results on noise, decryption fails when noise > delta / 2 
    ########################################################################
    rk.print_noise_growth(m1_scaled, scaled_scaled_k * m0, noise_growth)
