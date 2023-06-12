## Logic
There are two services
### First service - telegram bot
Saves the chat ID to the database at the start of communication in Telegram.

### Second service
The state from the service that we are interested in is periodically requested. If the state has changed and matches the condition, then messages are sent to chats.

## Interaction example
![image](https://github.com/IlnyrNazargulov/periodic-checking-bot/assets/43291422/9503d8bc-3fc3-499c-ad1a-5baada987383)

The meaning of the example: there is a search for a free place to go to the doctor. Free time for writing rarely appears.
