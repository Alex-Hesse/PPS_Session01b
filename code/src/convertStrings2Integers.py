from copy import deepcopy


class ConvertStrings2Integers():
    _instance = None

    def __new__(cls, *args, **kwargs):
        """Macht klasse zum Singelton
        """
        # check ob es schon eine instanz gibt
        if cls._instance is None:
            # erzeuge eine falls es noch keine gibt
            cls._instance = super(ConvertStrings2Integers, cls).__new__(cls)
        return cls._instance

    def __init__(self, strings: list[str] = []):
        """Class to convert strings to integers and back, to avoid string comparison.

        Args:
            strings (list[str], optional): list of strings that will be converted. Defaults to [].
        """
        if not hasattr(self, "__map"):
            self.__map = []
        for string in strings:
            self.str2int(string)

    def obj2int(self, obj):

        if type(obj) == str:
            obj = self.str2int(obj)
        else:
            obj = deepcopy(obj)
            for i in range(len(obj)):
                if type(obj[i]) == str:
                    obj[i] = self.str2int(obj[i])
                else:
                    try:
                        obj[i] = self.obj2int(obj[i])
                    except TypeError:
                        raise TypeError(
                            "ConvertStrings2Ints: obj2int: expect nested obj containing strings")
        return obj

    def obj2str(self, obj):

        if type(obj) == int:
            obj = self.int2str(obj)
        else:
            obj = deepcopy(obj)
            for i in range(len(obj)):
                if type(obj[i]) == int:
                    obj[i] = self.int2str(obj[i])
                else:
                    try:
                        obj[i] = self.obj2str(obj[i])
                    except TypeError:
                        raise TypeError(
                            "ConvertStrings2Ints: obj2istr: expect nested obj containing integers")
        return obj

    def int2str(self, integer: int) -> str:
        """converts integer back to the original string

        Args:
            integer (int): integer which has been created

        Raises:
            KeyError: if integer doesnt belong to any string

        Returns:
            str: original string
        """
        if integer < len(self.__map):
            return self.__map[integer]
        else:
            raise KeyError(
                f"ConvertStrings2Ints: int2str: integer '{integer}' doesn't belong to any string.")

    def str2int(self, string: str) -> int:
        """converts string to integer

        Args:
            string (str): any string

        Returns:
            int: corresponding integer
        """
        if string not in self.__map:
            self.__map.append(string)
            integer = len(self.__map) - 1
        else:
            integer = self.__map.index(string)
        return integer
