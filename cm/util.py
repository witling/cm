def strip_command(content):
    import re

    match = re.match('^(\s*\$\S+)', content)
    if match is None:
        return

    cut = len(match.group(1))
    return content[cut:].strip()
