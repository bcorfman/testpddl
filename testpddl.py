__author__ = 'brandon_corfman'
from pddlpy import DomainProblem
from search import Problem, astar_search

class PlanningProblem(Problem):
    def __init__(self, domain_problem):
        self.dp = domain_problem
        self.goals = {tuple(atom.predicate) for atom in self.dp.goals()}
        initial = tuple([tuple(atom.predicate) for atom in self.dp.initialstate()])
        Problem.__init__(self, initial)

    def actions(self, state):
        for op_name in self.dp.operators():
            for op in self.dp.ground_operator(op_name):
                if op.precondition_pos.issubset(state) and not op.precondition_neg.intersection(state):
                    yield op

    def result(self, state, action):
        new_state = set(state)
        for atom in action.effect_pos:
            new_state.add(atom)
        for atom in action.effect_neg:
            new_state.remove(atom)
        return tuple(new_state)

    def goal_test(self, state):
        return self.goals.issubset(set(state))

    def h(self, node):
        return len(self.goals - set(node.state))  # number of unsatisfied goals


def main():
    dp = DomainProblem('domain-03.pddl', 'problem-03.pddl')
    print(astar_search(PlanningProblem(dp)).solution())

if __name__ == '__main__':
    main()


