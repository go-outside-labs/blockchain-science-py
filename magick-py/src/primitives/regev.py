# -*- encoding: utf-8 -*-
# src/lib/regev.py
# Class for secret key Regev encryption.


from src.utils.os import load_config
from src.utils.os import log_info, log_error
from src.primitives.message import Message


class Regev():

    def __init__(self):

        self.mod = None
        self.n = None
        self.m = None
        self.p = None
        self.bound = None
        self._load_env_parameters()

    ############################
    #      Private methods
    ############################

    def _load_env_parameters(self) -> None:
        """Load environment variables"""

        env_vars = load_config()
        self.mod = int(env_vars['mod'])
        self.n = int(env_vars['n'])
        self.m = int(env_vars['m'])
        self.p = int(env_vars['p'])
        self.bound = int(env_vars['bound'])


    ############################
    #      Public methods
    ############################

    def print_results(self, m0, m1, m0_string, m1_string) -> None:
        """Print the results of the experiment"""

        if m0 == m1:
            log_info(f'Original msg was successfully retrieved!\n')
        else:
            log_error(f'Original msg was not retrieved.')

        log_info(f'{m0_string}: {m0}\n')
        log_info(f'{m1_string}: {m1}\n')
        log_info(f'Parameters: \nmod: {self.mod} \nn: {self.n} \nm: {self.m} \np: {self.p} \nbound: [-{self.bound}, {self.bound}] \n')

    def print_noise_growth(self, m0, m1, noise_growth) -> None:
        """Print the noise growth"""

        log_info(f'Correct decryption for Delta / 2: {(self.mod / self.p) / 2}? {m0 == m1}')
        log_info(f'Noise growth: {noise_growth.message[0]}')

    def create_secret_key(self, this_mod=None, msg_n=1):
        """Create a secret key vector"""

        if this_mod is None:
            this_mod = self.mod

        return  Message.create_random_message(this_mod, self.n, msg_n)

    def create_message_setup(self, this_m=None, this_n=None, this_mod=None, msg_n=None):
        """Create a message vector setup"""
        
        if this_mod is None:
            this_mod = self.mod
        
        if this_m is None:
            this_m = self.m
        
        if this_n is None:
            this_n = self.n
        
        if msg_n is None:
            msg_n = 1

        # message vector of size `m`, where each element has a modulus `mod`
        m0= Message.create_random_message(this_mod, self.m, msg_n)

        # public    
        A = Message.create_random_message(self.mod, self.m, self.n)

        # error vector
        e = Message.calculate_sample_error(self.bound, self.mod, self.m, msg_n)

        return m0, A, e

    ############################
    #      Static methods
    ############################

    @staticmethod
    def calculate_encryption(A, s, e, m0):
        """
            Encrypt this message with a simple `B = A * s + e + m0`, 
            where `s` is the secret and `e` is the error vector.
            Set the cipher as the tuple c = (B, A).
        """

        B = (A * s) + e + m0
        return (B, A)

    @staticmethod
    def calculate_decryption(s, c):
        """ 
            Calculate the decryption of a ciphertext, given c
            and a secret, such that m1 = m0 + e.
        """

        B = c[0]
        A = c[1]
        return B - (A * s)
