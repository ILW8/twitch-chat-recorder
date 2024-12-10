from twitchio.ext import commands
from dotenv import load_dotenv
import os
import datetime


class Bot(commands.Bot):
    def __init__(self, token: str):
        assert token is not None
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        super().__init__(token=token, prefix='|', initial_channels=['btmc', 'osulive', 'osulive_2'])

        self.init_time = datetime.datetime.utcnow().isoformat()
        self.log_files = dict()
        self.data_dir = "logs"

        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def __del__(self):
        for channel_name, log_file in self.log_files.items():
            print(f"closing handle for {channel_name}")
            log_file.close()

    async def event_ready(self):
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    async def event_message(self, message):
        # Messages with echo set to True are messages sent by the bot, ignore them.
        if message.echo:
            return

        if message.channel.name not in self.log_files:
            file_path = os.path.join(self.data_dir, f"{self.init_time}__{message.channel.name}.txt")
            self.log_files[message.channel.name] = open(file_path, "w", encoding="utf-8")

        self.log_files[message.channel.name].write(message.raw_data + "\n")
        print(f"#{message.channel.name}:\t{message.author.name}\t\t{message.content}")


if __name__ == '__main__':
    load_dotenv()
    bot = Bot(os.getenv("BOT_TOKEN"))
    bot.run()
