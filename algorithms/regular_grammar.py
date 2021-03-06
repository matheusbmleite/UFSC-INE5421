#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""regular_grammar.py

Definition of a regular grammar and conversion of this structure to an
deterministic finite automaton, and vice-versa. This method does not
have a name, for it is reasonably simple to understand and/or deduce.

Gustavo Zambonin & Matheus Ben-Hur de Melo Leite, UFSC, October 2015.
"""

from algorithms.finite_automaton import FiniteAutomaton


class RegularGrammar(object):
    """A regular grammar is defined as a 4-tuple (N, Σ, P, S) such that:
    N is a list of non-terminals. These are variables replaced by terminals
    according to the production rules;
    Σ is a finite set of input symbols called the alphabet;
    P is a set of production rules that match the following forms:
        * B -> a (B ∈ N and a is a terminal in Σ);
        * B -> bA (B, A ∈ N and a ∈ Σ; only in right-regular grammars);
        * B -> Ab (B, A ∈ N and a ∈ Σ; only in left-regular grammars);
        * B -> ε (B ∈ N and ε is the string of length 0);
    S is the start symbol, a production that begins a derivation process, which
    allows the grammar to compute the word.
    """

    def __init__(self, non_terminals, terminals, productions, init_production):
        """Inits RegularGrammar with the attributes introduced above."""
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.productions = productions
        self.init_production = init_production

    def __str__(self):
        """Pretty-print the regular grammar object attributes."""
        non_term = "Non-terminals: %s" % (', '.join(
                                          nt for nt in self.non_terminals))
        terminals = "Terminals: %s" % (', '.join(
                                       t for t in self.terminals))
        init_prod = "Initial production: " + self.init_production
        grammar = "Grammar: "
        for prod in self.productions:
            grammar += "\n[" + prod + "]" + " -> "
            grammar += " | ".join([p for p in self.productions[prod]])

        return "%s\n%s\n%s\n%s" % (non_term, terminals, init_prod, grammar)

    def automaton_to_grammar(aut):
        """Transforms a deterministic finite automaton to a regular grammar.

        Arguments:
            aut: the automaton that will be transformed.

        Returns:
            The equivalent regular grammar for the given automaton.
        """
        non_terminals = set()
        productions = {}

        for state in aut.transitions:
            terminal = ",".join(part.upper() for part in state)
            productions[terminal] = set()
            non_terminals.add(terminal)
            for letter in aut.transitions[state]:
                aux = ",".join(i.upper()
                               for i in aut.transitions[state][letter])
                if aux != "":
                    productions[terminal].add(letter + aux)
                if aut.transitions[state][letter] in aut.final_states:
                    productions[terminal].add(letter)

        return RegularGrammar(non_terminals, aut.alphabet, productions,
                              "".join(part.upper() for part in aut.init_state))

    def grammar_to_automaton(gram):
        """Transforms a regular grammmar to a DFA.

        Arguments:
            gram: the grammar that will be read.

        Returns:
            The equivalent DFA for the given regular grammar.
        """
        alphabet = gram.terminals
        states, final_states = set(), set()
        transitions = {}

        for production in gram.productions:
            states.add(production.lower())
            prod = frozenset([production.lower()])
            transitions[prod] = {}

            for part in gram.productions[production]:
                if len(part) > 1:
                    transitions[prod][part[0]] = part[1:].lower()

            for part in gram.productions[production]:
                if len(part) == 1:
                    final_states.add(transitions[prod][part])

            if len(gram.productions[production]) == 0:
                for symbol in alphabet:
                    transitions[prod][symbol] = set()

        return FiniteAutomaton(states, alphabet, transitions,
                               gram.init_production.lower(), final_states)
