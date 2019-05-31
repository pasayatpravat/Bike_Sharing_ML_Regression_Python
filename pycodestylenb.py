import nbformat
from pycodestyle import StyleGuide


class NBStyleGuide(StyleGuide):
    """Checks the cells of a notebook."""

    def input_file(self, filename, lines=None, expected=None, line_offset=0):
        if lines is None:
            with open(filename, "r", encoding="utf-8") as fp:
                nb = nbformat.read(fp, as_version=4)

            lines = []
            for cell in nb.cells:
                if cell["cell_type"] == "code":
                    lines.extend([line + "\n" for line in cell["source"].splitlines()])

        return super().input_file(
            filename, lines=lines, expected=expected, line_offset=line_offset
        )


if __name__ == "__main__":
    import sys

    style_guide = NBStyleGuide(parse_argv=True, config_file=True)

    # Ignore some errors related to whitespace
    style_guide.options.ignore = style_guide.options.ignore + (
        "E302",
        "E305",
        "E402",
        "E501",
    )

    report = style_guide.check_files()

    if report.total_errors:
        if style_guide.options.count:
            sys.stderr.write(str(report.total_errors) + "\n")
        sys.exit(1)
