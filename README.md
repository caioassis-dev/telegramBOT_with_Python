
# 📅 TelegramBot + Python 📅

* Criando um bot no telegram com scripts em python para que os clientes consigam agendar de forma automatica os serviços disponiveis no salão.

<div style="display:inline_block" >
  
 <img align="center" alt="Python" src="https://cdn.picpng.com/logo/language-logo-python-44976.png" style="height:50px; width:auto" target="_blank">
 <img align="center" alt="Telegram" src="https://logodownload.org/wp-content/uploads/2017/11/telegram-logo-0-2-1536x1536.png" style="height:50px; width:auto" target="_blank">

## Haircut bot de automatização para agendamento de serviços.

* Utilizado as seguintes bibliotecas para integrar ao sistema de API do Telegram:

* typing, telegram, datetime, decouple, telegram.ext

Estou salvando as informações dos agendamentos em um dicionario, pois esse é um app apenas na versão BETA.

Para versão de produção o correto e adicionar as informações dos clientes em um banco de dados, pode ser um SQLITE3 apenas para que isso seja salvo em um local onde a aplicação pode ser desligada e os dados não são perdidos.

A outra ideia é interligar os agendamentos direto na agenda do estabelecimento para que o pessoal da recepção tenha acesso direto pelo calendario do celular e computador e ver todos os agendamentos do dia.

Também podemos implementar a opção de agendar para outros dias e não apenas para o dia atual, o que no beta ainda não foi feito.

Qual o motivo da versão BETA não adicionarmos tudo? 
Normalmente essa versão é feita para que o cliente faça sua análise para que na próxima versão, o produto fique igual ao que ele está imaginando. 
Isso é feito para otimizar a produção e não perder tempo com trabalho desnecessário.

### Imagem de uma interação com o BOT, simulação de um cliente agendando um serviço:

* clique na imagem e veja o video do bot funcionando no Youtube:

[![Captura de Tela 2024-06-30 às 16 04 56](https://github.com/caioassis-dev/books_data_analysis_with_pandas/assets/61170444/56ab13ef-9c9d-4a8c-9f36-4eb1cc94d65e)](https://youtu.be/1T9R1Y9C7no?si=s5E7BEzXV1zFsZsn)


