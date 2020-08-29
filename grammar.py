import fuzzingbook
import fuzzing
import re
import random

GRAMMER = {
    "<start>": ["<my_name>"],
    "<my_name>": ["<f_name> + <my_name>", "<f_name>"],
    "<f_name>": ["<name><f_name>", "f_name + l_name"],
    "<l_name>": ["<name><my_name><f_name><l_name>"],
    "<name>": ["sohel", "mira"]
}

GRAMMER["<name>"]
START_SYMBOL = "<start>"
RE_NONTERMINAL = re.compile(r'(<[^<> ]*>)')


def nonterminals(expansion):

    if isinstance(expansion, tuple):
        expansion = expansion[0]

    return re.findall(RE_NONTERMINAL, expansion)


assert nonterminals("<my_name> * <f_name>") == ["<my_name>", "<f_name>"]
assert nonterminals("<name><l_name>") == ["<name>", "<l_name>"]
assert nonterminals("b < c > d") == []
assert nonterminals("b <c> d") == ["<c>"]
assert nonterminals("b + d") == []
assert nonterminals(("<b>", {'option': 'value'})) == ["<b>"]

print(nonterminals("<my_name> * <f_name>").[0])


def is_nonterminal(s):
    return re.match(RE_NONTERMINAL, s)


assert is_nonterminal("<012>")
assert is_nonterminal("<symbol-1>")
assert not is_nonterminal("+")


class ExpansionError(Exception):
    print('error-112233')
    pass


def simple_grammar_fuzzer(grammar, start_symbol=START_SYMBOL,
                          max_nonterminals=10, max_expansion_trials=100,
                          log=False):
    term = start_symbol
    expansion_trials = 0

    while len(nonterminals(term)) > 0:
        symbol_to_expand = random.choice(nonterminals(term))
        expansions = grammar[symbol_to_expand]
        expansion = random.choice(expansions)
        new_term = term.replace(symbol_to_expand, expansion, 1)

        if len(nonterminals(new_term)) < max_nonterminals:
            term = new_term
            if log:
                print("%-40s" % (symbol_to_expand + " -> " + expansion), term)
            expansion_trials = 0
        else:
            expansion_trials += 1
            if expansion_trials >= max_expansion_trials:
                raise ExpansionError("Cannot expand " + repr(term))

    return term


#simple_grammar_fuzzer(grammar=GRAMMER, max_nonterminals=3, log=True)
# for i in range(10):
#    print(simple_grammar_fuzzer(grammar=GRAMMER, max_nonterminals=5))
