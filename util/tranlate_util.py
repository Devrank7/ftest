from aiogram.types import User
from googletrans import Translator

from db.enum.enums import Language
from db.nosql.redis_op import RedisDictCachable
from db.service import UserService

translator = Translator()

MAX_LEN_CACHE = 200


async def adjust_lang(text: str, lang: Language) -> dict[str, str]:
    lan = lang.value.strip().lower()
    print('text = ',text)
    detected = translator.detect(text)
    if lan == detected.lang:
        return {"text": text, "lang": detected.lang}
    translated = translator.translate(text, dest=str(lan))
    return {"text": translated.text, "lang": detected.lang}


async def answer_by_lang_with_redis(text: str, chat_id: int, user_service: UserService, max_len: int = 100) -> str:
    user = await user_service.read(chat_id)
    return await answer_by_lang_with_redis_read(text, user, max_len)


async def answer_by_lang_with_redis_read(text: str, user: User, max_len: int = 100) -> str:
    async def cacheable_function(texts: str):
        return await adjust_lang(text=texts, lang=user.lang)

    redis = RedisDictCachable(key=f"{text}_{user.lang.value.lower()}", func=cacheable_function)
    dic = await redis.cacheable() if len(text) < min(max_len, MAX_LEN_CACHE) else await cacheable_function(text)
    return dic['text']
