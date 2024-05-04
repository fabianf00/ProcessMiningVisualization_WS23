from abc import ABC
from mining_algorithms.ddcal_clustering import DensityDistributionClusterAlgorithm


class MiningInterface(ABC):

    def __init__(self):
        self.graph = None
        self.min_node_size = 1.5

    def get_clusters(
        self, frequency: list[int | float]
    ) -> tuple[list[int | float], list[int | float]]:
        """use the DensityDistributionClusterAlgorithm to cluster the frequency data.
        The clusters are used to determine a scaling factor of the nodes in the graph.
        The arrays are sorted in ascending order.

        Parameters
        ----------
        frequency : list[int | float]
            The frequency data to be clustered

        Returns
        -------
        tuple[list[int | float], list[int | float]]
            A tuple containing the sorted frequency data and the labels of the sorted data
            The labels are used to determine the scaling factor of the nodes in the graph
        """
        try:
            cluster = DensityDistributionClusterAlgorithm(frequency)
            return list(cluster.sorted_data), list(cluster.labels_sorted_data)
        except ZeroDivisionError as e:
            # TODO: use logging
            print(e)
            return [frequency[0]], [1.0]

    def get_graph(self):
        return self.graph

    @classmethod
    def create_mining_instance(cls, *constructor_args):
        """Create a new instance of the mining class using the constructor arguments.

        Returns
        -------
        MiningInterface
            A new instance of the class
        """
        return cls(*constructor_args)
