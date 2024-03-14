#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# src/main.py
# by Mia Stein

import argparse

from src.utils.os import load_config
import src.experiments.simple_pir as pir_exp
import src.experiments.homomorphism as ah_exp
import src.experiments.simple_encryption as simple_exp


def run_menu() -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser(description='✨ Magick: PIR Experiment ✨')
    parser.add_argument('-e', dest='lre', action='store_true',
                        help="Run simple linear key Regev encryption experiment with sampled error. \
                        Example: magick -e")
    parser.add_argument('-s', dest='lrs', action='store_true',
                        help="Run simple linear key Regev encryption experiment with scaled msg. \
                        Example: magick -s")
    parser.add_argument('-a', dest='ah', action='store_true',
                        help="Prove that the Regev scheme is additive homomorphic. \
                        Example: magick -s")
    parser.add_argument('-i', dest='pip', action='store_true',
                        help="Prove that the Regev scheme supports plaintext inner product. \
                        Example: magick -i")
    parser.add_argument('-t', dest='tutorial', action='store_true',
                        help="Run a very simple PIR explanation (without encryption). \
                        Example: magick -t")
    parser.add_argument('-p', dest='pir', action='store_true',
                        help="Run a secret key Regev PIR experiment. \
                        Example: magick -p")

    return parser


def run() -> None:

    load_config()
    parser = run_menu()
    args = parser.parse_args()

    if args.lre:
        simple_exp.linear_secret_key_regev_encryption_with_error()

    elif args.lrs:
        simple_exp.linear_secret_key_regev_encryption_scaled()

    elif args.ah:
        ah_exp.additive_homomorphism()
    
    elif args.pip:
        ah_exp.plaintext_inner_product()
    
    elif args.tutorial:
        pir_exp.no_encryption_example()

    elif args.pir:
        pir_exp.secret_key_regev_example()

    else:
        parser.print_help()


if __name__ == "__main__":
    run()

