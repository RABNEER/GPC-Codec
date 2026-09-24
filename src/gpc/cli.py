"""
Command-Line Interface for GPC Codec
"""

import sys
import argparse
from .core import GeneralizedPathaCode

def main():
    parser = argparse.ArgumentParser(description="Generalized Patha Code (GPC) CLI")
    subparsers = parser.add_subparsers(dest="command")

    enc_parser = subparsers.add_parser("encode", help="Encode binary message vector")
    enc_parser.add_argument("message", type=str, help="Binary string (e.g., 1011)")

    bench_parser = subparsers.add_parser("benchmark", help="Run quick benchmark for given K")
    bench_parser.add_argument("-k", type=int, default=4, help="Message dimension K (default: 4)")

    args = parser.parse_args()

    if args.command == "encode":
        bits = [int(b) for b in args.message.strip()]
        codec = GeneralizedPathaCode(K=len(bits))
        cw = codec.encode(bits)
        print(f"Input ({len(bits)} bits): {args.message}")
        print(f"GPC Codeword ({len(cw)} bits): {''.join(map(str, cw))}")
        print(f"Code Rate: {codec.rate:.4f} | Marked B_E: {codec.BE}")
    elif args.command == "benchmark":
        codec = GeneralizedPathaCode(K=args.k)
        print(f"GPC (K={args.k}): M={codec.M}, Rate={codec.rate:.4f}, B_E={codec.BE} bits ({codec.BE/codec.M*100:.1f}%)")
        print(f"Pilot indices: {codec.pilots}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
