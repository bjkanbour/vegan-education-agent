"""
Entry point. Run modes:

  python main.py                        # process all files in input/
  python main.py --text "some text"     # review inline text
  python main.py --file path/to/file    # review a single file
"""

import argparse
import logging
from pathlib import Path

from dotenv import load_dotenv

from agent.education_agent import process_all_inputs, process_file, review_content


def main() -> None:
    load_dotenv()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%H:%M:%S",
    )

    parser = argparse.ArgumentParser(description="Vegan Education Agent")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--text", type=str, help="Inline text to review")
    group.add_argument("--file", type=str, help="Path to a file to review")
    args = parser.parse_args()

    if args.text:
        result = review_content(args.text)
        print(result)
    elif args.file:
        path = Path(args.file).resolve()
        if not path.exists():
            logging.error("File not found: %s", path)
            return
        output = process_file(path)
        if output is None:
            logging.error("Processing failed — no output written.")
        else:
            print(f"\nOutput written to: {output}")
    else:
        process_all_inputs()


if __name__ == "__main__":
    main()
