import programy.clients.events.console.client as client
import programy.clients.args as args


class Args(args.ClientArguments):
    def __init__(self):
        self.args = None
        self._bot_root = 'storage'
        self._logging = 'config\windows\logging.yaml'
        self._config_name = 'config\windows\config.yaml'
        self._config_format = 'yaml'
        self._no_loop = False
        self._substitutions = None


class ConsoleBotClientMod(client.ConsoleBotClient):

    def parse_arguments(self, *args, **kwargs):
        client_args = Args()
        client_args.parse_args(self)
        return client_args


a = ConsoleBotClientMod()
a.run()
