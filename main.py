import sys
import yaml

class ConfigParser:
    def __init__(self):
        self.constants = {}
        self.config = {}

    def evaluate_constant_expression(self, expression):
        expr = expression.strip('![]')

        allowed_functions = {
            "len": len,
            "pow": pow,
            "max": max,
            "min": min,
            "abs": abs,
            "sum": sum,
        }

        for name, value in self.constants.items():
            expr = expr.replace(name, str(value))

        try:
            return eval(expr, {"__builtins__": None}, allowed_functions)
        except Exception as e:
            raise ValueError(f"Ошибка вычисления выражения '{expression}': {str(e)}")

    def parse_list(self, list_str):
        items = list_str.strip('(list )').split()
        return [self.parse_value(item) for item in items]

    def parse_value(self, value):
        if value.startswith('"') and value.endswith('"'):
            return value.strip('"')
        elif value.startswith('(list'):
            return self.parse_list(value)
        elif value.replace('.', '', 1).isdigit():
            return float(value) if '.' in value else int(value)
        else:
            return value

    def parse_config(self, text):
        lines = [line.split('*>')[0].strip() for line in text.splitlines()]
        lines = [line for line in lines if line]

        for line in lines:
            if line.startswith('def'):
                _, name, _, value = line.split(maxsplit=3)
                self.constants[name] = self.parse_value(value)
                self.config[name] = self.constants[name]
            elif '![' in line:
                name = line.split()[0]
                expr = line[line.index('!['): line.index(']') + 1]
                try:
                    value = self.evaluate_constant_expression(expr)
                    self.config[name] = value
                except ValueError as e:
                    print(f"Ошибка: {e}", file=sys.stderr)
            else:
                try:
                    name, value = [x.strip() for x in line.split('=', 1)]
                    self.config[name] = self.parse_value(value)
                except ValueError:
                    print(f"Ошибка синтаксиса в строке: {line}", file=sys.stderr)

        return self.config


def main():
    if len(sys.argv) != 2:
        print("Использование: python script.py <output.yaml>")
        sys.exit(1)

    output_file = sys.argv[1]

    input_text = sys.stdin.read()

    parser = ConfigParser()
    config = parser.parse_config(input_text)

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, allow_unicode=True, sort_keys=False)
    except Exception as e:
        print(f"Ошибка записи в файл {output_file}: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
