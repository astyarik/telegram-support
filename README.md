# Telegram support bot (on aiogram)

Requirements:
1. Aiogram 3.x
2. Dotenv
(pip install -r requirements.txt)

Conten in .env:
`TOKEN='BOT_TOKEN' 
ADMIN_ID='ADMIN_ID'`

Content:
bot.py - main script
app/handlers.py - contain main mechanism of bot work (response on /start, work of inline buttons and etc)
app/keyboards.py - contain the contant of inline buttons

**handlers.py have "button1" and "button2" which you must fill in according to your needs.**

Author - Wobla
Purpose/Application: Support bot on telgram with information table and functions feedback

# How work:
1. On handlerds.py all functions go to work, what allows:
1.1 after /start click on Information/Support/Feedback (can edit names)
1.1.1 On information click on About us/Button 1/Button 2/Go back to menu (also can edit)
1.1.2 You can insert any text on information buttons
1.1.3 Buttong "Go back to menu" return menu Info.../Sup.../Feed...
2. When you click "Support" bot ask type reason of problem (you can add button "go back to menu")
2.1 After if user send message he gets message "Send to admin" and admin (ADMIN_ID) get his appeal and can response to him through button "Response"
