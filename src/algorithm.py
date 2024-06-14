from string import ascii_lowercase

SIGMA = ascii_lowercase
CONCATENATION = '+'
UNION = '|'
KLEENE_STAR = '*'
EMPTY_LANGUAGE = '#'
EMPTY_WORD = 'E'


class State:
    label = None
    edge1 = None
    edge2 = None


class NFA:
    """
    Class of a non-deterministic finite automaton
    """
    initial = None
    accept = None

    def __init__(self, initial, accept):
        self.initial = initial
        self.accept = accept


def thompson_construction(postfix):
    """
    The function takes the reverse Polish notation of a regular expression and
    returns the corresponding nondeterministic finite automaton
    """
    stack = []
    for c in postfix:
        if c == KLEENE_STAR:
            nfa1 = stack.pop()
            initial = State()
            accept = State()
            initial.edge1 = nfa1.initial
            initial.edge2 = accept
            nfa1.accept.edge1 = nfa1.initial
            nfa1.accept.edge2 = accept
            stack.append(NFA(initial, accept))
        elif c == CONCATENATION:
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            nfa1.accept.edge1 = nfa2.initial
            stack.append(NFA(nfa1.initial, nfa2.accept))
        elif c == UNION:
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            initial = State()
            accept = State()
            initial.edge1 = nfa1.initial
            initial.edge2 = nfa2.initial
            nfa1.accept.edge1 = accept
            nfa2.accept.edge1 = accept
            stack.append(NFA(initial, accept))
        else:
            initial = State()
            accept = State()
            initial.label = c
            initial.edge1 = accept
            stack.append(NFA(initial, accept))
    return stack.pop()


def search_states(state):
    """
    The function recursively finds a set of states,
    to which you can switch from a given state
    """
    states = set()
    states.add(state)
    if state.label is None:
        if state.edge1 is not None:
            states |= search_states(state.edge1)
        if state.edge2 is not None:
            states |= search_states(state.edge2)
    return states


def infix_to_postfix(infix):
    """
    The function takes a regular expression and
    makes a reverse Polish entry out of it
    """
    precedence = {UNION: 1, CONCATENATION: 2, KLEENE_STAR: 3}

    postfix = ''
    stack = []

    for i, char in enumerate(infix):
        if char.isalpha():
            postfix += char
        elif char == '(':
            stack.append(char)
        elif char == ')':
            while stack and stack[-1] != '(':
                postfix += stack.pop()
            stack.pop()
        else:
            if char == KLEENE_STAR and i > 0 and infix[i-1] == KLEENE_STAR:
                continue
            while stack and stack[-1] != \
                    '(' and precedence[char] <= precedence.get(stack[-1], 0):
                postfix += stack.pop()
            stack.append(char)

    while stack:
        postfix += stack.pop()

    return postfix


def match(infix, word):
    """
    The function accepts the reverse Polish notation and the word.
    Returns True if the word belongs to a regular expression and
    False otherwise
    """
    postfix = infix_to_postfix(infix)
    nfa = thompson_construction(postfix)
    current = set()
    incoming = set()
    current |= search_states(nfa.initial)
    for s in word:
        for c in current:
            if c.label == s:
                incoming |= search_states(c.edge1)
        current = incoming
        incoming = set()
    return nfa.accept in current


def is_correct_regex(regex_str):
    """
    The function takes a regular expression and will check,
    that it is set correctly
    """
    if len(regex_str) > 1:
        if regex_str[0] == '(' and regex_str[-1] == ')':
            middle = regex_str[1:-1]
            for i in range(0, len(middle)):
                if middle[i] == CONCATENATION or middle[i] == UNION:
                    left = middle[0:i]
                    right = middle[i + 1:]
                    if is_correct_regex(left) and is_correct_regex(right):
                        return True
            return False
        elif regex_str[-1] == KLEENE_STAR:
            return is_correct_regex(regex_str[:-1])
        else:
            if len(regex_str) > 1 and all(c in SIGMA for c in regex_str):
                return False
            for c in regex_str:
                if c not in SIGMA:
                    return False
            return True
    elif len(regex_str) == 1:
        if regex_str == EMPTY_LANGUAGE or regex_str == EMPTY_WORD \
                                       or regex_str in SIGMA:
            return True
    else:
        return False
