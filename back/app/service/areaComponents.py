from enum import Enum


class Service(Enum):
    AREA = "Area"
    GMAIL = "GMail"
    DISCORD = "Discord"
    GITHUB = "Github"
    SPOTIFY = "Spotify"
    GITLAB = "Gitlab"
    TIME = "Time"


class IAction:
    def __init__(self):
        self.name = "IAction"
        self.description = "No description where provided"
        self.service = Service.AREA

    async def get_params(self):
        return {}

    async def is_triggered(self, user, params) -> bool:
        if user is None:
            return False
        return True


class IReaction:
    """An interface for a reaction object"""

    def __init__(self):
        self.name = "IReaction"
        self.description = "No description where provided"
        self.service = Service.AREA

    async def get_params(self) -> dict:
        """Function called by the periodic trigger in order to get the needed parameters for the action

        Returns:
            Dict:
                parameters needed by the action,
                keys are the name of the parameter and values are the default values assign to them
        """
        return {}

    async def react(self, user: dict, params: dict):
        """Function called by the periodic trigger when the coresponding action is triggered,
        This function should perform the desired reaction based on the provided user and params.

        Args:
            user (dict):
                the user for witch the reaction should trigger,
                the format of this dict is the same than in the database.
            params (dict):
                the needed parameters for the reaction to trigger,
                they where provited by the get_params method.
        """
        print(
            f"IReaction was triggered for user {user['username']} with params {params}"
        )
