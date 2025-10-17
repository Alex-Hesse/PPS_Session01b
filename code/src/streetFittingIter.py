from streetFitting import StreetFitting
import time


class StreetFittingIter(StreetFitting):
    def __init__(self, startStreet, houseRules, neighborRules, emptyVal=-1, ruleOrder=[], minIter=1e10):
        super().__init__(startStreet, houseRules, neighborRules, emptyVal, ruleOrder)
        self.minIter = minIter
        self.iteration = 0

    def _recursiveFitting(self, streets: list, iteration: int = 0):
        """Applies house and Neigbor rules in ruleOrder to the street

        Args:
            streets (list): list of streets that should be checked
            iteration (int, optional): iteration counter. Defaults to 0.
        """
        self.iteration += 1
        if self.iteration > self.minIter:
            return []
        super()._recursiveFitting(streets, iteration)

    def recursiveFitting(self, streets: list) -> list:
        """starts the fitting algorithm with the given streets

        Args:
            street (list): list of allowed start configurations

        Returns:
            list: final streets with all rules applied
        """
        self.iteration = 0
        self._recursiveFitting(streets)
        return self.fittingStreets
