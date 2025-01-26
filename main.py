import os
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters, CallbackContext

# Bot tokeningizni kiriting
TOKEN = '7981392410:AAGea3TNmuu3X-ApWkddzKvtsnA3o4BbY84'

# /start komanda
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    main_menu = [
        ['☘️ Mahsulotlarimiz', 'ℹ️ Biz haqimizda'],
        ["📦 Buyurtma berish", '☎️ Aloqa']
    ]
    reply_markup = ReplyKeyboardMarkup(main_menu, resize_keyboard=True)
    await update.message.reply_text(
        """***Asosiy menu.***""",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )


# Katalog bo‘limini ko‘rsatish
async def show_catalog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    catalog_menu = [
        ['🌟 Elaro Premium', '💠 Elaro SUZUVCHI Hovuz tagliklari'],
        ['🧓 Kattalar Uchun Tagliklar', '🩲 Elaro PANTS Tagliklar-Trusiklar'],
        ["🍼 Vinder Baby PREMIUM Tagliklari", '🛏 Plonka Tagliklar'],
        ['🔙 Ortga']
    ]
    reply_markup = ReplyKeyboardMarkup(catalog_menu, resize_keyboard=True)
    await update.message.reply_text(
        "Pastdagi tugmalardan o'zingizga kerakli mahsulot kategoriyasini tanlang:",
        reply_markup=reply_markup
    )


# Mahsulotlar ro'yxati
PRODUCTS = {
    "baby": {
        "1": "Elaro Premium 1 NewBorn (2-5 kg, 72 dona)",
        "2": "Elaro Premium 2 Mini (4-8 kg, 62 dona)",
        "3": "Elaro Premium 3 Midi (6-11 kg, 56 dona)",
        "4": "Elaro Premium 4 Maxi (9-14 kg, 52 dona)",
        "5": "Elaro Premium 5 Junior (12-17 kg, 46 dona)",
        "6": "Elaro Premium 6 X Large (15-25 kg, 40 dona)"
    },
    "adult": {
        "1": "Kattalar Tagliklar (85-125 sm, 30 dona)",
        "2": "Kattalar Tagliklar (100-150 sm, 30 dona)",
        "3": "Kattalar Tagliklar (120-170 sm, 30 dona)\n\nElaro Tursik 💸 Narxi: 57.000 so'm",
        "4": "Elaro Trusik L (100-150 sm, 8 dona)",
        "5": "Elaro Trusik M (85-125 sm, 9 dona)",
        "6": "Elaro Trusik XL (130-170 sm, 8 dona)"
    },
     "plonka": {
        "1": "Plonka taglik (600 × 600 mm, 5 dona)",
        "2": "Plonka taglik (600 × 900 mm, 5 dona)",
        "3": "VINDER Underpads (600 × 900 mm, 30 dona)"
    },
    "vinder": {
        "1": "Vinder Baby PREMIUM Materials 2 Junior (20 dona, 2 - 5 kg)",
        "2": "Vinder Baby PREMIUM Materials 2 Junior (18 dona, 4 - 8 kg)",
        "3": "Vinder Baby PREMIUM Materials 3 Junior (16 dona, 6 - 11 kg)",
        "4": "Vinder Baby PREMIUM Materials 4 Junior (14 dona, 9 - 14 kg)",
        "5": "Vinder Baby PREMIUM Materials 5 Junior (12 dona, 12 - 17 kg)",
        "6": "Vinder Baby PREMIUM Materials 6 Junior (10 dona, 15 - 25 kg)"
    },
    "pants": {
        "1": "Elaro PANTS tagliklar-trusiklar 16 dona, 6 - 11 kg",
        "2": "Elaro PANTS tagliklar-trusiklar 14 dona, 6 - 14 kg",
        "3": "Elaro PANTS tagliklar-trusiklar 12 dona, 12 - 17 kg",
        "4": "Elaro PANTS tagliklar-trusiklar 10 dona, 15 - 25 kg"
    },
    "hovuz": {
        "1": "Elaro SUZUVCHI Hovuz tagliklari (4 - 5) 🌟 16 dona, 7 - 18 kg",
        "2": "Elaro SUZUVCHI Hovuz tagliklari (3 - 4) 🌟 18 dona, 4 - 14 kg",
        "3": "Elaro SUZUVCHI Hovuz tagliklari (5 - 6) 🌟 14 dona, 11 - 25 kg"
    }
    
}

# Mahsulotlarni ko'rsatish funksiyasi
def generate_product_buttons(category):
    product_count = len(PRODUCTS[category])
    buttons = []

    # Har safar 3 ta tugma qo'shamiz
    for i in range(0, product_count, 3):
        row = [
            InlineKeyboardButton(f"{i+1}️⃣", callback_data=f"order_{category}_{i+1}"),
            InlineKeyboardButton(f"{i+2}️⃣", callback_data=f"order_{category}_{i+2}") if i+1 < product_count else None,
            InlineKeyboardButton(f"{i+3}️⃣", callback_data=f"order_{category}_{i+3}") if i+2 < product_count else None
        ]
        buttons.append([btn for btn in row if btn])  # Faqat to'liq tugmalarni qo'shish

    return InlineKeyboardMarkup(buttons)


async def show_products(update: Update, context: ContextTypes.DEFAULT_TYPE, category: str, caption: str, photo_url: str):
    await update.message.reply_photo(
        photo=photo_url,
        caption=caption,
        parse_mode="Markdown",
        reply_markup=generate_product_buttons(category)
    )

async def show_divans(update: Update, context: ContextTypes.DEFAULT_TYPE):
    caption = "👶 ***Pampers Mahsulotlari (Elaro Premium)\n\n💸 Narxi 135.000 so'm:***\n\n" + "\n\n".join([
        f"({key}) ***{value}***" for key, value in PRODUCTS["baby"].items()
    ])
    photo_url = "https://t.me/elarobaby_baza/7"
    await show_products(update, context, "baby", caption, photo_url)

async def show_stols(update: Update, context: ContextTypes.DEFAULT_TYPE):
    caption = "🧓 ***Kattalar Uchun Tagliklar\n\n💸 Narxi: (148.000 - 194.000 so'm)***\n\n" + "\n\n".join([
        f"({key}) ***{value}***" for key, value in PRODUCTS["adult"].items()
    ])
    photo_url = "https://t.me/elarobaby_baza/11"
    await show_products(update, context, "adult", caption, photo_url)

async def plonka_taglik(update: Update, context: ContextTypes.DEFAULT_TYPE):
    caption = "🆕 ***Plonka tagliklar\n\n💸 Narxi: 90.000 so'm***\n\n" + "\n\n".join([  # Yangi kategoriyani ko'rsatish
        f"({key}) ***{value}***" for key, value in PRODUCTS["plonka"].items()
    ])
    photo_url = "https://t.me/elarobaby_baza/13"  # Yangi kategoriya rasmi URL
    await show_products(update, context, "plonka", caption, photo_url)


async def show_household_items(update: Update, context: ContextTypes.DEFAULT_TYPE):
    caption = "***Vinder Baby PREMIUM pamperslar\n\n💸 Narxi: 34.000 so'm***\n\n" + "\n\n".join([  # Yangi kategoriyani ko'rsatish
        f"({key}) ***{value}***" for key, value in PRODUCTS["vinder"].items()
    ])
    photo_url = "https://t.me/elarobaby_baza/10"  # Yangi kategoriya rasmi URL
    await show_products(update, context, "vinder", caption, photo_url)

async def show_beds(update: Update, context: ContextTypes.DEFAULT_TYPE):
    caption = "🩲 ***Elaro PANTS Tagliklar-Trusiklar\n\n💸 Narxi: 36.000 so'm***\n\n" + "\n\n".join([  # Yangi kategoriya haqida matn
        f"({key}) ***{value}***" for key, value in PRODUCTS["pants"].items()
    ])
    photo_url = "https://t.me/elarobaby_baza/12"  # Yangi kategoriya rasmi URL
    await show_products(update, context, "pants", caption, photo_url)


async def show_shelves(update: Update, context: ContextTypes.DEFAULT_TYPE):
    caption = "💠 *** Elaro SUZUVCHI Hovuz tagliklari:***\n\n" + "\n\n".join([  # Yangi kategoriya haqida matn
        f"({key}) ***{value}***" for key, value in PRODUCTS["hovuz"].items()
    ])
    photo_url = "https://t.me/elarobaby_baza/8"  # Yangi kategoriya rasmi URL
    await show_products(update, context, "hovuz", caption, photo_url)


# Tugma bosilganda mahsulotni saqlash va aloqa ma'lumotlarini so'rash
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    category, product_number = query.data.replace("order_", "").split("_")
    selected_product = PRODUCTS[category].get(product_number, "Noma'lum mahsulot")

    context.user_data["selected_product"] = selected_product
    contact_buttons = [
        [KeyboardButton("📞 Telefon raqamini yuborish", request_contact=True)],
        [KeyboardButton("📍 Lokatsiyani yuborish", request_location=True)],
        [KeyboardButton("🔙 Ortga")]
    ]
    reply_markup = ReplyKeyboardMarkup(contact_buttons, resize_keyboard=True)
    await query.message.reply_text(f"📞 {selected_product} uchun telefon raqamingizni yuboring:", reply_markup=reply_markup)

# Telefon va lokatsiyani qabul qilish
async def receive_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.contact:
        user_contact = update.message.contact.phone_number
        context.user_data["user_contact"] = user_contact
        await update.message.reply_text("📍 Endi lokatsiyangizni yuboring:", reply_markup=ReplyKeyboardMarkup([[KeyboardButton("📍 Lokatsiyani yuborish", request_location=True), ("🔙 Ortga")]], resize_keyboard=True))

    elif update.message.location:
        latitude = update.message.location.latitude
        longitude = update.message.location.longitude
        product_name = context.user_data.get("selected_product", "Tanlanmagan mahsulot")
        user_contact = context.user_data.get("user_contact", "Tanlanmagan")

        channel_id = "-1002201576115"
        await context.bot.send_message(
            chat_id=channel_id,
            text=f"🛒 *Yangi buyurtma:*\n\n📦 *Mahsulot:* {product_name}\n📞 *Telefon:* {user_contact}\n🌍 *Lokatsiya:* [Xaritada ko‘rish](https://www.google.com/maps?q={latitude},{longitude})",
            parse_mode="Markdown"
        )
        await update.message.reply_text("✅ Buyurtmangiz qabul qilindi! Tez orada aloqaga chiqamiz.")


# Manzil
async def handle_location(update: Update, context):
    await update.message.reply_text(
        "🍼 ***Elaro Baby Mahsulotlari:***\n\n"
        "🌐 ***Ijtimoiy tarmoqlarimiz:***\n"
        "- ***Instagram:*** [elarobaby_tashkent](https://www.instagram.com/elarobaby_tashkent/)\n"
        "- ***Telegram:*** [Elaro Baby](https://t.me/Elaro_baby)\n\n"
        "📞 ***Hamkorlik yoki xaridlar bo‘yicha bog‘laning:***\n"
        "  - ☎️ +99888 084 99 99\n"
        "  - ☎️ +99899 929 99 91\n\n"
        "- Mahsulotlar haqida batafsil ma'lumot olish uchun biz bilan bog‘laning!",
        parse_mode="Markdown"
    )



# Aloqa
async def handle_contact(update: Update, context):
    about_text = (
        "📌 *Elaro Baby* brendi 2023-yilda asos solingan!\n\n"
        "🇯🇵 Mahsulotlarimiz Yaponiyaning eng zamonaviy texnologiyasi asosida 🇨🇳 Xitoyda ishlab chiqarilmoqda.\n\n"
        "😉 Hozirgi kunga kelib, mahsulotlarimiz assortimenti kengayib bormoqda.\n\n"
        "🇺🇿 O‘zbekistonning barcha hududlarida raqobatbardosh mahsulotlarimizni ko‘rishingiz va xarid qilishingiz mumkin ✅"
    )
    await update.message.reply_text(about_text, parse_mode="Markdown")

async def handle_order(update: Update, context: CallbackContext):
    # "Ortga" va "Guruhga qo‘shilish" tugmalari
    order_menu = [
        [KeyboardButton("🔙 Ortga")],
        [KeyboardButton("📢 Kanalimizga qo‘shilish")]
    ]
    reply_markup = ReplyKeyboardMarkup(order_menu, resize_keyboard=True)

    # To‘lov uchun karta raqamlari
    payment_info = (
        "💳 *To‘lov uchun karta raqamlari:*\n\n"
        "📌 *Uzcard:* 5614 6822 1353 8905\n"
        "👤 *Ism:* Islohjon Karimov\n"
        "📞 *To‘lov qilgach, biz bilan bog‘laning yoki 'Ortga' tugmasini bosing.*"
    )

    await update.message.reply_text(payment_info, reply_markup=reply_markup, parse_mode="Markdown")

async def handle_group_join(update: Update, context: CallbackContext):
    # Guruhga qo‘shilish tugmasi bosilganda linkni yuborish
    await update.message.reply_text("📢 Kanalimizga qo‘shiling: https://t.me/Elaro_baby")


TOKEN = "7981392410:AAH2kq4WcfzRvjFjqZDVY7Kz3PlFQDYVB9I"  # Bot tokeningizni kiritishni unutmang

# Foydalanuvchi xabarlarini boshqarish
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if text == '☘️ Mahsulotlarimiz':
        await show_catalog(update, context)
    elif text == 'ℹ️ Biz haqimizda':
        await handle_contact(update, context)
    elif text == "📦 Buyurtma berish":
        await handle_order(update, context)
    elif text == '☎️ Aloqa':
        await handle_location(update, context)
    elif text == '🔙 Ortga':
        await start(update, context)
    elif text == '🌟 Elaro Premium':
        await show_divans(update, context)
    elif text == '🧓 Kattalar Uchun Tagliklar':
        await show_stols(update, context)
    elif text == '🩲 Elaro PANTS Tagliklar-Trusiklar':
        await show_beds(update, context)
    elif text == '📞 Buyurtma berish':
        await handle_order(update, context)
    elif text == '💠 Elaro SUZUVCHI Hovuz tagliklari':
        await show_shelves(update, context)
    elif text == "🍼 Vinder Baby PREMIUM Tagliklari":
        await show_household_items(update, context)
    elif text == "🛏 Plonka Tagliklar":
        await plonka_taglik(update, context)
    elif text == "📢 Kanalimizga qo‘shilish":
        await handle_group_join(update, context)
    else:
        # Nomalum xabar yuborilganda
        await update.message.reply_text("Nomalum habar, o'zingizga kerakli tugmani bosing.")


# Botni ishga tushirish
def main():
    app = ApplicationBuilder().token("7981392410:AAGea3TNmuu3X-ApWkddzKvtsnA3o4BbY84").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.CONTACT, receive_contact))
    app.add_handler(MessageHandler(filters.LOCATION, receive_contact))

    print("Bot ishga tushdi...")
    app.run_polling()

if __name__ == '__main__':
    main()








