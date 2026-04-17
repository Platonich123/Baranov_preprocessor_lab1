import re
import sys
from pathlib import Path

LITERAL_PATTERN = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'')
COMMENT_PATTERN = re.compile(r'/\*[\s\S]*?\*/|//.*?$' , re.MULTILINE)
WHITESPACE_PATTERN = re.compile(r'[ \t]+')
INVALID_CONTROL_PATTERN = re.compile(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]')


def mask_literals(text: str):
    literals = {}

    def repl(match: re.Match) -> str:
        key = f'__LITERAL_{len(literals)}__'
        literals[key] = match.group(0)
        return key

    masked = LITERAL_PATTERN.sub(repl, text)
    return masked, literals


def restore_literals(text: str, literals: dict[str, str]) -> str:
    for key, value in literals.items():
        text = text.replace(key, value)
    return text


def find_invalid_characters(text: str):
    issues = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        for match in INVALID_CONTROL_PATTERN.finditer(line):
            issues.append((line_no, match.start() + 1, ord(match.group(0))))
    return issues


def check_comment_balance(masked_text: str):
    opened = len(re.findall(r'/\*', masked_text))
    closed = len(re.findall(r'\*/', masked_text))
    if opened > closed:
        return 'Обнаружен незакрытый многострочный комментарий.'
    if closed > opened:
        return 'Обнаружен лишний закрывающий фрагмент комментария */.'
    return None


def normalize_code(text: str) -> str:
    lines = []
    for line in text.splitlines():
        line = WHITESPACE_PATTERN.sub(' ', line).strip()
        if line:
            lines.append(line)
    return '\n'.join(lines) + '\n'


def preprocess(source_text: str):
    messages = []

    invalid_chars = find_invalid_characters(source_text)
    if invalid_chars:
        for line_no, col_no, code in invalid_chars:
            messages.append(
                f'Ошибка: недопустимый символ с кодом ASCII {code} в строке {line_no}, позиция {col_no}.'
            )
        return None, messages

    masked_text, literals = mask_literals(source_text)

    balance_error = check_comment_balance(masked_text)
    if balance_error:
        messages.append(f'Ошибка: {balance_error}')
        return None, messages

    without_comments = COMMENT_PATTERN.sub('', masked_text)
    normalized = normalize_code(without_comments)
    restored = restore_literals(normalized, literals)

    messages.append('Ошибок не выявлено.')
    return restored, messages


def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print('Использование: python preprocessor.py <входной_файл> [выходной_файл]')
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2]) if len(sys.argv) == 3 else input_path.with_name(f'{input_path.stem}_cleaned{input_path.suffix}')

    if not input_path.exists():
        print(f'Ошибка: файл {input_path} не найден.')
        sys.exit(1)

    try:
        source_text = input_path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        print('Ошибка: не удалось прочитать файл в кодировке UTF-8.')
        sys.exit(1)

    cleaned_text, messages = preprocess(source_text)

    if cleaned_text is None:
        for message in messages:
            print(message)
        sys.exit(1)

    output_path.write_text(cleaned_text, encoding='utf-8')
    print(f'Исходный файл: {input_path}')
    print(f'Очищенный файл: {output_path}')
    for message in messages:
        print(message)


if __name__ == '__main__':
    main()
