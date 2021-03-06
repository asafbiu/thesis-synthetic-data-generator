import argparse
import random
import yaml
import os
from pathlib import Path
from sampler import sample
from typing import List, Tuple, Union


def load_grammar(grammar_dir: str, file_exts=[".yaml", ".yml"]) -> dict:
    grammar = {}
    grammar_files = [
        f
        for f in os.listdir(grammar_dir)
        if os.path.isfile(os.path.join(grammar_dir, f))
        and Path(os.path.join(grammar_dir, f)).suffix in file_exts
    ]
    for grammar_file in grammar_files:
        with open(os.path.join(grammar_dir, grammar_file), "r") as stream:
            try:
                data = yaml.safe_load(stream)
                grammar = {**grammar, **data}
            except yaml.YAMLError as exc:
                print(exc)
    return grammar


def main(k, grammar_dir="config", root_key="utterance", seed=42):
    if seed:
        random.seed(seed)
    grammar = load_grammar(grammar_dir)
    for n in range(k):
        d = sample(key=root_key, name=root_key, program_stack=dict(), grammar=grammar)
        print(f"{n+1}) Sample:")
        print(f'Text:\n{d["text"]}\n')
        print(f'Code:\n{d["code"]}\n')
        print("-------------------------------")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generates pairs of scenario and intents"
    )
    parser.add_argument(
        "--k", type=int, default=1, help="number of examples to generate"
    )
    parser.add_argument("--seed", type=int, default=None, help="random seed")

    args = parser.parse_args()

    main(k=args.k, seed=args.seed)
