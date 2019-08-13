from programy.utils.logging.ylogger import YLogger

from programy.clients.events.client import EventBotClient
from programy.clients.events.console.config import ConsoleConfiguration

class Args(object):
    def __init__(self):
        self.args = None
        self._bot_root = 'storage'
        self._logging = 'config\windows\logging.yaml'
        self._config_name = 'config\windows\config.yaml'
        self._config_format = 'yaml'
        self._no_loop = False
        self._substitutions = None

    def parse_args(self, client):
        pass

    @property
    def bot_root(self):
        return self._bot_root

    @bot_root.setter
    def bot_root(self, root):
        self._bot_root = root

    @property
    def logging(self):
        return self._logging

    @property
    def config_filename(self):
        return self._config_name

    @property
    def config_format(self):
        return self._config_format

    @property
    def noloop(self):
        return self._no_loop

    @property
    def substitutions(self):
        return self._substitutions



class EventBotClientNoCmdArgs(EventBotClient):

    def parse_arguments(self, *args, **kwargs):
        client_args = Args()
        client_args.parse_args(self)
        return client_args

class ConsoleBotClient(EventBotClientNoCmdArgs):

    def __init__(self, argument_parser=None):
        self.running = False
        EventBotClient.__init__(self, "Console", argument_parser)

    def get_client_configuration(self):
        return ConsoleConfiguration()

    def add_client_arguments(self, parser=None):
        return

    def parse_args(self, arguments, parsed_args):
        return

    def get_question(self, client_context, input_func=input):
        ask = "%s " % self.get_client_configuration().prompt
        return input_func(ask)

    def display_startup_messages(self, client_context):
        self.process_response(client_context, client_context.bot.get_version_string(client_context))
        initial_question = client_context.bot.get_initial_question(client_context)
        self._renderer.render(client_context, initial_question)

    def process_question(self, client_context, question):

        self._questions += 1

        return client_context.bot.ask_question(client_context , question, responselogger=self)

    def render_response(self, client_context, response):
        # Calls the renderer which handles RCS context, and then calls back to the client to show response
        self._renderer.render(client_context, response)

    def process_response(self, client_context, response):
        print(response)

    def process_question_answer(self, client_context):
        question = self.get_question(client_context)
        response = self.process_question(client_context, question)
        self.render_response(client_context, response)

    def wait_and_answer(self):
        running = True
        try:
            client_context = self.create_client_context(self._configuration.client_configuration.default_userid)
            self.process_question_answer(client_context)
        except KeyboardInterrupt as keye:
            running = False
            client_context = self.create_client_context(self._configuration.client_configuration.default_userid)
            self._renderer.render(client_context, client_context.bot.get_exit_response(client_context))
        except Exception as excep:
            YLogger.exception(self, "Oops something bad happened !", excep)
        return running

    def prior_to_run_loop(self):
        client_context = self.create_client_context(self._configuration.client_configuration.default_userid)
        self.display_startup_messages(client_context)


if __name__ == '__main__':

    print("Initiating Console Client...")

    def run():
        console_app = ConsoleBotClient()
        console_app.run()

    run()



class ConsoleBotClientMod(client.ConsoleBotClient):

    def parse_arguments(self, *args, **kwargs):
        client_args = Args()
        client_args.parse_args(self)
        return client_args


a = ConsoleBotClientMod()
a.run()
