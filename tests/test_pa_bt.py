import py_trees
from py_trees.composites import Selector, Sequence
from py_trees.behaviours import Count
from py_trees.trees import BehaviourTree
from py_trees.visitors import DisplaySnapshotVisitor
from py_trees.common import Status

# from py_trees.idioms import pick_up_where_you_left_off
def is_finished(tree):
    return tree.root.status in (Status.SUCCESS, Status.FAILURE)


def tick_until_finished(tree):
    while not is_finished(tree):
        tree.tick()
    return tree


def plan_tree(goal_conditions, actions, current_state):
    tree = BehaviourTree(root=Sequence("Sequence"))
    tree.root.add_children([condition for condition in goal_conditions])

    while True:  # improve this condition
        tree = refine_actions(tree)
        tree = tick_until_finished(tree)
        if tree.root.status == Status.SUCCESS:
            return tree
        else:
            condition = get_condition_to_expand(tree)
            tree, new_sub_tree = expand_tree(tree, condition)
            while exists_conflict(tree):
                tree = increase_priority(tree, new_sub_tree)


def main():
    root = Sequence("Sequence")

    task_a = Count(name="Task A", fail_until=0, running_until=3, success_until=100)
    task_b = Count(name="Task B", fail_until=1, running_until=3, success_until=100)

    root.add_children([task_a])

    tree = BehaviourTree(root=root)
    tree.add_visitor(DisplaySnapshotVisitor())
    tree.setup()
    print(tree.tick())
    import ipdb

    ipdb.set_trace()
    # [tree.tick() for a in range(10)]


if __name__ == "__main__":
    main()
