from .placement_options import PlacementOptions
from .placement_result import PlacementResult


class PlexLayoutPlacement:
    def __init__(self):
        """Initializes new instance of the PlexLayoutPlacement class."""
        self.__kinds = ["root", "parent", "child", "reference"]
        self.__default_options = PlacementOptions()

    def place(self, state, options=None):
        """
        Returns positions for thoughts from specified state.
        :rtype: plugins.app.gui.plex.placement_result.PlacementResult
        :type options: PlacementOptions
        :type state: PlexState
        :param state: State to calculate positions for
        :param options: Options
        :return: Placement result
        """
        options = options or self.__default_options
        result = {}
        for kind in self.__kinds:
            thoughts = state.by_state(kind)
            thoughts = sorted(thoughts, key=lambda t: t.title)
            position = self.__position(kind, thoughts, options)
            result.update(position)

        return PlacementResult(result)

    @staticmethod
    def __position(state, thoughts, options):
        if state == "root" and len(thoughts) > 0:
            return {thoughts[0].key: [0, 0]}

        result = {}
        if state in ["child", "parent"]:
            y = -options.height/2.75 if state == "parent" else options.height/2.75
            count = min(3, len(thoughts))
            while count > 0:
                v = []
                for x in range(0, count):
                    v.append(thoughts.pop(0))
                thoughts_to_place = len(v)

                if thoughts_to_place == 1:
                    result[v[0].key] = [0, y]
                else:
                    for idx, t in enumerate(v):
                        width = options.width/1.375
                        x = (width / (thoughts_to_place-1)) * idx
                        result[t.key] = [x - width / 2, y]

                y += options.step
                count = min(3, len(thoughts))

        if state in ["reference"]:
            y = 0
            for rt in thoughts:
                result[rt.key] = [-options.width/2.75, y]
                y -= options.step

        return result


