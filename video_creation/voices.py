

from utils.console import print_step, print_substep

import os

from rich.console import Console

from TTS.engine_wrapper import TTSEngine
from TTS.GTTS import GTTS
from TTS.streamlabs_polly import StreamlabsPolly
from TTS.aws_polly import AWSPolly
from TTS.TikTok import TikTok

from utils.console import print_table, print_step


console = Console()

TTSProviders = {
    "GoogleTranslate": GTTS,
    "AWSPolly": AWSPolly,
    "StreamlabsPolly": StreamlabsPolly,
    "TikTok": TikTok,
}

VIDEO_LENGTH: int = 40  # secs


def save_text_to_mp3(reddit_obj:dict[str])->tuple[int,int]:
    """Saves text to MP3 files. Goes through the reddit_obj and generates the title MP3 file and a certain number of comments until the total amount of time exceeds VIDEO_LENGTH seconds.

    Args:
        reddit_obj (dict[str]): Reddit object received from reddit API in reddit/subreddit.py

    Returns:
        tuple[int,int]: (total length of the audio, the number of comments audio was generated for)
    """
    
    env = os.getenv("TTSCHOICE", "")
    if env.casefold() in map(lambda _: _.casefold(), TTSProviders):
        text_to_mp3 = TTSEngine(
            get_case_insensitive_key_value(TTSProviders, env), reddit_obj
        )
    else:
        choice = ""
        while True:
            print_step("Please choose one of the following TTS providers: ")
            print_table(TTSProviders)
            choice = input("\n")
            if choice.casefold() in map(lambda _: _.casefold(), TTSProviders):
                break
            print("Unknown Choice")
        text_to_mp3 = TTSEngine(
            get_case_insensitive_key_value(TTSProviders, choice), reddit_obj
        )

    return text_to_mp3.run()


def get_case_insensitive_key_value(input_dict, key):
    return next(
        (
            value
            for dict_key, value in input_dict.items()
            if dict_key.lower() == key.lower()
        ),
        None,
    )
