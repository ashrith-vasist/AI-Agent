import random
from dataclasses import dataclass

@dataclass
class DSAQuestion:
    topic: str
    question: str
    logic: str


QUESTION_BANK = {
    "arrays": [
        DSAQuestion(
            "arrays",
            "How would you find the only duplicate in an array of N+1 integers?",
            "Use a Hash Set to track seen numbers or Floyd's cycle detection for O(1) space."
        ),
        DSAQuestion(
            "arrays",
            "How do you find the Kth largest element in an unsorted array?",
            "Use a Min Heap of size K or the QuickSelect algorithm."
        ),
    ],
    "linked_lists": [
        DSAQuestion(
            "linked_lists",
            "How do you detect a cycle in a linked list?",
            "Use Floyd’s slow and fast pointer technique."
        ),
        DSAQuestion(
            "linked_lists",
            "How would you reverse a singly linked list?",
            "Iterate while adjusting next pointers using prev, curr, and next."
        ),
    ],
    "trees": [
        DSAQuestion(
            "trees",
            "How do you find the lowest common ancestor in a BST?",
            "Traverse left or right depending on node values."
        ),
        DSAQuestion(
            "trees",
            "How do you perform level order traversal of a tree?",
            "Use BFS with a queue."
        ),
    ],
    "strings": [
        DSAQuestion(
            "strings",
            "How do you check if two strings are anagrams?",
            "Compare character frequency maps or sorted strings."
        ),
        DSAQuestion(
            "strings",
            "How do you find the longest palindromic substring?",
            "Expand around center or use Manacher’s algorithm."
        ),
    ],
}
