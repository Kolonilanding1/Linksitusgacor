import os
import asyncio
import logging
import threading
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

import pytz
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, Bot
from telegram.constants import ParseMode
from telegram.error import BadRequest
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# Pindahkan verification_map ke sini supaya global dan bisa diakses semua fungsi
verification_map = {
    'BOLAPELANGI_VERIFIKASI': {
        'channel': '@bola_pelangi',
        'groups': ['@InfoFreebet4D', '@SITUSLINKGACOR4D'],
        'success_text': '✅ Anda telah berhasil verifikasi BOLAPELANGI.',
        'last_action': 'VERIFIKASI_BOLAPELANGI'
    },
    'BOLAPELANGI2_VERIFIKASI': {
        'channel': '@Bolapelangi2ofc',
        'groups': ['@InfoFreebet4D', '@SITUSLINKGACOR4D'],
        'success_text': '✅ Anda telah berhasil verifikasi BOLAPELANGI2.',
        'last_action': 'VERIFIKASI_BOLAPELANGI2'
    },
    'KOLONI4D_VERIFIKASI': {
        'channel': '@koloni4d_official1',
        'groups': ['@InfoFreebet4D', '@SITUSLINKGACOR4D'],
        'success_text': '✅ Anda telah berhasil verifikasi KOLONI4D.',
        'last_action': 'VERIFIKASI_KOLONI4D'
    },
    'SINGASLOT_VERIFIKASI': {
        'channel': '@Infosingaslot',
        'groups': ['@InfoFreebet4D', '@SITUSLINKGACOR4D'],
        'success_text': '✅ Anda telah berhasil verifikasi SINGASLOT.',
        'last_action': 'VERIFIKASI_SINGASLOT'
    },
    
}
auto_task = None
API_TOKEN = os.environ["API_TOKEN"]
GROUP_USERNAME = '@SITUSLINKGACOR4D'
TARGET_CHAT_ID = -1002255700000  # Ganti sesuai target

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

messages = [
    {
        "text": """<b>⚽️🔥 PREDIKSI BOLA TERAKURAT HARI INI! 🔥⚽️</b>

🔥 Update skor & prediksi live setiap hari
👉 Gabung: <a href='https://shortq.xyz/bolapelangi'>BOLAPELANGI</a>
🎲 Situs Gacor Terbaik, siap jackpot!

🎁 KLAIM FREEBET
🆔 @SitusLinkterGacor_Bot
🆔 @Koloni_4D_bot

⚽️ SITUS BOLA TERPERCAYA
🎯 BOLAPELANGI → <a href='https://shortq.xyz/bolapelangi'>LINK VIP BOLAPELANGI</a>
🎯 BOLAPELANGI2 → <a href='https://shortq.info/bolapelangi2'>LINK VIP BOLAPELANGI 2</a>

🎰 SITUS SLOT GACOR
🔥 KOLONI4D → <a href='https://mez.ink/koloni4d/'> LINK KOLONI4D VIP 1 </a>
🔥 KOLONI4D → <a href='https://heylink.me/LinkAlternatifKoloni4D'> LINK KOLONI4D VIP 2</a>
🔥 SINGASLOT → <a href='https://shortq.org/Singaslot'> LINK VIP SINGASLOT</a>

📊 Mau makin yakin? Cek RTP dulu!
👉 <a href='https://shortq.my/RTP-koloni4d'>RTP TERAKURAT</a>""",
        "image": "https://i.postimg.cc/5yTVzk8Z/3.png"

    },
    {
        "text": """<b>📊 HASIL & STATISTIK TERBARU!</b>

90% prediksi terbukti akurat
Buruan join gratis!
👉 <a href='https://shortq.xyz/bolapelangi'>LINK VIP BOLAPELANGI</a>
Raih kemenangan bersama komunitas!

🎁 KLAIM FREEBET
🆔 @Situslinktergacor_Bot
🆔 @Koloni_4D_bot

⚽️ SITUS BOLA TERPERCAYA
🎯 BOLAPELANGI → <a href='https://shortq.xyz/bolapelangi'>LINK VIP BOLAPELANGI</a>
🎯 BOLAPELANGI2 → <a href='https://shortq.info/bolapelangi2'>LINK VIP BOLAPELANGI 2</a>

🎰 SITUS SLOT GACOR
🔥 KOLONI4D → <a href='https://mez.ink/koloni4d/'> LINK KOLONI4D VIP 1 </a>
🔥 KOLONI4D → <a href='https://heylink.me/LinkAlternatifKoloni4D'> LINK KOLONI4D VIP 2</a>
🔥 SINGASLOT → <a href='https://shortq.org/Singaslot'>LINK VIP SINGASLOT</a>

📊 Mau makin yakin? Cek RTP dulu!
👉 <a href='https://shortq.my/RTP-koloni4d'>RTP TERAKURAT</a>""",
        "image": "https://i.postimg.cc/28LmYrDm/4.png"
    },
    {
        "text": """<b>⚽️🔥 PREDIKSI BOLA TERAKURAT HARI INI! 🔥⚽️</b>

🔥 Update skor & tips jitu setiap hari
👉 Gabung: <a href='https://shortq.info/bolapelangi2'>LINK VIP BOLAPELANGI 2</a>
🎲 Siap jackpot, menang maksimal!

🎁 KLAIM FREEBET
🆔 @Situslinktergacor_Bot
🆔 @Koloni_4D_bot

⚽️ SITUS BOLA TERPERCAYA
🎯 BOLAPELANGI → <a href='https://shortq.xyz/bolapelangi'>LINK VIP BOLAPELANGI</a>
🎯 BOLAPELANGI2 → <a href='https://shortq.info/bolapelangi2'>LINK VIP BOLAPELANGI 2 </a>

🎰 SITUS SLOT GACOR
🔥 KOLONI4D → <a href='https://mez.ink/koloni4d/'> LINK KOLONI4D VIP 1 </a>
🔥 KOLONI4D → <a href='https://heylink.me/LinkAlternatifKoloni4D'> LINK KOLONI4D VIP 2</a>
🔥 SINGASLOT → <a href='https://shortq.org/Singaslot'>LINK VIP SINGASLOT</a>

📊 Mau makin yakin? Cek RTP dulu!
👉 <a href='https://shortq.my/RTP-koloni4d'>RTP TERAKURAT</a>""",
        "image": "https://i.postimg.cc/XqyPRNyz/2.png"
    },
    {
        "text": """<b>📊 HASIL & STATISTIK TERBARU!</b>

90% prediksi terbukti akurat
👉 Gabung: <a href='https://shortq.info/bolapelangi2'>LINK VIP BOLAPELANGI 2</a>
Raih kemenangan bersama komunitas!

🎁 KLAIM FREEBET
🆔 @Situslinktergacor_Bot
🆔 @Koloni_4D_bot

⚽️ SITUS BOLA TERPERCAYA
🎯 BOLAPELANGI → <a href='https://shortq.xyz/bolapelangi'>LINK VIP BOLAPELANGI</a>
🎯 BOLAPELANGI2 → <a href='https://shortq.info/bolapelangi2'>LINK VIP BOLAPELANGI 2</a>

🎰 SITUS SLOT GACOR
🔥 KOLONI4D → <a href='https://mez.ink/koloni4d/'> LINK KOLONI4D VIP 1 </a>
🔥 KOLONI4D → <a href='https://heylink.me/LinkAlternatifKoloni4D'> LINK KOLONI4D VIP 2</a>
🔥 SINGASLOT → <a href='https://shortq.org/Singaslot'> LINK VIP SINGASLOT </a>

📊 Mau makin yakin? Cek RTP dulu!
👉 <a href='https://shortq.my/RTP-koloni4d'> RTP TERAKUTRAT</a>""",
        "image": "https://i.postimg.cc/q7D40RzJ/1.png"
    },
    {
        "text": """<b>🔥🔥 PREDIKSI SLOT GACOR HARI INI! 🔥🔥</b>

Link slot gacor & bocoran jam hoki
👉 Join: <a href='https://mez.ink/koloni4d/'> LINK KOLONI4D VIP 1</a>
👉 Join: <a href='https://heylink.me/LinkAlternatifKoloni4D'> LINK KOLONI4D VIP 2</a>
🎲 Siap jackpot!

🎁 KLAIM FREEBET
🆔 @Situslinktergacor_Bot
🆔 @Koloni_4D_bot

⚽️ SITUS BOLA TERPERCAYA
🎯 BOLAPELANGI → <a href='https://shortq.xyz/bolapelangi'>LINK VIP BOLAPELANGI</a>
🎯 BOLAPELANGI2 → <a href='https://shortq.info/bolapelangi2'>LINK VIP BOLAPELANGI 2</a>

🎰 SITUS SLOT GACOR
🔥 KOLONI4D → <a href='https://mez.ink/koloni4d/'> LINK KOLONI4D VIP 1 </a>
🔥 KOLONI4D → <a href='https://heylink.me/LinkAlternatifKoloni4D'> LINK KOLONI4D VIP 2</a>
🔥 SINGASLOT → <a href='https://shortq.org/Singaslot'>LINK VIP SINGASLOT </a>

📊 Mau makin yakin? Cek RTP dulu!
👉 <a href='https://shortq.my/RTP-koloni4d'>RTP TERAKURAT</a>

🎁 KLAIM FREEBET
🆔 @Situslinktergacor_Bot
🆔 @Koloni_4D_bot

⚽️ SITUS BOLA TERPERCAYA
🎯 BOLAPELANGI → <a href='https://shortq.xyz/bolapelangi'>LINK VIP BOLAPELANGI</a>
🎯 BOLAPELANGI2 → <a href='https://shortq.info/bolapelangi2'>LINK VIP BOLAPELANGI 2 </a>

🎰 SITUS SLOT GACOR
🔥 KOLONI4D → <a href='https://mez.ink/koloni4d/'> LINK KOLONI4D VIP 1 </a>
🔥 KOLONI4D → <a href='https://heylink.me/LinkAlternatifKoloni4D'> LINK KOLONI4D VIP 2</a>
🔥 SINGASLOT → <a href='https://shortq.org/Singaslot'>LINK VIP SINGA SLOT </a> 

📊 Mau makin yakin? Cek RTP dulu!
👉 <a href='https://shortq.my/RTP-koloni4d'>RTP TERAKURAT</a>""",
        "image": "https://i.postimg.cc/4X8M5rkQ/5.png"
    },
    {
        "text": """<b>⚡️ 90% MEMBER SUDAH WD HARI INI!</b>

Buruan join, dapatkan bocoran slot hoki
👉 Join: <a href='https://mez.ink/koloni4d/'> LINK KOLONI4D VIP 1</a>
👉 Join: <a href='https://heylink.me/LinkAlternatifKoloni4D'> LINK KOLONI4D VIP 2</a>
Situs gacor terbaik menunggumu!

🎁 KLAIM FREEBET
🆔 @Situslinktergacor_Bot
🆔 @Koloni_4D_bot

⚽️ SITUS BOLA TERPERCAYA
🎯 BOLAPELANGI → <a href='https://shortq.xyz/bolapelangi'>LINK VIP BOLAPELANGI</a>
🎯 BOLAPELANGI2 → <a href='https://shortq.info/bolapelangi2'>LINK VIP BOLAPELANGI 2</a>

🎰 SITUS SLOT GACOR
🔥 KOLONI4D → <a href='https://mez.ink/koloni4d/'> LINK KOLONI4D VIP 1 </a>
🔥 KOLONI4D → <a href='https://heylink.me/LinkAlternatifKoloni4D'> LINK KOLONI4D VIP 2</a>
🔥 SINGASLOT → <a href='https://shortq.org/Singaslot'>LINK VIP SINGASLOT</a>

📊 Mau makin yakin? Cek RTP dulu!
👉 <a href='https://shortq.my/RTP-koloni4d'>RTP TERAKURAT</a>""",
        "image": "https://i.postimg.cc/tR086WQ0/6.png"
    },
    {
        "text": """<b>🔥🔥 PREDIKSI SLOT GACOR HARI INI! 🔥🔥</b>

Update link & bocoran jam gacor
👉 Join: <a href='https://shortq.org/Singaslot'>LINK VIP SINGASLOT</a> 
🎲 Siap jackpot!

🎁 KLAIM FREEBET
🆔 @Situslinktergacor_Bot
🆔 @Koloni_4D_bot

⚽️ SITUS BOLA TERPERCAYA
🎯 BOLAPELANGI → <a href='https://shortq.xyz/bolapelangi'>LINK VIP BOLAPELANGI</a>
🎯 BOLAPELANGI2 → <a href='https://shortq.info/bolapelangi2'>LINK VIP BOLAPELANGI 2 </a>

🎰 SITUS SLOT GACOR
🔥 KOLONI4D → <a href='https://mez.ink/koloni4d/'> LINK KOLONI4D VIP 1 </a>
🔥 KOLONI4D → <a href='https://heylink.me/LinkAlternatifKoloni4D'> LINK KOLONI4D VIP 2</a>
🔥 SINGASLOT → <a href='https://shortq.org/Singaslot'>LINK VIP SINGASLOT</a>

📊 Mau makin yakin? Cek RTP dulu!
👉 <a href='https://shortq.my/RTP-koloni4d'>RTP TERAKURAT</a>""",
        "image": "https://i.postimg.cc/Nsy5FqYJ/7.png"
    },
    {
        "text": """<b>⚡️ HASIL MENANG SLOT TERBARU!</b>

90% member sudah WD hari ini
👉 <a href='https://shortq.org/Singaslot'>LINK VIP SINGALOT</a>
Gabung sekarang dan menangkan jackpot!

🎁 KLAIM FREEBET
🆔 @Situslinktergacor_Bot
🆔 @Koloni_4D_bot

⚽️ SITUS BOLA TERPERCAYA
🎯 BOLAPELANGI → <a href='https://shortq.xyz/bolapelangi'>LINK VIP BOLAPELANGI</a>
🎯 BOLAPELANGI2 → <a href='https://shortq.info/bolapelangi2'>LINK VIP BOLAPELANGI 2 </a>

🎰 SITUS SLOT GACOR
🔥 KOLONI4D → <a href='https://mez.ink/koloni4d/'> LINK KOLONI4D VIP 1 </a>
🔥 KOLONI4D → <a href='https://heylink.me/LinkAlternatifKoloni4D'> LINK KOLONI4D VIP 2</a>
🔥 SINGASLOT → <a href='https://shortq.org/Singaslot'>LINK VIP SINGASLOT</a>

📊 Mau makin yakin? Cek RTP dulu!
👉 <a href='https://shortq.my/RTP-koloni4d'>RTP TERAKURAT</a>""",
        "image": "https://i.postimg.cc/Xjw6QQgN/8.png"
    },
]

# Fungsi untuk menangani /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("⚽ LINK BOLAPELANGI (Situs Bola)", callback_data='LINK_BOLAPELANGI')],
        [InlineKeyboardButton("🎰 LINK BOLAPELANGI2 (Situs Bola)", callback_data='LINK_BOLAPELANGI2')],
        [InlineKeyboardButton("🎲 LINK KOLONI4D (Situs Slot)", callback_data='LINK_KOLONI4D')],
        [InlineKeyboardButton("🎮 LINK SINGASLOT (Situs Slot)", callback_data='LINK_SINGASLOT')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    message_text = (
        "<b>🎰 Situs Gacor Pilihan Hari Ini!</b>\n\n"
        "Langsung pilih menu di bawah ini untuk klaim bonus dan main di situs paling cuan hari ini! 🚀\n\n"
        "🎁 Freebet Tanpa Ribet • 💸 Bonus Harian • 📊 RTP Tinggi Dijamin"
    )

    # Gunakan kondisi agar tidak error
    if update.message:
        await update.message.reply_text(
            message_text,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
    elif update.callback_query:
        await update.callback_query.edit_message_text(
            message_text,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )


# Fungsi untuk menangani tombol-tombol yang dipilih
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Menentukan tindakan berdasarkan tombol yang dipilih
    if query.data == 'LINK_BOLAPELANGI':
        keyboard = [
            [InlineKeyboardButton("🔗 LINK ALTERNATIF VVIP!!", callback_data='BOLAPELANGI_ALTERNATIF')],
            [InlineKeyboardButton("📱 CHANNEL OFFICIAL", callback_data='BOLAPELANGI_OFFICIAL')],
            [InlineKeyboardButton("⚡ PREDIKSI BOLA 100% AKURAT", callback_data='BOLAPELANGI_PREDIKSI')],
            [InlineKeyboardButton("🎁 CLAIM FREEBET BOLAPELANGI", callback_data='BOLAPELANGI_CLAIM')],
            [InlineKeyboardButton("⬅️ Kembali", callback_data='start')]

        ]
        await query.edit_message_text(
        text=(
        "🎯 <b>MENU UTAMA BOLAPELANGI</b>\n\n"
        "Selamat datang di dunia permainan paling gacor! 🔥\n"
        "Akses semua fitur VVIP hanya dengan satu klik. Pilih menu di bawah ini dan mulai petualanganmu! 💎🎁"
        ),
    reply_markup=InlineKeyboardMarkup(keyboard),
    parse_mode='HTML'
)

    elif query.data == 'start':
        # Panggil ulang menu utama
        await start(update, context)

    elif query.data == 'LINK_BOLAPELANGI2':
        keyboard = [
            [InlineKeyboardButton("🔗 LINK ALTERNATIF VVIP", callback_data='BOLAPELANGI2_ALTERNATIF')],
            [InlineKeyboardButton("📱 CHANNEL OFFICIAL", callback_data='BOLAPELANGI2_OFFICIAL')],
            [InlineKeyboardButton("⚡ PREDIKSI BOLA 100% AKURAT", callback_data='BOLAPELANGI2_PREDIKSI')],
            [InlineKeyboardButton("🎁 CLAIM FREEBET BOLAPELANGI2", callback_data='BOLAPELANGI2_CLAIM')],
            [InlineKeyboardButton("⬅️ Kembali", callback_data='start')]
        ]
        await query.edit_message_text(
        text=(
        "🎯 <b>MENU UTAMA BOLAPELANGI2</b>\n\n"
        "Selamat datang di pusat hiburan paling elite! 💎\n"
        "Nikmati berbagai fitur VVIP, promo spesial, dan akses eksklusif hanya untuk kamu. 🎁\n\n"
        "🔘 Pilih menu di bawah dan rasakan sensasi bermain yang berbeda!"),
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML')

    elif query.data == 'start':
        # Panggil ulang menu utama
        await start(update, context)

    elif query.data == 'LINK_KOLONI4D':
        keyboard = [
            [InlineKeyboardButton("🔗 LINK ALTERNATIF VVIP", callback_data='KOLONI4D_ALTERNATIF')],
            [InlineKeyboardButton("📱 CHANNEL OFFICIAL", callback_data='KOLONI4D_OFFICIAL')],
            [InlineKeyboardButton("⚡ RTP & POLA TERGACOR !! ", callback_data='KOLONI4D_RTP')],
            [InlineKeyboardButton("🎁 CLAIM FREEBET KOLONI4D", callback_data='KOLONI4D_CLAIM')],
            [InlineKeyboardButton("⬅️ Kembali", callback_data='start')]
        ]
        await query.edit_message_text(
        text=(
        "🎯 <b>MENU UTAMA KOLONI4D</b>\n\n"
        "Selamat datang di dunia hiburan paling gacor! 🚀\n"
        "Semua fitur eksklusif, bonus, dan kejutan seru tersedia di sini. 💎\n\n"
        "👇 Pilih menu di bawah dan mulai perjalanan menangmu sekarang juga! 🎁"
        ),
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML')
        
    elif query.data == 'start':
        # Panggil ulang menu utama
        await start(update, context)

    elif query.data == 'LINK_SINGASLOT':
        keyboard = [
            [InlineKeyboardButton("🔗 LINK ALTERNATIF VVIP", callback_data='SINGASLOT_ALTERNATIF')],
            [InlineKeyboardButton("📱 CHANNEL OFFICIAL", callback_data='SINGASLOT_OFFICIAL')],
            [InlineKeyboardButton("⚡ RTP & POLA TERGACOR !! ", callback_data='SINGASLOT_RTP')],
            [InlineKeyboardButton("🎁 CLAIM FREEBET KOLONI4D", callback_data='SINGASLOT_CLAIM')],
            [InlineKeyboardButton("⬅️ Kembali", callback_data='start')]
        ]
        await query.edit_message_text(
        text=(
        "🦁 <b>MENU UTAMA SINGASLOT</b>\n\n"
        "Selamat datang di arena slot paling ganas! 🎰🔥\n"
        "Nikmati akses VVIP ke fitur terbaik, bonus melimpah, dan kejutan setiap hari! 💎\n\n"
        "👇 Pilih menu di bawah untuk mulai berburu kemenangan besar sekarang!"),
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML')

    elif query.data == 'start':
        # Panggil ulang menu utama
        await start(update, context)

# Menambahkan bagian BOLAPELANGI_ALTERNATIF dengan tombol GRUP PUBLIK
async def info_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = update.effective_user.id
    callback_data = query.data

    # Simpan data ke context.user_data
    context.user_data['user_id'] = user_id
    context.user_data['callback_data'] = callback_data

    await query.answer()
    if callback_data == 'BOLAPELANGI_ALTERNATIF':
        keyboard = [
            [InlineKeyboardButton("🔗 LINK ALTERNATIF BOLAPELANGI", url="https://shortq.xyz/bolapelangi")],
            [InlineKeyboardButton("📱 CHANNEL OFFICIAL BOLAPELANGI", url="https://t.me/bola_pelangi")],
            [InlineKeyboardButton("💬 GRUP PUBLIK", url='https://t.me/SITUSLINKGACOR4D')],
            [InlineKeyboardButton("💬 GRUP PUBLIK 2", url='https://t.me/InfoFreebet4D')],
            [InlineKeyboardButton("⬅️ Kembali", callback_data='LINK_BOLAPELANGI')],

        ]
        await query.edit_message_text(
            text=(
                "🌐 <b>LINK ALTERNATIF RESMI BOLAPELANGI</b> 🌐\n\n"
                "🔒 Tidak bisa akses situs utama? Tenang! Kami selalu siap dengan link resmi anti-blokir.\n\n"
                "⚡ <b>Akses super cepat</b>\n"
                "🛡️ <b>Aman & Terpercaya</b>\n"
                "🎰 <b>Dijamin Gacor Setiap Hari</b>\n\n"
                "Pilih link di bawah ini dan langsung nikmati pengalaman bermain tanpa hambatan! 🚀"
                ),
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='HTML')
        
    elif query.data == 'BOLAPELANGI_OFFICIAL':
        keyboard = [
            [InlineKeyboardButton("📱 CHANNEL OFFICIAL BOLAPELANGI", url="https://t.me/bola_pelangi")],
            [InlineKeyboardButton("💬 GRUP PUBLIK", url='https://t.me/SITUSLINKGACOR4D')],
            [InlineKeyboardButton("💬 GRUP PUBLIK 2", url='https://t.me/InfoFreebet4D')],
            [InlineKeyboardButton("⬅️ Kembali", callback_data='LINK_BOLAPELANGI')],
        ]
        await query.edit_message_text(
            text=(
                "📢 <b>CHANNEL RESMI BOLAPELANGI</b> 📢\n\n"
                "Dapatkan update terkini, info penting, dan kejutan spesial setiap hari!\n"
                "Bergabunglah sekarang untuk menikmati keistimewaan berikut:\n\n"
                "🎉 <b>Bonus Eksklusif untuk Member Channel</b>\n"
                "📊 <b>Prediksi Harian Terpercaya dan Akurat</b>\n"
                "🎥 <b>Live Update & Informasi Real-Time</b>\n\n"
                "👇 Tekan tombol di bawah untuk mengakses semua link penting kami:"
                ),
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='HTML')

    elif query.data == 'BOLAPELANGI_PREDIKSI':
        keyboard = [
            [InlineKeyboardButton("🔥 PREDIKSI BOLA TERJITU HARI INI! 🔮", url="https://shortq.info/jadwalprediksi/")],
            [InlineKeyboardButton("📱 CHANNEL OFFICIAL BOLAPELANGI", url="https://t.me/bola_pelangi")],
            [InlineKeyboardButton("💬 GRUP PUBLIK", url='https://t.me/SITUSLINKGACOR4D')],
            [InlineKeyboardButton("💬 GRUP PUBLIK 2", url='https://t.me/InfoFreebet4D')],
            [InlineKeyboardButton("⬅️ Kembali", callback_data='LINK_BOLAPELANGI')],
        ]
        await query.edit_message_text(
            text=(
                "⚽️ <b>PREDIKSI JITU BOLA HARI INI</b> ⚽️\n\n"
                "Bingung pilih tim yang tepat? Tenang, kami siap bantu!\n"
                "Prediksi dari analis <b>BOLAPELANGI</b> berdasarkan data statistik mendalam, performa terkini, dan tren terbaru.\n\n"
                "📊 Akurasi Tinggi & Terpercaya\n"
                "💰 Membantu kamu raih profit lebih konsisten\n"
                "🧠 Cocok untuk semua level pemain, dari pemula hingga pro\n\n"
                "🎯 <b>Gunakan fitur eksklusif & dapatkan info penting lainnya di bawah ini:</b>"),

            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='HTML')

    elif query.data == 'BOLAPELANGI_CLAIM':
        keyboard = [
            [InlineKeyboardButton("🎁 CLAIM FREEBET BOLAPELANGI", callback_data='BOLAPELANGI_VERIFIKASI')],
            [InlineKeyboardButton("📱 CHANNEL OFFICIAL BOLAPELANGI", url="https://t.me/bola_pelangi")],
            [InlineKeyboardButton("💬 GRUP PUBLIK", url='https://t.me/SITUSLINKGACOR4D')],
            [InlineKeyboardButton("💬 GRUP PUBLIK 2", url='https://t.me/InfoFreebet4D')],
            [InlineKeyboardButton("⬅️ Kembali", callback_data='LINK_BOLAPELANGI')],
        ]
        await query.edit_message_text(
            text=(
                "🎉 <b>RAIH FREEBET GRATIS TANPA DEPOSIT!</b> 🎉\n\n"
                "Spesial untuk member setia <b>BOLAPELANGI</b>:\n"
                "Dapatkan bonus freebet harian tanpa perlu modal sepeser pun!\n\n"
                "🔥 Proses Cepat & Praktis\n"
                "🎯 Langsung Main Tanpa Repot\n"
                "💰 Tingkatkan Peluang Menangmu Lebih Maksimal\n\n"
                "👇 Pilih menu di bawah dan mulai petualangan menangmu sekarang juga!"
                ),
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='HTML')

    elif query.data == 'BOLAPELANGI2_ALTERNATIF':
        keyboard = [
            [InlineKeyboardButton("🔗 LINK ALTERNATIF BOLAPELANGI2", url="https://rumahbopel2.com/")],
            [InlineKeyboardButton("📱 CHANNEL OFFICIAL BOLAPELANGI2", url="https://t.me/bolapelangi2ofc")],
            [InlineKeyboardButton("💬 GRUP PUBLIK", url='https://t.me/SITUSLINKGACOR4D')],
            [InlineKeyboardButton("💬 GRUP PUBLIK 2", url='https://t.me/InfoFreebet4D')],
            [InlineKeyboardButton("⬅️ Kembali", callback_data='LINK_BOLAPELANGI2')],
        ]
        await query.edit_message_text(
            text=(
                "🏆 <b>LINK ALTERNATIF RESMI BOLAPELANGI2</b> 🏆\n\n"
                "🚫 Situs utama lemot atau kena blokir? Tenang, kami punya solusinya!\n"
                "🔗 Nikmati akses cepat, aman, dan tanpa hambatan dengan link alternatif resmi kami.\n\n"
                "🔒 <b>Anti-Blokir</b> • ⚡ <b>Kecepatan Super Cepat</b> • 💯 <b>Jaminan Gacor Tiap Hari</b>\n\n"
                "👇 Pilih link terbaikmu di bawah ini dan langsung main tanpa batas!"
                ),
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='HTML')

    elif query.data == 'BOLAPELANGI2_OFFICIAL':
        keyboard = [
            [InlineKeyboardButton("📱 CHANNEL OFFICIAL BOLAPELANGI2", url="https://t.me/bolapelangi2ofc")],
            [InlineKeyboardButton("💬 GRUP PUBLIK", url='https://t.me/SITUSLINKGACOR4D')],
            [InlineKeyboardButton("💬 GRUP PUBLIK 2", url='https://t.me/InfoFreebet4D')],
            [InlineKeyboardButton("⬅️ Kembali", callback_data='LINK_BOLAPELANGI2')],
        ]
        await query.edit_message_text(
            text=(
                "📣 <b>CHANNEL RESMI BOLAPELANGI2</b> 📣\n\n"
                "Dapatkan info terpanas dan kejutan spesial setiap hari langsung di channel kami!\n"
                "Gabung sekarang dan nikmati akses eksklusif ke:\n\n"
                "🎁 <b>Bonus Eksklusif untuk Member</b>\n"
                "📈 <b>Prediksi Terakurat & Terupdate</b>\n"
                "🎬 <b>Live Update & Berita Terbaru</b>\n\n"
                "👇 Tekan tombol di bawah untuk bergabung dan jangan sampai ketinggalan!"
            ),
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='HTML')

    elif query.data == 'BOLAPELANGI2_PREDIKSI':
        keyboard = [
            [InlineKeyboardButton("🔥 PREDIKSI BOLA TERJITU HARI INI! 🔮", url="https://shortq.info/jadwalprediksi/")],
            [InlineKeyboardButton("📱 CHANNEL OFFICIAL BOLAPELANGI2", url="https://t.me/bolapelangi2ofc")],
            [InlineKeyboardButton("💬 GRUP PUBLIK", url='https://t.me/SITUSLINKGACOR4D')],
            [InlineKeyboardButton("💬 GRUP PUBLIK 2", url='https://t.me/InfoFreebet4D')],
            [InlineKeyboardButton("⬅️ Kembali", callback_data='LINK_BOLAPELANGI2')],
        ]
        await query.edit_message_text(
            text=(
                "📊 <b>PREDIKSI JITU BOLA HARI INI</b> 📊\n\n"
                "Masih bingung pilih tim yang menang? Tenang, kami siap bantu!\n"
                "Prediksi dari tim analis <b>BOLAPELANGI</b> dibuat dengan data statistik terkini, performa tim, dan tren terbaru yang sudah terbukti akurat.\n\n"
                "📈 Akurasi Tinggi & Terpercaya\n"
                "💸 Bantu kamu raih cuan lebih konsisten\n"
                "🧠 Cocok untuk semua level pemain, pemula hingga pro\n\n"
                "🎯 <b>Jangan lewatkan fitur spesial dan info penting lainnya. Yuk, cek di bawah ini dan maksimalkan peluangmu!</b>"),
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='HTML')

    elif query.data == 'BOLAPELANGI2_CLAIM':
        keyboard = [
            [InlineKeyboardButton("🎁 CLAIM FREEBET BOLAPELANGI2", callback_data='BOLAPELANGI2_VERIFIKASI')],
            [InlineKeyboardButton("📱 CHANNEL OFFICIAL BOLAPELANGI2", url="https://t.me/bolapelangi2ofc")],
            [InlineKeyboardButton("💬 GRUP PUBLIK", url='https://t.me/SITUSLINKGACOR4D')],
            [InlineKeyboardButton("💬 GRUP PUBLIK 2", url='https://t.me/InfoFreebet4D')],
            [InlineKeyboardButton("⬅️ Kembali", callback_data='LINK_BOLAPELANGI2')],
        ]
        await query.edit_message_text(
            text=(
                "🎉 <b>KLAIM FREEBET GRATIS TANPA DEPOSIT!</b> 🎉\n\n"
                "Hanya untuk member setia <b>BOLAPELANGI2</b>:\n"
                "Nikmati bonus freebet harian tanpa harus mengeluarkan modal sepeser pun!\n\n"
                "🔥 Proses Cepat & Tanpa Ribet\n"
                "🎯 Main Langsung dan Menangkan Hadiah\n"
                "💰 Tingkatkan Peluang Cuanmu Setiap Hari\n\n"
                "👇 Pilih menu di bawah dan segera manfaatkan kesempatan emas ini!"),
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='HTML')
       
    # Menambahkan bagian KOLONI4D_ALTERNATIF dengan tombol GRUP PUBLIK
    elif query.data == 'KOLONI4D_ALTERNATIF':
        keyboard = [
            [InlineKeyboardButton("🔗 LINK KOLONI4D VIP 1",url="https://mez.ink/koloni4d/")],
            [InlineKeyboardButton("🔗 LINK KOLONI4D VIP 2",url="https://heylink.me/LinkAlternatifKoloni4D/")],
            [InlineKeyboardButton("📱 CHANNEL OFFICIAL KOLONI4D", url="https://t.me/koloni4d_official")],
            [InlineKeyboardButton("💬 GRUP PUBLIK", url='https://t.me/SITUSLINKGACOR4D')],  
            [InlineKeyboardButton("💬 GRUP PUBLIK 2", url='https://t.me/InfoFreebet4D')],
            [InlineKeyboardButton("⬅️ Kembali", callback_data='LINK_KOLONI4D')],   
        ]
        await query.edit_message_text(
            text=(
                "🏆 <b>LINK ALTERNATIF RESMI KOLONI4D</b> 🏆\n\n"
                "🚫 Situs utama lemot atau kena blokir? Tenang, kami punya solusinya!\n"
                "🔗 Nikmati akses cepat, aman, dan tanpa hambatan lewat link alternatif resmi kami.\n\n"
                "🔒 <b>Anti-Blokir</b> • ⚡ <b>Kecepatan Super Cepat</b> • 💯 <b>Jaminan Situs Gacor</b>\n\n"
                "👇 Pilih link favoritmu di bawah dan langsung main tanpa batas!"
                ),
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='HTML')

    # Menambahkan bagian KOLONI4D_OFFICIAL dengan tombol GRUP PUBLIK
    elif query.data == 'KOLONI4D_OFFICIAL':
        keyboard = [
            [InlineKeyboardButton("📱 CHANNEL OFFICIAL", url="https://t.me/koloni4d_official")],
            [InlineKeyboardButton("💬 GRUP PUBLIK", url='https://t.me/SITUSLINKGACOR4D')],  
            [InlineKeyboardButton("💬 GRUP PUBLIK 2", url='https://t.me/InfoFreebet4D')],
            [InlineKeyboardButton("⬅️ Kembali", callback_data='LINK_KOLONI4D')],  
        ]
        await query.edit_message_text(
            text=(
                "🎰 <b>CHANNEL RESMI SLOT KOLONI4D</b> 🎰\n\n"
                "Nikmati update terkini seputar game slot terbaik, promo jackpot eksklusif, dan event-event seru khusus para pecinta slot!\n\n"
                "🎁 Bonus Eksklusif untuk Member Setia\n📊 Tips & Trik Ampuh Menang Slot Tiap Hari\n🎥 Live Spin Seru & Info Jackpot Real Time\n\n"
                "👇 Klik tombol di bawah untuk akses link penting dan jangan sampai ketinggalan keseruan terbaru dari dunia slot!"
            ),
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='HTML'
            )

    elif query.data == 'KOLONI4D_RTP':
        keyboard = [
            [InlineKeyboardButton("📱 CHANNEL OFFICIAL", url="https://rtpkln4d-v1.pagesco.de/")],
            [InlineKeyboardButton("📱 CHANNEL OFFICIAL", url="https://t.me/koloni4d_official")],
            [InlineKeyboardButton("💬 GRUP PUBLIK", url='https://t.me/SITUSLINKGACOR4D')],  
            [InlineKeyboardButton("💬 GRUP PUBLIK 2", url='https://t.me/InfoFreebet4D')],
            [InlineKeyboardButton("⬅️ Kembali", callback_data='LINK_KOLONI4D')],  
        ]
        await query.edit_message_text(
            text=(
                "🔥 <b>PREDIKSI RTP & POLA JUARA HARI INI</b> 🔥\n\n"
                "Ingin kemenangan besar? Andalkan prediksi RTP & pola terbaru dari tim ahli KOLONI4D yang sudah teruji akurasi dan efektivitasnya!\n\n"
                "📊 Data real-time terkini • 📈 Strategi juara • 💸 Maksimalkan peluang kemenanganmu hari ini!\n\n"
                "🚀 Jangan tunggu lagi! Klik link di bawah dan raih hadiah spektakuler sekarang juga!"
            ),
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='HTML'
        )
    elif query.data == 'KOLONI4D_CLAIM':
        keyboard = [
            [InlineKeyboardButton("🎁 CLAIM FREEBET KOLONI4D",callback_data='KOLONI4D_VERIFIKASI')],
            [InlineKeyboardButton("📱 CHANNEL OFFICIAL KOLONI4D", url="https://t.me/koloni4d_official")],
            [InlineKeyboardButton("💬 GRUP PUBLIK", url='https://t.me/SITUSLINKGACOR4D')],  
            [InlineKeyboardButton("💬 GRUP PUBLIK 2", url='https://t.me/InfoFreebet4D')],
            [InlineKeyboardButton("⬅️ Kembali", callback_data='LINK_KOLONI4D')],  
        ]
        await query.edit_message_text(
            text=(
                "🎉 <b>FREEBET GRATIS SPESIAL UNTUK MEMBER BARU KOLONI4D!</b> 🎉\n\n"
                "Sambut member baru dengan bonus freebet tanpa deposit, bisa klaim setiap hari tanpa ribet!\n\n"
                "✅ Klaim cepat & mudah\n✅ Langsung main tanpa tunggu\n✅ Peluang menang lebih besar!\n\n"
                "🔥 Jangan sampai ketinggalan! Pilih menu seru lainnya di bawah dan raih kesempatanmu sekarang juga:"
            ),
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='HTML'
        )

    # Menangani sub-tombol untuk LINK SINGASLOT
    if query.data == 'SINGASLOT_ALTERNATIF':
        keyboard = [
            [InlineKeyboardButton("🔗 LINK ALTERNATIF SINGASLOT", url="https://singa2025.net/")],
            [InlineKeyboardButton("📱 CHANNEL OFFICIAL SINGA SLOT", url="https://t.me/Singslot")],
            [InlineKeyboardButton("💬 GRUP PUBLIK", url='https://t.me/SITUSLINKGACOR4D')],  
            [InlineKeyboardButton("💬 GRUP PUBLIK 2", url='https://t.me/InfoFreebet4D')],
            [InlineKeyboardButton("⬅️ Kembali", callback_data='LINK_SINGASLOT')],  
        ]
        await query.edit_message_text(
            text=(
                "🏆 <b>LINK ALTERNATIF RESMI SINGASLOT</b> 🏆\n\n"
                "🚫 Situs utama lemot atau diblokir? Tenang, kami punya solusinya!\n"
                "🔗 Nikmati akses super cepat, aman, dan tanpa gangguan melalui link alternatif resmi kami!\n\n"
                "🔒 <b>Anti-Blokir</b> • ⚡ <b>Kecepatan Maksimal</b> • 💯 <b>Terpercaya & Gacor!</b>\n\n"
                "👇 Pilih link favoritmu di bawah dan langsung gaskeun kemenanganmu hari ini!"
            ),
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='HTML'
        )

    elif query.data == 'SINGASLOT_OFFICIAL':
        keyboard = [
            [InlineKeyboardButton("📱 CHANNEL OFFICIAL SINGA SLOT", url="https://t.me/Infosingaslot")],
            [InlineKeyboardButton("💬 GRUP PUBLIK", url='https://t.me/SITUSLINKGACOR4D')],  
            [InlineKeyboardButton("💬 GRUP PUBLIK 2", url='https://t.me/InfoFreebet4D')],
            [InlineKeyboardButton("⬅️ Kembali", callback_data='LINK_SINGASLOT')],  
        ]
        await query.edit_message_text(
            text=(
                "🎰 <b>CHANNEL RESMI SLOT SINGASLOT</b> 🎰\n\n"
                "Jangan lewatkan update eksklusif seputar game slot terbaik, promo jackpot besar, dan event seru hanya di channel resmi kami!\n\n"
                "🎁 Bonus Eksklusif Khusus Member\n📊 Tips & Trik Ampuh Menang Slot Setiap Hari\n🎥 Live Spin Seru & Info Jackpot Real Time\n\n"
                "👇 Klik tombol di bawah untuk akses link penting dan raih keseruan serta kemenangan terbaru!"
            ),
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='HTML'
        )

    elif query.data == 'SINGASLOT_RTP':
        keyboard = [
            [InlineKeyboardButton("🔗 LINK ALTERNATIF SINGA SLOT", url="https://rtpsngslt-v1.pagesco.de/")],
            [InlineKeyboardButton("📱 CHANNEL OFFICIAL KOLONI4D", url="https://t.me/Singslot")],
            [InlineKeyboardButton("💬 GRUP PUBLIK", url='https://t.me/SITUSLINKGACOR4D')],  
            [InlineKeyboardButton("💬 GRUP PUBLIK 2", url='https://t.me/InfoFreebet4D')],
            [InlineKeyboardButton("⬅️ Kembali", callback_data='LINK_SINGASLOT')],  
        ]
        await query.edit_message_text(
            text=(
                "🔥 <b>PREDIKSI RTP & POLA JUARA HARI INI</b> 🔥\n\n"
                "Mau menang besar? Gunakan prediksi RTP & pola terbaru dari tim ahli KOLONI4D yang sudah terbukti akurat!\n\n"
                "📊 Data real-time • 📈 Strategi jitu • 💸 Raih kemenangan maksimal!\n\n"
                "🚀 Klik link di bawah dan mulai bawa pulang hadiah besar hari ini!"),
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='HTML')

    elif query.data == 'SINGASLOT_CLAIM':
        keyboard = [
            [InlineKeyboardButton("🎁 CLAIM FREEBET SINGASLOT", callback_data='SINGASLOT_VERIFIKASI')],
            [InlineKeyboardButton("📱 CHANNEL OFFICIAL SINGA SLOT", url="https://t.me/Singslot")],
            [InlineKeyboardButton("💬 GRUP PUBLIK", url='https://t.me/SITUSLINKGACOR4D')],  
            [InlineKeyboardButton("💬 GRUP PUBLIK 2", url='https://t.me/InfoFreebet4D')],
            [InlineKeyboardButton("⬅️ Kembali", callback_data='LINK_SINGASLOT')],  
        ]
        await query.edit_message_text(
            text=(
                "🎉 <b>GRATIS KLAIM FREEBET UNTUK MEMBER BARU KOLONI4D!</b> 🎉\n\n"
                "Selamat datang! Dapatkan bonus freebet tanpa deposit yang siap dipakai setiap hari khusus buat kamu!\n\n"
                "✅ Klaim mudah tanpa ribet\n✅ Langsung main tanpa harus menunggu\n✅ Peluang menang besar di ujung jari kamu!\n\n"
                "🔥 Jangan sampai ketinggalan! Pilih menu seru lainnya di bawah dan raih kemenanganmu sekarang juga!"
            ),
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='HTML'
        )

async def verify_membership(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    callback_data = query.data  # Ambil data dari callback

    verify_data = verification_map.get(callback_data)
    if not verify_data:
        await query.answer("⚠️ Data verifikasi tidak ditemukan.", show_alert=True)
        return

    try:
        # Cek status channel
        channel_status = await context.bot.get_chat_member(verify_data['channel'], user_id)

        # Cek status grup (semua grup harus lolos)
        group_joined = True
        for group in verify_data['groups']:
            group_status = await context.bot.get_chat_member(group, user_id)
            logging.info(f"Group status for {group}: {group_status.status}")  # Logging tiap grup
            if group_status.status not in ['member', 'administrator', 'creator']:
                logging.warning(f"User {user_id} is not a member of group {group}!")
                group_joined = False
                break

        logging.info(f"Channel status: {channel_status.status}")  # Logging status channel

        if channel_status.status not in ['member', 'administrator', 'creator']:
            logging.warning(f"User {user_id} is not a member of the channel!")
        
        # Verifikasi sukses
        if channel_status.status in ['member', 'administrator', 'creator'] and group_joined:
            context.user_data['last_action'] = verify_data['last_action']
            text = verify_data['success_text']
            lanjut_button = InlineKeyboardMarkup([[
                InlineKeyboardButton("🔓 Klik untuk Lanjut", callback_data="thank_you_after_verify")
            ]])
            await query.edit_message_text(text=text, parse_mode='HTML', reply_markup=lanjut_button)
        else:
            # Jika gagal
            await query.answer("❗ Anda belum bergabung di grup dan channel!", show_alert=True)
            await send_welcome_message(query, context) # type: ignore

    except Exception as e:
        logging.error(f"Error occurred while verifying membership for user {user_id}: {e}")
        await query.answer("⚠️ Terjadi kesalahan saat verifikasi.", show_alert=True)
        await send_welcome_message(query, context) # type: ignore


async def thank_you_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    last_action = context.user_data.get('last_action', '')
    print(f"Last action: {last_action}")

    if last_action == 'VERIFIKASI_BOLAPELANGI':
        group_link = "https://bopel.vip/wa"
        text = (
            "🎁 <b>KLAIM FREEBET HARI INI – EKSKLUSIF UNTUK MEMBER BARU!</b> 🎁\n\n"
            "✅ Selamat! Anda sudah bergabung di grup & channel resmi kami.\n"
            "🎉 Sekarang saatnya klaim freebet tanpa deposit, cukup daftar melalui link resmi berikut:\n\n"
            "🌐 <b>LINK VIP BOLAPELANGI</b>\n"
            "<a href=\"https://shortq.xyz/bolapelangi/\">LINK VIP BOLAPELANGI</a>\n\n"
            "⚠️ <b>PERHATIAN PENTING!</b>\nPastikan data yang Anda isi <u>benar dan valid</u>, terutama nomor rekening atau e-wallet.\n"
            "❌ Kesalahan pengisian data, seperti nomor rekening yang salah, tidak dapat kami proses atau perbaiki.\n"
            "🔒 Semua data yang Anda berikan sepenuhnya menjadi tanggung jawab pribadi Anda.\n\n"
            "⛔ <b>Freebet hanya berlaku untuk akun baru yang belum pernah terdaftar sebelumnya. Jangan sampai terlewat!</b>"
        )

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📥 KONFIRMASI VIA WHATSAPP", url=group_link)],
            [InlineKeyboardButton("⬅️ Kembali", callback_data='LINK_BOLAPELANGI')]
        ])

        await query.edit_message_text(
            text=text,
            reply_markup=keyboard,
            parse_mode='HTML'
        )

    elif last_action == 'VERIFIKASI_BOLAPELANGI2':
        group_link = "https://rumahbopel2.com/"
        text = (
            "🎁 <b>KLAIM FREEBET HARI INI – EKSKLUSIF UNTUK MEMBER BARU!</b> 🎁\n\n"
            "✅ Selamat! Anda telah resmi bergabung di grup & channel kami.\n"
            "🎉 Saatnya klaim freebet tanpa deposit, cukup daftar melalui link resmi berikut ini:\n\n"
            "🌐 <b>LINK VIP BOLAPELANGI2</b>\n"
            "<a href=\"https://rumahbopel2.com/\">LINK VIP BOLAPELANGI2</a>\n\n"
            "⚠️ <b>PENTING!</b>\nPastikan data yang Anda isi <u>tepat dan valid</u>, terutama nomor rekening atau e-wallet.\n"
            "❌ Kesalahan pengisian data (misal nomor rekening salah) tidak dapat kami proses atau perbaiki.\n"
            "🔒 Semua data yang Anda berikan menjadi tanggung jawab Anda sepenuhnya.\n\n"
            "⛔ <b>Freebet hanya berlaku bagi akun baru yang belum pernah terdaftar sebelumnya. Jangan sampai terlewat!</b>"
        )
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📥 KONFIRMASI VIA WHATSAPP", url=group_link)],
            [InlineKeyboardButton("⬅️ Kembali", callback_data='LINK_BOLAPELANGI2')]
        ])

        await query.edit_message_text(
            text=text,
            reply_markup=keyboard,
            parse_mode='HTML'
        )

    elif last_action == 'VERIFIKASI_KOLONI4D':
        group_link = "https://shortq.my/wa-koloni4d"
        text = (
            "🎁 <b>KLAIM FREEBET HARI INI – EKSKLUSIF UNTUK MEMBER BARU KOLONI4D!</b> 🎁\n\n"
            "✅ Selamat! Anda telah resmi bergabung di grup & channel resmi kami.\n"
            "🎉 Saatnya klaim freebet tanpa deposit dengan mendaftar melalui link resmi berikut:\n\n"
            "🌐 <b>LINK VIP BOLAPELANGI</b>\n"
            "<a href=\"https://shortq.my/wa-koloni4d/\">LINK VIP BOLAPELANGI2</a>\n\n"
            "⚠️ <b>PENTING!</b>\nPastikan data yang Anda masukkan <u>akurasi dan validitasnya terjamin</u>, terutama nomor rekening atau e-wallet.\n"
            "❌ Kesalahan input data (seperti nomor rekening yang salah) tidak bisa kami proses atau perbaiki.\n"
            "🔒 Semua data yang Anda berikan menjadi tanggung jawab pribadi Anda.\n\n"
            "⛔ <b>Freebet hanya berlaku bagi akun baru yang belum pernah terdaftar sebelumnya. Jangan sampai terlewatkan!</b>"
        )
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📥 KONFIRMASI VIA WHATSAPP", url=group_link)],
            [InlineKeyboardButton("⬅️ Kembali", callback_data='LINK_KOLONI4D')]
        ])

        await query.edit_message_text(
            text=text,
            reply_markup=keyboard,
            parse_mode='HTML'
        )

    elif last_action == 'VERIFIKASI_SINGASLOT':
        group_link = "https://singa2025.store/"
        text = (
            "🎁 <b>KLAIM FREEBET HARI INI – KHUSUS MEMBER BARU SINGASLOT!</b> 🎁\n\n"
            "✅ Selamat! Anda sudah resmi bergabung di grup & channel resmi kami.\n"
            "🎉 Saatnya klaim freebet tanpa deposit dengan mendaftar melalui link resmi berikut:\n\n"
            "🌐 <b>LINK VIP BOLAPELANGI</b>\n"
            "<a href=\"https://singa2025.store/\">LINK VIP BOLAPELANGI2</a>\n\n"
            "⚠️ <b>PERHATIAN!</b>\nPastikan data yang Anda isi <u>akurat dan valid</u>, terutama nomor rekening atau e-wallet.\n"
            "❌ Kesalahan input data (misal nomor rekening salah) tidak dapat kami proses atau perbaiki.\n"
            "🔒 Data yang Anda berikan sepenuhnya menjadi tanggung jawab pribadi.\n\n"
            "⛔ <b>Freebet hanya berlaku bagi akun baru yang belum pernah terdaftar sebelumnya. Jangan sampai terlewatkan!</b>"
        )
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📥 KONFIRMASI VIA WHATSAPP", url=group_link)],
            [InlineKeyboardButton("⬅️ Kembali", callback_data='LINK_SINGASLOT')]
        ])

        await query.edit_message_text(
            text=text,
            reply_markup=keyboard,
            parse_mode='HTML'
        )

async def auto_send_messages(app: Application):
    index = 0
    duration = 24 * 60 * 60  # 24 jam dalam detik
    start_time = asyncio.get_running_loop().time()

    while True:
        current_time = asyncio.get_running_loop().time()
        if current_time - start_time > duration:
            logging.info("⏱️ 24 jam selesai. Stop kirim otomatis.")
            break

        try:
            if not messages:
                logging.warning("🚫 List messages kosong.")
                await asyncio.sleep(60)
                continue

            message_data = messages[index]
            image = message_data.get("image")
            text = message_data.get("text", "")

            if not image:
                logging.warning(f"⚠️ Gambar kosong di index {index}. Lewati.")
                index = (index + 1) % len(messages)
                await asyncio.sleep(10)
                continue

            await app.bot.send_photo(
                chat_id=TARGET_CHAT_ID,
                photo=image,
                caption=text,
                parse_mode='HTML'
            )

            logging.info(f"✅ Pesan ke-{index + 1} terkirim.")
            index = (index + 1) % len(messages)
            await asyncio.sleep(3600)  # 2 jam

        except Exception as e:
            logging.error(f"❌ Gagal kirim pesan otomatis (index {index}): {e}")
            await asyncio.sleep(30)

async def on_startup(app: Application):
    global auto_task
    if auto_task is None or auto_task.done():
        auto_task = asyncio.create_task(auto_send_messages(app))
        logging.info("🚀 Auto-send dimulai saat startup.")

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"OK")
        else:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Bot is alive!")

    def do_HEAD(self):
        # Kirim response header yang sama seperti do_GET, tanpa body
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
        else:
            self.send_response(200)
            self.end_headers()


def start_ping_server():
    import os
    port = int(os.environ.get('PORT', 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()

# Jalankan server HTTP di thread terpisah
threading.Thread(target=start_ping_server, daemon=True).start()

def log_activity(user_id, username, action):
    try:
        with open("userlist.txt", "a", encoding="utf-8") as f:
            f.write(f"{datetime.now()} | {user_id} | {username} | {action}\n")
    except Exception as e:
        logging.error(f"Failed to write log: {e}")

def main():
    application = Application.builder().token(API_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(verify_membership, pattern=r"^(BOLAPELANGI|BOLAPELANGI2|KOLONI4D|SINGASLOT)_VERIFIKASI$"))
    application.add_handler(
    CallbackQueryHandler(verify_membership, pattern=r"^(BOLAPELANGI|BOLAPELANGI2|KOLONI4D|SINGASLOT)_VERIFIKASI_CLAIM$"))
    application.add_handler(CallbackQueryHandler(thank_you_message, pattern="^thank_you_after_verify$"))

    application.add_handler(CallbackQueryHandler(
        info_handler,
        pattern=r'^(BOLAPELANGI(_ALTERNATIF|_OFFICIAL|_PREDIKSI|_CLAIM)?|BOLAPELANGI2(_ALTERNATIF|_OFFICIAL|_PREDIKSI|_CLAIM)?|KOLONI4D(_ALTERNATIF|_OFFICIAL|_RTP|_CLAIM)?|SINGASLOT(_ALTERNATIF|_OFFICIAL|_RTP|_CLAIM)?)$'
    ))

    application.add_handler(CallbackQueryHandler(
        button_handler,
        pattern=r"^(?!BOLAPELANGI|BOLAPELANGI2|KOLONI4D|SINGASLOT|verify_|thank_you_after_verify).*"
    ))

    application.post_init = on_startup
    application.run_polling()

if __name__ == "__main__":
    main()
