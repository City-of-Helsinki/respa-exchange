from respa_exchange.xml import NAMESPACES, T


class ItemID:
    def __init__(self, id, change_key):
        self.id = id
        self.change_key = change_key

    def to_xml(self):
        return T.ItemId(Id=self.id, ChangeKey=self.change_key)

    @classmethod
    def from_tree(cls, tree):
        """
        Get the first Item ID from the given tree (likely a response)

        :param tree:
        :rtype: ItemID
        """
        item_id = tree.find("*//t:ItemId", namespaces=NAMESPACES)
        if item_id is None:
            raise Exception("Something went wrong.")  # TODO: WHAT WENT WRONG? WHAT DID YOU SEE?
        return cls(
            id=item_id.attrib["Id"],
            change_key=item_id.attrib.get("ChangeKey")
        )
