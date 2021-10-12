from modules import Response as R
from telegram.ext import*
import os

Api_key = "1628016853:AAEyFvb-PmsbUEp4kcAveWtPiFjn_I6wvKE"

def start_command(update, context):
    name = update.message.from_user.first_name
    update.message.reply_text("Hey "+str(name)+"! I am here to help you in creating animation. Please enter your scripts here.")

def help_command(update, context):
    update.message.reply_text("Please refer to the user manual or contact the Administrator!")

def handle_message(update, context):
    name = update.message.from_user.first_name
    if name in ["Deepak Kumar","Harish"]:
        text = str(update.message.text).lower()
        print("\nReceived Script: " + text + "\n")
        status = R.develope(update.message.chat.id,text)
        if status:
            sentStatus = R.send_file(update.message.chat.id)
            print(["Video sent Sucessfully!" if sentStatus else "Unable to upload Video files."][0])
        else:
            update.message.reply_text(str("Something unexpected happen! Please try again later."))
    else:
        update.message.reply_text("This project is under developement. You don't have privilege to access it now.")

def error(update, context):
    print(f"Update {update} caused error {context.error}")


os.system("cls")
print("Anime Maker is online now.\n")
updater = Updater(Api_key, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start",start_command))
dispatcher.add_handler(CommandHandler("help",help_command))
dispatcher.add_handler(MessageHandler(Filters.text, handle_message))
dispatcher.add_error_handler(error)
updater.start_polling()
updater.idle()
