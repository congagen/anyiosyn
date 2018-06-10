
import os
import sys

from lib.midi import render


def main(spec_path, output_path):
    input_filename = os.path.basename(spec_path)

    render.render_midi(spec_path, output_path+input_filename)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        spec_path = sys.argv[1]
        output_path = sys.argv[2]

        main(spec_path, output_path)