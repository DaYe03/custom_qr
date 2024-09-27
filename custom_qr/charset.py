import numpy as np

small = {
    "maxWidth": 3,
    "maxHeight": 5,
    'A': np.array([[0, 1, 0],
                   [1, 0, 1],
                   [1, 1, 1],
                   [1, 0, 1],
                   [1, 0, 1]], dtype=np.uint8),
    'B': np.array([[1, 1, 0],
                   [1, 0, 1],
                   [1, 1, 0],
                   [1, 0, 1],
                   [1, 1, 0]], dtype=np.uint8),
    'C': np.array([[0, 1, 1],
                   [1, 0, 0],
                   [1, 0, 0],
                   [1, 0, 0],
                   [0, 1, 1]], dtype=np.uint8),
    'D': np.array([[1, 1, 0],
                   [1, 0, 1],
                   [1, 0, 1],
                   [1, 0, 1],
                   [1, 1, 0]], dtype=np.uint8),
    'E': np.array([[1, 1, 1],
                   [1, 0, 0],
                   [1, 1, 0],
                   [1, 0, 0],
                   [1, 1, 1]], dtype=np.uint8),
    'F': np.array([[1, 1, 1],
                   [1, 0, 0],
                   [1, 1, 0],
                   [1, 0, 0],
                   [1, 0, 0]], dtype=np.uint8),
    'G': np.array([[0, 1, 1],
                   [1, 0, 0],
                   [1, 0, 1],
                   [1, 0, 1],
                   [0, 1, 1]], dtype=np.uint8),
    'H': np.array([[1, 0, 1],
                   [1, 0, 1],
                   [1, 1, 1],
                   [1, 0, 1],
                   [1, 0, 1]], dtype=np.uint8),
    'I': np.array([[1],
                   [1],
                   [1],
                   [1],
                   [1]], dtype=np.uint8),
    'J': np.array([[0, 0, 1],
                   [0, 0, 1],
                   [0, 0, 1],
                   [1, 0, 1],
                   [0, 1, 1]], dtype=np.uint8),
    'K': np.array([[1, 0, 1],
                   [1, 1, 0],
                   [1, 0, 0],
                   [1, 1, 0],
                   [1, 0, 1]], dtype=np.uint8),
    'L': np.array([[1, 0, 0],
                   [1, 0, 0],
                   [1, 0, 0],
                   [1, 0, 0],
                   [1, 1, 1]], dtype=np.uint8),
    'M': np.array([[1, 0, 0, 0, 1],
                   [1, 1, 0, 1, 1],
                   [1, 0, 1, 0, 1],
                   [1, 0, 0, 0, 1],
                   [1, 0, 0, 0, 1]], dtype=np.uint8),
    'N': np.array([[1, 0, 0, 1],
                   [1, 1, 0, 1],
                   [1, 0, 1, 1],
                   [1, 0, 0, 1],
                   [1, 0, 0, 1]], dtype=np.uint8),
    'O': np.array([[0, 1, 0],
                   [1, 0, 1],
                   [1, 0, 1],
                   [1, 0, 1],
                   [0, 1, 0]], dtype=np.uint8),
    'P': np.array([[1, 1, 0],
                   [1, 0, 1],
                   [1, 1, 0],
                   [1, 0, 0],
                   [1, 0, 0]], dtype=np.uint8),
    'Q': np.array([[0, 1, 0],
                   [1, 0, 1],
                   [1, 0, 1],
                   [1, 1, 0],
                   [0, 1, 1]], dtype=np.uint8),
    'R': np.array([[1, 1, 0],
                   [1, 0, 1],
                   [1, 1, 0],
                   [1, 0, 1],
                   [1, 0, 1]], dtype=np.uint8),
    'S': np.array([[0, 1, 1],
                   [1, 0, 0],
                   [0, 1, 0],
                   [0, 0, 1],
                   [1, 1, 0]], dtype=np.uint8),
    'T': np.array([[1, 1, 1],
                   [0, 1, 0],
                   [0, 1, 0],
                   [0, 1, 0],
                   [0, 1, 0]], dtype=np.uint8),
    'U': np.array([[1, 0, 1],
                   [1, 0, 1],
                   [1, 0, 1],
                   [1, 0, 1],
                   [0, 1, 0]], dtype=np.uint8),
    'V': np.array([[1, 0, 1],
                   [1, 0, 1],
                   [1, 0, 1],
                   [0, 1, 0],
                   [0, 1, 0]], dtype=np.uint8),
    'W': np.array([[1, 0, 1, 0, 1],
                   [1, 0, 1, 0, 1],
                   [1, 0, 1, 0, 1],
                   [1, 1, 1, 1, 1],
                   [0, 1, 0, 1, 0]], dtype=np.uint8),
    'X': np.array([[1, 0, 1],
                   [1, 0, 1],
                   [0, 1, 0],
                   [1, 0, 1],
                   [1, 0, 1]], dtype=np.uint8),
    'Y': np.array([[1, 0, 1],
                   [1, 0, 1],
                   [0, 1, 0],
                   [0, 1, 0],
                   [0, 1, 0]], dtype=np.uint8),
    'Z': np.array([[1, 1, 1],
                   [0, 0, 1],
                   [0, 1, 0],
                   [1, 0, 0],
                   [1, 1, 1]], dtype=np.uint8),
    'a': np.array([[0, 1, 1],
                   [1, 0, 1],
                   [0, 1, 1]], dtype=np.uint8),
    'b': np.array([[1, 0, 0],
                   [1, 0, 0],
                   [1, 1, 0],
                   [1, 0, 1],
                   [1, 1, 0]], dtype=np.uint8),
    'c': np.array([[0, 1, 1],
                   [1, 0, 0],
                   [0, 1, 1]], dtype=np.uint8),
    'd': np.array([[0, 0, 1],
                   [0, 0, 1],
                   [0, 1, 1],
                   [1, 0, 1],
                   [0, 1, 1]], dtype=np.uint8),
    'e': np.array([[1, 1, 1],
                   [1, 0, 1],
                   [1, 1, 0]], dtype=np.uint8),
    'f': np.array([[0, 1],
                   [1, 0],
                   [1, 1],
                   [1, 0],
                   [1, 0]], dtype=np.uint8),
    'g': np.array([[0, 1, 1],
                   [1, 0, 1],
                   [0, 1, 1],
                   [0, 0, 1],
                   [1, 1, 0]], dtype=np.uint8),
    'h': np.array([[1, 0, 0],
                   [1, 0, 0],
                   [1, 1, 0],
                   [1, 0, 1],
                   [1, 0, 1]], dtype=np.uint8),
    'i': np.array([[1],
                   [0],
                   [1],
                   [1],
                   [1]], dtype=np.uint8),
    'j': np.array([[0, 1],
                   [0, 1],
                   [0, 1],
                   [1, 0],
                   [1, 1]], dtype=np.uint8),
    'k': np.array([[1, 0, 0],
                   [1, 0, 1],
                   [1, 1, 0],
                   [1, 0, 1],
                   [1, 0, 1]], dtype=np.uint8),
    'l': np.array([[1, 1],
                   [0, 1],
                   [0, 1],
                   [0, 1],
                   [0, 1]], dtype=np.uint8),
    'm': np.array([[1, 1, 1, 1, 0],
                   [1, 0, 1, 0, 1],
                   [1, 0, 1, 0, 1]], dtype=np.uint8),
    'n': np.array([[1, 1, 0],
                   [1, 0, 1],
                   [1, 0, 1]], dtype=np.uint8),
    'o': np.array([[1, 1, 1],
                   [1, 0, 1],
                   [1, 1, 1]], dtype=np.uint8),
    'p': np.array([[1, 1, 0],
                   [1, 0, 1],
                   [1, 1, 0],
                   [1, 0, 0]], dtype=np.uint8),
    'q': np.array([[0, 1, 1],
                   [1, 0, 1],
                   [0, 1, 1],
                   [0, 0, 1]], dtype=np.uint8),
    'r': np.array([[1, 1],
                   [1, 0],
                   [1, 0]], dtype=np.uint8),
    's': np.array([[0, 1, 1],
                   [0, 1, 0],
                   [1, 1, 0]], dtype=np.uint8),
    't': np.array([[0, 1, 0],
                   [0, 1, 0],
                   [1, 1, 1],
                   [0, 1, 0],
                   [0, 1, 0]], dtype=np.uint8),
    'u': np.array([[1, 0, 1],
                   [1, 0, 1],
                   [0, 1, 1]], dtype=np.uint8),
    'v': np.array([[1, 0, 1],
                   [1, 0, 1],
                   [0, 1, 0]], dtype=np.uint8),
    'w': np.array([[1, 0, 1, 0, 1],
                   [1, 0, 1, 0, 1],
                   [0, 1, 0, 1, 0]], dtype=np.uint8),
    'x': np.array([[1, 0, 1],
                   [0, 1, 0],
                   [1, 0, 1]], dtype=np.uint8),
    'y': np.array([[1, 0, 1],
                   [1, 0, 1],
                   [0, 1, 0],
                   [1, 0, 0]], dtype=np.uint8),
    'z': np.array([[1, 1, 0],
                   [0, 1, 0],
                   [0, 1, 1]], dtype=np.uint8),
    '0': np.array([[1, 1, 1],
                   [1, 0, 1],
                   [1, 0, 1],
                   [1, 0, 1],
                   [1, 1, 1]], dtype=np.uint8),
    '1': np.array([[0, 1, 0],
                   [1, 1, 0],
                   [0, 1, 0],
                   [0, 1, 0],
                   [1, 1, 1]], dtype=np.uint8),
    '2': np.array([[1, 1, 1],
                   [0, 0, 1],
                   [1, 1, 1],
                   [1, 0, 0],
                   [1, 1, 1]], dtype=np.uint8),
    '3': np.array([[1, 1, 1],
                   [0, 0, 1],
                   [1, 1, 1],
                   [0, 0, 1],
                   [1, 1, 1]], dtype=np.uint8),
    '4': np.array([[1, 0, 1],
                   [1, 0, 1],
                   [1, 1, 1],
                   [0, 0, 1],
                   [0, 0, 1]], dtype=np.uint8),
    '5': np.array([[1, 1, 1],
                   [1, 0, 0],
                   [1, 1, 1],
                   [0, 0, 1],
                   [1, 1, 1]], dtype=np.uint8),
    '6': np.array([[1, 1, 1],
                   [1, 0, 0],
                   [1, 1, 1],
                   [1, 0, 1],
                   [1, 1, 1]], dtype=np.uint8),
    '7': np.array([[1, 1],
                   [0, 1],
                   [0, 1],
                   [0, 1],
                   [0, 1]], dtype=np.uint8),
    '8': np.array([[1, 1, 1],
                   [1, 0, 1],
                   [1, 1, 1],
                   [1, 0, 1],
                   [1, 1, 1]], dtype=np.uint8),
    '9': np.array([[1, 1, 1],
                   [1, 0, 1],
                   [1, 1, 1],
                   [0, 0, 1],
                   [1, 1, 1]], dtype=np.uint8),
    ' ': np.array([[0],
                   [0],
                   [0],
                   [0],
                   [0]], dtype=np.uint8),
    '!': np.array([[1],
                   [1],
                   [1],
                   [0],
                   [1]], dtype=np.uint8),
    '"': np.array([[1, 0, 1],
                   [1, 0, 1],
                   [0, 0, 0],
                   [0, 0, 0],
                   [0, 0, 0]], dtype=np.uint8),
    '#': np.array([[0, 1, 0, 1, 0],
                   [1, 1, 1, 1, 1],
                   [0, 1, 0, 1, 0],
                   [1, 1, 1, 1, 1],
                   [0, 1, 0, 1, 0]], dtype=np.uint8),
    '$': np.array([[0, 1, 1, 1, 1],
                   [1, 0, 1, 0, 0],
                   [0, 1, 1, 1, 0],
                   [0, 0, 1, 0, 1],
                   [1, 1, 1, 1, 0]], dtype=np.uint8),
    '%': np.array([[0, 1, 0, 1, 0],
                   [1, 0, 1, 0, 0],
                   [0, 1, 1, 1, 0],
                   [0, 0, 1, 0, 1],
                   [0, 1, 0, 1, 0]], dtype=np.uint8),
    '&': np.array([[1, 1, 1, 0],
                   [1, 0, 1, 0],
                   [0, 1, 0, 0],
                   [1, 0, 1, 1],
                   [1, 1, 1, 1]], dtype=np.uint8),
    "'": np.array([[1],
                   [1],
                   [0],
                   [0],
                   [0]], dtype=np.uint8),
    '(': np.array([[0, 1],
                   [1, 0],
                   [1, 0],
                   [1, 0],
                   [0, 1]], dtype=np.uint8),
    ')': np.array([[1, 0],
                   [0, 1],
                   [0, 1],
                   [0, 1],
                   [1, 0]], dtype=np.uint8),
    '*': np.array([[0, 0, 1, 0, 0],
                   [1, 0, 1, 0, 1],
                   [0, 1, 1, 1, 0],
                   [1, 0, 1, 0, 1],
                   [0, 0, 1, 0, 0]], dtype=np.uint8),
    '+': np.array([[0, 0, 0],
                   [0, 1, 0],
                   [1, 1, 1],
                   [0, 1, 0],
                   [0, 0, 0]], dtype=np.uint8),
    ',': np.array([[0],
                   [0],
                   [0],
                   [1],
                   [1]], dtype=np.uint8),
    '-': np.array([[0, 0, 0],
                   [0, 0, 0],
                   [1, 1, 1],
                   [0, 0, 0],
                   [0, 0, 0]], dtype=np.uint8),
    '.': np.array([[0],
                   [0],
                   [0],
                   [0],
                   [1]], dtype=np.uint8),
    '/': np.array([[0, 0, 1],
                   [0, 1, 0],
                   [0, 1, 0],
                   [0, 1, 0],
                   [1, 0, 0]], dtype=np.uint8),
    "\\":np.array([[1, 0, 0],
                   [0, 1, 0],
                   [0, 1, 0],
                   [0, 1, 0],
                   [0, 0, 1]], dtype=np.uint8),
    ':': np.array([[0],
                   [1],
                   [0],
                   [1],
                   [0]], dtype=np.uint8),
    ';': np.array([[0],
                   [1],
                   [0],
                   [1],
                   [1]], dtype=np.uint8),
    '<': np.array([[0, 0, 1],
                   [0, 1, 0],
                   [1, 0, 0],
                   [0, 1, 0],
                   [0, 0, 1]], dtype=np.uint8),
    '=': np.array([[0, 0, 0],
                   [1, 1, 1],
                   [0, 0, 0],
                   [1, 1, 1],
                   [0, 0, 0]], dtype=np.uint8),
    '>': np.array([[1, 0, 0],
                   [0, 1, 0],
                   [0, 0, 1],
                   [0, 1, 0],
                   [1, 0, 0]], dtype=np.uint8),
    '?': np.array([[1, 1, 1],
                   [0, 0, 1],
                   [0, 1, 0],
                   [0, 0, 0],
                   [0, 1, 0]], dtype=np.uint8),
    '@': np.array([[0, 1, 1, 1, 0],
                   [1, 0, 0, 0, 1],
                   [1, 0, 1, 1, 1],
                   [1, 0, 1, 0, 1],
                   [1, 0, 1, 1, 1]], dtype=np.uint8),
    '[': np.array([[1, 1],
                   [1, 0],
                   [1, 0],
                   [1, 0],
                   [1, 1]], dtype=np.uint8),
    ']': np.array([[1, 1],
                   [0, 1],
                   [0, 1],
                   [0, 1],
                   [1, 1]], dtype=np.uint8),
    '^': np.array([[0, 1, 0],
                   [1, 0, 1],
                   [0, 0, 0],
                   [0, 0, 0],
                   [0, 0, 0]], dtype=np.uint8),
    '_': np.array([[0, 0, 0],
                   [0, 0, 0],
                   [0, 0, 0],
                   [0, 0, 0],
                   [1, 1, 1]], dtype=np.uint8),
    '`': np.array([[1, 0],
                   [0, 1],
                   [0, 0],
                   [0, 0],
                   [0, 0]], dtype=np.uint8),
    '{': np.array([[0, 1, 1],
                   [0, 1, 0],
                   [1, 1, 0],
                   [0, 1, 0],
                   [0, 1, 1]], dtype=np.uint8),
    '|': np.array([[1],
                   [1],
                   [1],
                   [1],
                   [1]], dtype=np.uint8),
    '}': np.array([[1, 1, 0],
                   [0, 1, 0],
                   [0, 1, 1],
                   [0, 1, 0],
                   [1, 1, 0]], dtype=np.uint8),
    '~': np.array([[0, 0, 0, 0],
                   [0, 0, 0, 0],
                   [0, 1, 0, 1],
                   [1, 0, 1, 0],
                   [0, 0, 0, 0]], dtype=np.uint8)
}