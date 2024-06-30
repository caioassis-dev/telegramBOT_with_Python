from typing import Final
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from datetime import datetime
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
    for agendamento in list(agenda.keys()):
        if agenda[agendamento]['cliente'] == cliente:
            del agenda[agendamento]

    if horario in agenda:
        return False
    else:
        agenda[horario] = {'cliente': cliente, 'servico': servico}
        return True

def formatar_horario(message_text):
    if message_text.isdigit() and 9 <= int(message_text) <= 17:
        horario = message_text + ':00'
        return horario
    elif ':' in message_text:
        partes = message_text.split(':')
        if len(partes) == 2 and partes[0].isdigit() and partes[1].isdigit():
            hora, minutos = int(partes[0]), int(partes[1])
            if 9 <= hora <= 17 and 0 <= minutos < 60:
                horario = f"{hora:02d}:{minutos:02d}"
                return horario
    return None

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text.lower()
    
    
    servicos = {
        '1': 'Corte de cabelo',
        '2': 'Barba',
        '3': 'Corte e Barba'
    }
    

    if message_text == "agendar":
        context.user_data['stage'] = 'nome'
        await update.message.reply_text('Qual é o seu nome?')
    elif message_text == "obrigado":
        await update.message.reply_text('De nada, deseja mais alguma ajuda?')
        context.user_data['stage'] = 'finalizar'
    elif context.user_data.get('stage') == 'nome':
        context.user_data['nome'] = message_text
        context.user_data['stage'] = 'servico'
        await update.message.reply_text('Escolha o número do serviço desejado:\n1. Corte de cabelo\n2. Barba\n3. Corte e Barba')
    elif context.user_data.get('stage') == 'servico':
        if message_text not in ['1', '2', '3']:
            await update.message.reply_text('Opção inválida. Por favor, escolha uma opção válida.')
            return

        context.user_data['servico'] = message_text
        context.user_data['stage'] = 'horario'
        await update.message.reply_text('Digite o horário entre as 09:00 até as 17:00')
    elif context.user_data.get('stage') == 'horario':
        horario = formatar_horario(message_text)
        if horario is None:
            await update.message.reply_text('Formato de horário inválido. O horário de funcionamento é entre as 09:00 até as 17:00')
            return

        cliente = context.user_data['nome']
        servico = context.user_data['servico']
        servicos

        if verificar_agendamento(horario, cliente, servico):
            servico_nome = servicos.get(servico)
            await update.message.reply_text(f'Agendado: {cliente} - {servico_nome} às {horario}')
            await update.message.reply_text('Obrigado! Tenha um ótimo dia!')
        else:
            await update.message.reply_text(f'O horário {horario} já está ocupado. Por favor, escolha outro horário.')
            return
        context.user_data.clear()
    elif message_text == "ver agendamentos":
        if agenda:
            servicos
            agendamentos = "\n".join([f"{hora}: {detalhes['cliente']} - {servicos[detalhes['servico']]}" for hora, detalhes in agenda.items()])
            await update.message.reply_text(f'Agendamentos do dia:\n{agendamentos}')
        else:
            await update.message.reply_text('Não há agendamentos em espera.')
    elif context.user_data.get('stage') == 'finalizar':
        if message_text.lower() == 'sim':
            await update.message.reply_text('Digite:\n1. Reagendar\n2. Falar com a recepção\n3. Finalizar')
            context.user_data['stage'] = 'opcao'
        else:
            await update.message.reply_text('Obrigado! Tenha um ótimo dia!')
            context.user_data.clear()
    elif context.user_data.get('stage') == 'opcao':
        if message_text == '1':
            context.user_data['stage'] = 'nome'
            await update.message.reply_text('Qual é o seu nome?')
        elif message_text == '2':
            await update.message.reply_text('Você está em espera. Um atendente da recepção entrará em contato em breve.')
            context.user_data.clear()
        elif message_text == '3':
            await update.message.reply_text('Obrigado! Tenha um ótimo dia!')
            context.user_data.clear()
        else:
            await update.message.reply_text('Opção inválida. Por favor, escolha uma opção válida.')
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