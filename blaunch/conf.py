class Config:
    auto_run = False
    padding = 5
    font_size = 10
    font_name = U'Monospace'
    position = (810, 400)
    size = (300, 250)
    shell_prefix = U'$'

    def __init__(self, file_contents):
        dictionaries = Config._parse(file_contents)

        for key in dictionaries:
            key = key.lower()
            value = dictionaries[key]

            if key == 'auto_run':
                self.auto_run = (value.lower() == 'true')
            elif key == 'padding':
                self.padding = int(value)
            elif key == 'font_size':
                self.font_size = int(value)
            elif key == 'font_name':
                self.font_name = value
            elif key == 'position_x':
                self.position = (int(value), self.position[1])
            elif key == 'position_y':
                self.position = (self.position[0], int(value))
            elif key == 'size_w':
                self.size = (int(value), self.size[1])
            elif key == 'size_h':
                self.size = (self.size[0], int(value))
            elif key == 'shell_prefix':
                self.shell_prefix = value

    @staticmethod
    def _parse(file_contents):
        """Parses file_contents into a dictionary

        Empty lines and commented (#) lines are ignored.
        Keys and values are trimmed.
        """

        if file_contents is None or file_contents == '':
            return {}

        result = {}

        for line in file_contents.splitlines():
            # Full line comment
            if line[:1] == '#':
                continue

            parts = line.split('=', 1)

            # Not a full key-value pair.
            if len(parts) < 2:
                continue

            result[parts[0].strip()] = parts[1].strip()

        return result
