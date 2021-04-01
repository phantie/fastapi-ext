def unique_seq(seq):
    return len(tuple(seq)) == len(set(seq))


def dunder(name: str) -> bool:
    return name.startswith('__') and name.endswith('__')


from fastapi import responses
responses = {getattr(responses, name) for name in dir(responses) if 'Response' in name}