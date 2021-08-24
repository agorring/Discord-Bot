# bot.py
"""
Author: Adam M. Gorring

If the pip package manager is available on the device, the following command in the console will install the discord.py package required to run the file.
    pip3 install -U discord.py

To execute the file, enter "python3" followed by the file path into the console

"""
import discord
import random
import csv
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

class QA:
  def __init__(self, question, answer):
    self.question = question
    self.answer = answer

def question_check(message):
    #Check if messages contain a "?"
    if "?" in message:
        return True
    
    else:
        return False

# SECTION Connect the bot to the server
GUILD = "ploopy's server"
client = discord.Client()
@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to\n'
        f'{guild.name}(id: {guild.id})\n'
    )

# SECTION Read CSV
# Loops through lines in the dataset using csv reader. Every line (except for the column names) is appended to QaList as an instance of QA.
QaList = []
with open('QA.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        
        #The Question column prints as "ï»¿Question". I don't know why. So "ï»¿Question" is used to refer to the column.
        QaList.append(QA(row["ï»¿Question"], row["Answer"]))
        line_count += 1

    print(f'Processed {line_count} lines.')

# SECTION Respond to messages
@client.event
async def on_message(message):

    if message.author == client.user:
        # If message author is the bot, don't respond. Prevents the bot from replying to itself.
        return

    similarity_score = 0
    set_question = ""

    if question_check(message.content):
        # Only continue if the message is a question
        for question in QaList:
            # Loop through every question in the data to determine the most likely match
            if similar(message.content, question.question) > similarity_score:
                similarity_score = similar(message.content, question.question)
                set_question = question

        if similarity_score > 0.6:
            # Only continue if the chosen message has a similarity score higher than 0.6
            answers = []
            for question in QaList:
                # Loop through every question to see if the set_question has multiple answers; append the answers into the list.
                if question.question == set_question.question:
                    answers.append(question.answer)

            response = random.choice(answers)
            await message.channel.send(response)

client.run("Insert Bot Token")
# Run using the bot's authentication token
