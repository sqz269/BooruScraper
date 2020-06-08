class IModuleConfigWindowHandler:

    def show_config(self):
        """Show the config window. should be alias for window.show
        """
        raise NotImplementedError("show_config is not implemented, please implement it")

    def load_config(self):
        """Parse and load an pre-existing ini file to UI fields
        """
        raise NotImplementedError("show_config is not implemented, please implement it")

    def save_config(self):
        """Parse and write the data in the UI fields to an ini file
        """
        raise NotImplementedError("show_config is not implemented, please implement it")
