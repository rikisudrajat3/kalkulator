import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext

# Muat variabel dari file .env
load_dotenv()

# Ambil token bot dari .env
TOKEN = os.getenv("BOT_TOKEN")

# Variabel untuk menandakan apakah bot dalam mode kalkulator atau tidak
is_calculator_active = False

# Fungsi untuk perintah /start
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Halo! Gunakan /kalkulatorkonan untuk mengaktifkan kalkulator.")

# Fungsi untuk perintah /hitung
async def hitung(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Silakan masukkan perhitungan Anda. Akhiri dengan '='.")

# Fungsi untuk menghitung ekspresi matematika
async def calculate(update: Update, context: CallbackContext) -> None:
    global is_calculator_active

    if is_calculator_active:
        text = update.message.text.strip()

        # Memeriksa apakah input diakhiri dengan '='
        if text.endswith("="):
            expression = text[:-1].strip()  # Hapus '=' dari input
            try:
                result = eval(expression)  # Evaluasi ekspresi matematika
                await update.message.reply_text(f"Hasil: {result}")
            except Exception:
                await update.message.reply_text("Maaf, terjadi kesalahan dalam perhitungan.")
        else:
            await update.message.reply_text("Tambahkan '=' di akhir untuk mendapatkan hasil.")

# Fungsi untuk mengaktifkan kalkulator
async def kalkulator_konan(update: Update, context: CallbackContext) -> None:
    global is_calculator_active
    is_calculator_active = True
    await update.message.reply_text("Kalkulator telah diaktifkan. Masukkan ekspresi matematika, akhiri dengan '='.")

# Fungsi untuk menghentikan kalkulator
async def stop_kalkulator(update: Update, context: CallbackContext) -> None:
    global is_calculator_active
    is_calculator_active = False
    await update.message.reply_text("Kalkulator telah dihentikan. Bot tidak akan lagi menghitung ekspresi.")

# Fungsi untuk menghentikan bot
async def stop(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Bot akan dihentikan sekarang.")
    await context.application.stop()  # Menghentikan bot

# Fungsi utama untuk menjalankan bot
def main():
    app = Application.builder().token(TOKEN).build()

    # Menambahkan handler untuk perintah /start, /hitung, /kalkulatorkonan, /stopkalkulator, dan /stop
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("hitung", hitung))
    app.add_handler(CommandHandler("kalkulatorkonan", kalkulator_konan))  # Menambahkan perintah /kalkulatorkonan
    app.add_handler(CommandHandler("stopkalkulator", stop_kalkulator))  # Menambahkan perintah /stopkalkulator
    app.add_handler(CommandHandler("stop", stop))  # Menambahkan perintah /stop
    
    # Menambahkan handler untuk pesan biasa (tanpa Filters)
    app.add_handler(MessageHandler(None, calculate))

    app.run_polling()

if __name__ == '__main__':
    main()
