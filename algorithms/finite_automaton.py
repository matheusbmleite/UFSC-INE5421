#!/usr/bin/env python
# -*- coding: utf-8 -*-
from copy import deepcopy

"""finite_automaton.py

Definition of a finite automaton and construction of deterministic finite
automata through the powerset construction method, also handling epsilon-moves.

Gustavo Zambonin & Matheus Ben-Hur de Melo Leite, UFSC, October 2015.
"""


class FiniteAutomaton(object):
    """A finite automaton is defined as a 5-tuple (Q, Σ, δ, q0, F) such that:
    Q is a finite set of states;
    Σ is a finite set of input symbols called the alphabet;
    δ : Q × Σ → Q (or, verbally, a transition function);
    q0 ∈ Q is a start state;
    F ⊆ Q is a set of accept states.
    """

    def __init__(self, states, alphabet, transitions, initstate, final_states):
        """Inits FiniteAutomaton with the attributes introduced above."""
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.init_state = initstate
        self.final_states = final_states
        self.epsilon = "ε"

    def __str__(self):
        """Pretty-prints the finite automaton object attributes."""
        states = "States: %s" % (', '.join(str(set(s)) for s in self.states))
        alphabet = "Alphabet: %s" % (', '.join(l for l in self.alphabet))
        transitions = "Transitions: "
        for t in self.transitions:
            transitions += '\n%s: %s' % (str(list(t)),
                                         str(self.transitions[t]))
        init_state = "Initial state: %s" % self.init_state
        final = "Final states: %s" % (', '.join(str(set(f))
                                      for f in self.final_states))
        return "%s\n%s\n%s\n%s\n%s" % (states, alphabet, transitions,
                                       init_state, final)

    def epsilon_closure(self):
        """Computes the epsilon-closure for each state of the input NFA.

        Returns:
            The set of every epsilon-closure of the NFA.
        """
        def single_closure(state):
            """Computes the epsilon-closure for a single state of a NFA.

            Attributes:
                state: the source state for the epsilon-closure computation.

            Returns:
                The epsilon-closure for said state.
            """
            closure, old_closure = {state, }, set()
            while old_closure != closure:
                old_closure = closure.copy()
                for state in old_closure:
                    try:
                        s = frozenset([state])
                        closure |= self.transitions[s][self.epsilon]
                    except KeyError:
                        pass
            return closure

        return {state: single_closure(state) for state in self.states}

    def determinize(self):
        """Modifies the input automaton inplace to be caracterized as a DFA."""
        opened, closed, final_states = set(), set(), set()
        new_transitions = {}

        epsilon_closure = self.epsilon_closure()
        init_closure = epsilon_closure[self.init_state]
        new_init_state = init_closure
        opened.add(frozenset(init_closure))

        while opened:
            state = opened.pop()
            closed.add(state)
            try:
                new_transitions[state] = self.transitions[state]
            except KeyError:
                pass

            if state not in self.transitions.keys():
                aux_dict = {letter: set() for letter in self.alphabet}
                for atom in state:  # an atom is each part of a new state
                    for letter in self.alphabet:
                        aux = self.transitions[frozenset([atom])][letter]
                        for dest in aux:
                            aux_dict[letter] |= epsilon_closure[dest]
                self.transitions[state] = aux_dict
                new_transitions[state] = aux_dict

            for key in self.transitions[state]:
                aux_state, new_state = self.transitions[state][key], set()
                for atom in aux_state:
                    new_state |= epsilon_closure[atom]
                if new_state not in opened | closed and new_state:
                    opened.add(frozenset(new_state))
                    try:
                        ns = frozenset(new_state)
                        new_transitions[ns] = self.transitions[ns]
                    except KeyError:
                        pass

        for state in self.final_states:
            for new_state in new_transitions:
                if state & new_state:
                    final_states.add(new_state)
        self.final_states = final_states
        self.init_state = new_init_state
        self.states.clear()
        for state in new_transitions:
            self.states.add(state)
        self.transitions = new_transitions

    def minimize(self):
        self.determinize()

        def belongs_to(self, state):
            for lst in classes:
                if len(lst) > 1 or lst not in old_classes:
                    for letter in self.transitions[lst[0]]:
                        both = False
                        arrival_list = list()
                        arrival_list2 = list()
                        for old_list in old_classes:
                            head = lst.pop(0)
                            lst.insert(0, head)
                            if frozenset(self.transitions[head][letter]) in old_list:
                                arrival_list = old_list
                            if frozenset(self.transitions[state][letter]) in old_list:
                                arrival_list2 = old_list

                        if arrival_list == arrival_list2:
                            both = True
                        if not both:
                            break
                    if both:
                        return lst
            return [frozenset(state)]

        classes = list()
        classes.append(list(self.final_states))
        if len(list(self.states - self.final_states)) > 0:
            classes.append(list(self.states - self.final_states))

        old_classes = list()


        while classes != old_classes:
            old_classes = deepcopy(classes)
            for classs in classes:
                if len(classs) > 1:
                    aux_c = classs[:]
                    head_state = aux_c.pop(0)
                    for state in aux_c:
                        index = classs.index(state)
                        classs.pop(index)
                        class_which_belongs = belongs_to(self, state)
                        if class_which_belongs in classes:
                            class_which_belongs.append(state)
                        else:
                            classes.append(class_which_belongs)

        print (classes)





def test():
     b = FiniteAutomaton(set(), set(), {}, "0", set())
     b.states.add("S")
     b.states.add("A")
     b.states.add("B")
     b.states.add("C")
     b.states.add("D")

     b.init_state = "S"
     b.final_states.add(frozenset(["A"]))
     b.final_states.add(frozenset(["B"]))
     b.final_states.add(frozenset(["C"]))
     b.final_states.add(frozenset(["D"]))

     b.transitions[frozenset(["S"])] = {}
     b.transitions[frozenset(["S"])]["a"] = {"A", "C", "D"}
     b.transitions[frozenset(["S"])]["b"] = {"A", "B", "C"}

     b.transitions[frozenset(["A"])] = {}
     b.transitions[frozenset(["A"])]["a"] = set()
     b.transitions[frozenset(["A"])]["b"] = {"A", "B"}

     b.transitions[frozenset(["B"])] = {}
     b.transitions[frozenset(["B"])]["a"] = {"A"}
     b.transitions[frozenset(["B"])]["b"] = {"B"}

     b.transitions[frozenset(["C"])] = {}
     b.transitions[frozenset(["C"])]["a"] = {"C","D"}
     b.transitions[frozenset(["C"])]["b"] = set()

     b.transitions[frozenset(["D"])] = {}
     b.transitions[frozenset(["D"])]["a"] = {"D"}
     b.transitions[frozenset(["D"])]["b"] = {"C"}

     b.alphabet.add("a")
     b.alphabet.add("b")

     b.minimize()

    #testing
     a = FiniteAutomaton(set(), set(), {}, "0", set())
     a.states.add("S")
     a.states.add("A")
     a.states.add("B")
     a.states.add("C")
     a.states.add("D")

     a.init_state = "S"
     a.final_states.add(frozenset(["S"]))
     a.final_states.add(frozenset(["C"]))
     a.final_states.add(frozenset(["D"]))

     a.transitions[frozenset(["S"])] = {}
     a.transitions[frozenset(["S"])]["a"] = {"B", "C"}
     a.transitions[frozenset(["S"])]["b"] = {"A", "D"}

     a.transitions[frozenset(["A"])] = {}
     a.transitions[frozenset(["A"])]["a"] = {"B"}
     a.transitions[frozenset(["A"])]["b"] = {"A"}

     a.transitions[frozenset(["B"])] = {}
     a.transitions[frozenset(["B"])]["a"] = {"A"}
     a.transitions[frozenset(["B"])]["b"] = {"B"}

     a.transitions[frozenset(["C"])] = {}
     a.transitions[frozenset(["C"])]["a"] = {"C"}
     a.transitions[frozenset(["C"])]["b"] = {"D"}

     a.transitions[frozenset(["D"])] = {}
     a.transitions[frozenset(["D"])]["a"] = {"D"}
     a.transitions[frozenset(["D"])]["b"] = {"C"}

     a.alphabet.add("a")
     a.alphabet.add("b")

     a.minimize()
test()
