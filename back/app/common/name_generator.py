class NameGenerator:
    @staticmethod
    def generate_username_from_email(email: str) -> str:
        """Generate a username from an email address

        Args:
            email (str): an external user email address

        Returns:
            str: a unique username from the given email
        """
        username: str = email.split("@")[0]
        username.replace(".", " ")
        return username.capitalize()
