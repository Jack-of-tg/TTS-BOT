import os
import pyrogram
from pyromod import listen
from pyrogram import filters, Client
from pyrogram.types import ForceReply
from gtts import gTTS
from gtts.lang import tts_langs


if bool(os.environ.get("WEBHOOK", False)): 
    from sample_config import Config
else:
    from config import Config

tts = Client(
    "text_to_speech_bot",
    api_id=Config.APP_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.TG_BOT_TOKEN,
)

languages = '''\
    "af" for >> "Afrikaans",
    "ar" for >> "Arabic",
    "bn" for >> "Bengali",
    "bs" for >> "Bosnian",
    "ca" for >> "Catalan",
    "cs" for >> "Czech",
    "cy" for >> "Welsh",
    "da" for >> "Danish",
    "de" for >> "German",
    "el" for >> "Greek",
    "en" for >> "English",
    "eo" for >> "Esperanto",
    "es" for >> "Spanish",
    "et" for >> "Estonian",
    "fi" for >> "Finnish",
    "fr" for >> "French",
    "gu" for >> "Gujarati",
    "hi" for >> "Hindi",
    "hr" for >> "Croatian",
    "hu" for >> "Hungarian",
    "hy" for >> "Armenian",
    "id" for >> "Indonesian",
    "is" for >> "Icelandic",
    "it" for >> "Italian",
    "ja" for >> "Japanese",
    "jw" for >> "Javanese",
    "km" for >> "Khmer",
    "kn" for >> "Kannada",
    "ko" for >> "Korean",
    "la" for >> "Latin",
    "lv" for >> "Latvian",
    "mk" for >> "Macedonian",
    "ml" for >> "Malayalam",
    "mr" for >> "Marathi",
    "my" for >> "Myanmar (Burmese)",
    "ne" for >> "Nepali",
    "nl" for >> "Dutch",
    "no" for >> "Norwegian",
    "pl" for >> "Polish",
    "pt" for >> "Portuguese",
    "ro" for >> "Romanian",
    "ru" for >> "Russian",
    "si" for >> "Sinhala",
    "sk" for >> "Slovak",
    "sq" for >> "Albanian",
    "sr" for >> "Serbian",
    "su" for >> "Sundanese",
    "sv" for >> "Swedish",
    "sw" for >> "Swahili",
    "ta" for >> "Tamil",
    "te" for >> "Telugu",
    "th" for >> "Thai",
    "tl" for >> "Filipino",
    "tr" for >> "Turkish",
    "uk" for >> "Ukrainian",
    "ur" for >> "Urdu",
    "vi" for >> "Vietnamese",
    "zh-CN" for >> "Chinese",
    "zh-TW" for >> "Chinese (Mandarin/Taiwan)",
    "zh" for >> "Chinese (Mandarin)"'''


@tts.on_message(filters.command(["lang"]))
async def lang(client, message):
    await message.reply_text(
        text=f"Available languages and codes for them  :- \n {languages}"
    )


@tts.on_message(filters.command(["start"]))
async def start(client, message):
    await message.reply_text(
        text=f"**Hi {message.from_user.mention}, I am a simple text to speech bot**"
    )


@tts.on_message(filters.text & ~filters.reply)
async def texf(client, message):
    userid = str(message.chat.id)
    if not os.path.isdir(f"./DOWNLOADS/{userid}"):
        os.makedirs(f"./DOWNLOADS/{userid}") 

        language = await client.ask(
            message.chat.id,
            "**Plz enter the language code.\nTo see supported languages with thier code**,use /lang",
            reply_markup=ForceReply(True),
        )  

        language_to_audio = language.text.lower()
    if language.text.lower() not in tts_langs():
        await message.reply_text(
            "`Unsupported Language Code, Please use /lang and retry 👀.`",
            quote=True,
            parse_mode="md"
        )
    else:
        a = await message.reply_text(
            "`Processing`",
            quote=True,
            parse_mode="md"
        )
    new_file  = "./DOWNLOADS" + "/" + userid + "/" + "Audio.mp3"
    myobj = gTTS(text=message.text, lang=language_to_audio, slow=False)   
    myobj.save(new_file)
    await message.reply_audio(new_file)
    await a.edit("**Thanks for using me.**")


tts.run()
