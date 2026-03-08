import os

class Path:
    def __init__(self, path, separator = '/', mode = 0):
        self.json_path = path
        path = self.fix_path(path, separator = separator)

        if path == "":
            self.splitted = []
        else:
            self.splitted = path.split(separator)

        if mode == 1:
            self.os_path = os.sep.join(self.splitted)

    def fix_path(self, path, separator = '/'):
        result = ""

        if len(path) > 0:
            """
            while path[-1] == separator:
                path = path[:-1]

            while path[0] == separator:
                path = path[1:]
            """

            bad = False

            for i in range(len(path)):
                if path[i] == separator:
                    if not bad:
                        result += path[i]
                        bad = True
                else:
                    result += path[i]

                    if bad:
                        bad = False

        return result