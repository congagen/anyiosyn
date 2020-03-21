
import os
import sys

from midi import render


def main(spec_path, output_path):
    input_filename = os.path.basename(spec_path)

    render.render_midi(spec_path, output_path+input_filename)


if __name__ == "__main__":
    spec_path = sys.argv[1]
    output_path = sys.argv[2]

    main(spec_path, output_path)