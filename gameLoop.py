from anthropos import Anthropos

player_list = "Trent,Sam,Joe,Kate,Dan,TY,Tom,Raelee,Alix,CoryMolly,Ella,Taya,Kaylee,Kelsie,Conner".split(
    ",")
a = Anthropos(player_list[0], 0)
a.beget(Anthropos(player_list[1], 1))
a.left_child.beget(Anthropos(player_list[2], 2))


class LineagePrinter:

    def build_tree_from_adam(self, adam):
        if adam is not None:
            self.tree += adam.name

            right_ptr = "└──"
            if adam.right_child is not None:
                left_ptr = "├──"
            else:
                left_ptr = "└──"
            self.build_tree("", left_ptr, adam.left_child, adam.right_child is not None)
            self.build_tree("", right_ptr, adam.right_child, False)

    def build_tree(self, pad, ptr, adam, has_right_sibling):
        if adam is not None:
            self.tree += "\n"
            self.tree += pad
            self.tree += ptr
            self.tree += adam.name
            if has_right_sibling:
                new_pad = pad + "│  "
            else:
                new_pad = pad + "   "
            right_ptr = "└──"
            if adam.right_child is not None:
                left_ptr = "├──"
            else:
                left_ptr = "└──"
            self.build_tree(new_pad, left_ptr, adam.left_child, adam.right_child is not None)
            self.build_tree(new_pad, right_ptr, adam.right_child, False)

    def __init__(self):
        self.tree = ""

    def print_tree(self, adam):
        self.build_tree_from_adam(adam)
        print(self.tree)
        self.tree = ""


lin_prin = LineagePrinter()
lin_prin.print_tree(a)
