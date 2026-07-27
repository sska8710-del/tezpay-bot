import asyncio
import logging
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart

BOT_TOKEN = "8610505122:AAFFlFknd_OFvWHHryfqbOkd38XheudofUY"
ADMIN_ID = 6680091637

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(
        "👋 **Добро пожаловать в службу поддержки TezPay!**\n\n"
        "Напишите ваш вопрос или что вы хотите приобрести (USDT / Stars / TON), "
        "и оператор ответит вам в ближайшее время."
    )

@dp.message(F.chat.id != ADMIN_ID)
async def forward_to_admin(message: types.Message):
    await message.forward(chat_id=ADMIN_ID)
    await message.reply("✅ Сообщение доставлено оператору! Ожидайте ответа.")

@dp.message(F.chat.id == ADMIN_ID)
async def reply_to_user(message: types.Message):
    if message.reply_to_message and message.reply_to_message.forward_from:
        user_id = message.reply_to_message.forward_from.id
        try:
            await bot.send_message(chat_id=user_id, text=message.text)
            await message.reply("🚀 Ответ отправлен клиенту!")
        except Exception as e:
            await message.reply(f"❌ Ошибка отправки: {e}")
    else:
        await message.reply("⚠️ Нажмите «Ответить» (Reply) на пересланное сообщение клиента!")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if name == "__main__":
    asyncio.run(main())
