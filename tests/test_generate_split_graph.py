import path_setup

from src.generate_split_graph import GenerateSplitGraph

def test_generate_split_graph():
    factory = GenerateSplitGraph('SplitGraph', 10)
    split_graph = factory.generate_graph()
    print(split_graph)

if __name__ == '__main__':
    test_generate_split_graph()