from typing import Final
from telegram import Update
from telegram.ext import Application, Updater, CommandHandler, MessageHandler,filters
from datetime import datetime
import re
from decouple import config

TOKEN = config('TELEGRAM_API_KEY')
BOT_USERNAME: Final = '@haircutScheduleBot'
agenda = {}

def saudacao_por_horario():
    agora = datetime.now().time()

    if agora.hour >= 0 and agora.hour <= 12:
        return "Bom dia"
    elif agora.hour > 12 and agora.hour <= 17:
        return "Boa tarde"
    else:
        return "Boa noite"

def verificar_agendamento(horario, cliente, servico):
    if horario in agenda:
        return False
    else:
        agenda[horario] = {'cliente': cliente, 'servico': servico}
        return True

def mostrar_agenda():
    print("\nAgenda:")
    for horario, info in agenda.items():
        print(f"{horario}: {info['cliente']} - {info['servico']}")

        
        
def formatar_horario(update, context):
    message_text = update.message.text.lower()

    if message_text.isdigit() and 9 <= int(message_text) <= 17:
        horario = message_text + ':00'
        return horario
    else:
        return None
        

async def handle_message(update, context):
    message_text = update.message.text.lower()

    if message_text == "agendar":
        context.user_data['stage'] = 'nome'
        await update.message.reply_text('Qual é o seu nome?')
    elif context.user_data.get('stage') == 'nome':
        context.user_data['nome'] = message_text
        context.user_data['stage'] = 'servico'
        await update.message.reply_text('Escolha o serviço:\n1. Corte de cabelo\n2. Barba\n3. Corte e Barba')
    elif context.user_data.get('stage') == 'servico':
        if message_text not in ['1', '2', '3']:
            await update.message.reply_text('Opção inválida. Por favor, escolha uma opção válida.')
            return

        context.user_data['servico'] = message_text
        context.user_data['stage'] = 'horario'
        
        await update.message.reply_text('Digite o horário entre as 09:00 até as 17:00')
    elif context.user_data.get('stage') == 'horario':
        horario = formatar_horario(update, context)
        if horario == None:
            await update.message.reply_text('Formato de horário inválido. O horário de funcionamento é entre as 09:00 até as 17:00')
            return

        # Verifique se o horário já está agendado
        cliente = context.user_data['nome']
        servico = context.user_data['servico']
        
        servicos = {
            '1': 'Corte de cabelo',
            '2': 'Barba',
            '3': 'Corte e Barba'
        }
        
        if verificar_agendamento(horario, cliente, servico):
            servico_nome = servicos.get(servico)
            await update.message.reply_text(f'Agendado: {cliente} - {servico_nome} às {horario}')
        else:
            await update.message.reply_text(f'O horário {horario} já está ocupado. Por favor, escolha outro horário.')
            return
        # Horário válido, agende o serviço
        context.user_data.clear()
    else:

        saudacao = saudacao_por_horario()
        await update.message.reply_text(f'{saudacao}, tudo bom?\n\nCaso queira agendar um serviço, digite "agendar".')


if __name__ == '__main__':

    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    # Mensagens
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    print('Polling...')
    app.run_polling(poll_interval=3)