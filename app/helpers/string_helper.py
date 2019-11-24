import re


class StringHelper(object):
    def to_snake_case(self, value: str) -> str:
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', value)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
