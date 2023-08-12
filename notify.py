#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import json
import random
import httplib, urllib
import argparse

class Telebot:

    phrases = [
        "Привет человеки. У меня хорошие новости - я начал раскатывать релиз. В него вошли следующие изменения:",
        "Всем привет. Кажется началась раскатка релиза. В ближайшее время может пойти что нибудь не так:",
        "Эй человеки, у нас сейчас будет апдейт боя. Вот что в нем появилось:",
        "Святые шарики, кажется у нас деплой. Вот что в нем:",
        "Привет бездельники. Это снова я, катаю вам новый релиз:",
        "Внимание всем постам. Идет раскатка новой версии боя. В ней есть вот это:",
        "Карамба, случился релиз. В него вошло это:",
        "Если в ближайшее время что-то упадет - это был релиз:",
        "Семь раз отмерь, один раз задеплой. Но это все не про нас, катаем релиз:",
        "Уж не знаю деплоятся ли нормальные люди в это время, но я начал катать следующие вещи:",
        "Страусы от страха прячут голову в песок, советую всем испугаться, потому что начался релиз:",
        "Семь бед - один деплой. Сейчас раскатаем следующую ерунду:",
        "У вас скучная жизнь? Позвольте вам ее разнообразить, у нас релиз:",
        "Не подумайте ничего плохого, но я решил сделать деплой:",
        "Скучный день (( Получайте деплой:",
        "Кажется кто то хочет повеселиться? Ловите новый релиз:",
        "Алярма! Сейчас на бой попадет новый релиз:",
        "Смерть всем человекам! Но сначала помучайтесь с новым релизом:",
        "Не было печали...апдейты раскатали:",
        "Надеюсь у вас много свободного времени, я выливаю новый релиз:"
    ]

    benderSettings = {
        "username": "Bender (Production Deployment)",
        "fallback": "Выливка нового релиза",
    }

    def __init__(self, telegramBotId="", telegramToken="", chatId=""):
        self.username = "Bender (Production Deployment)"
        self.telegramBotId = "your_botId"
        self.telegramToken = "your_token"
        self.chatId = "@bntvp"
        self.botMessage = "Выливка нового релиза"
        #тут иконка ротоба бендера
        self.botIcon = "https://www.shareicon.net/download/128x128//2016/01/06/234422_bender_256x256.png"
        pid = random.randint(1, len(self.phrases) - 1)
        self.preText = self.phrases[pid]

    #Продумать, какие еще запросы можно делать боту
    def makeBotRequest(self, method, options):
        teleh = "api.telegram.org"
        telePath = "/bot{}:{}/{}".format(self.telegramBotId, self.telegramToken, method)
        debug("Send query " + telePath)

        headers = {"Content-type" : "application/json"}

        conn = httplib.HTTPSConnection(teleh, 443)
        debug('query data is ' + str(json.dumps(options['query'])))

        #conn.set_debuglevel(1);

        conn.request('POST', telePath, json.dumps(options['query']), headers)
        response = conn.getresponse()
        data = response.read()

        debug("respom " + str(response.reason))
        debug(data)

    def setPretext(self, msg = ""):
        self.preText = msg

    def sendTelegramBot(self, gitMsg):
        botUrl = "https://api.telegram.org/bot{}:{}/sendMessage".format(self.telegramBotId,self.telegramToken)
        debug('Forming bot html message')
        notifyText = ''
        for commit in gitMsg:
           debug('In python json may be converted to string' + str(commit))
           debug('title is ' + commit['title'])
           notifyText += "<strong><i>" + commit['title'] + "</i></strong>\n"
           notifyText += commit['value'] + "\n"

        title = self.preText
        botMsg = "{}\n\n".format(self.botMessage)
        if title:
            botMsg += "<strong>{}</strong>\n\n".format(title)

        botMsg += "{}".format(notifyText)
        if self.botIcon:
            botMsg += "<a href=\"{}\">&#8205;</a>".format(self.botIcon)

        debug('Bot message ' + botMsg)
        options = {
            "query" : {
                "chat_id": self.chatId,
                "text"   : botMsg,
                "parse_mode" : 'Html',
                "disable_notification" : True,
                "protect_content"      : True,
                "disable_web_page_preview" : False,
                "reply_to_message_id" : 0,
                "allow_sending_without_reply" : True,
            },
            "http_errors"     : "false",
            "timeout"         : 100,
            "read_timeout"    : 100,
        }
        debug("Request to {}. Data: {}".format(botUrl, options['query']))
        self.makeBotRequest('sendMessage', options)

def debug(message):
    print message

groupedData = {}
# читаем stdin, список комитов, которые будут запущены в приложении на бою
for line in sys.stdin.readlines():
    #debug("read line from stdin {}".format(line))
    debug("read line from stdin: " + line)

    data = line.split(' SEPARATOR ')
    msg = data[1]
    debug('message is:' + msg)
    split = msg.split(' ')
    key = split[0]
    debug('key value is:' + key)
    #добавить отладку и посмотреть какие значения бывают key
    if key not in groupedData:
        groupedData[key] = []
    groupedData[key].append(">> " + msg.strip())

commits = []
for key in groupedData:
    #видимо в ключах бывают комментарии комитов,
    #бывают комиты слияния они начинаются с Merge и не несут информации
    if key == "Merge":
        continue

    #как работает append??
    commits.append({
        "title" : key,
        "short" : False,
        "value" : "\n".join(groupedData[key])
    })

def createParser ():
    parser = argparse.ArgumentParser()
    parser.add_argument ('-s', '--stage')

    return parser

if __name__ == "__main__":
    parser = createParser()
    namespace = parser.parse_args()

    bot = Telebot()

    if namespace.stage == "ares":
        print ("ares")
        bot.botMessage = "Выливка на арес"
        bot.setPretext()
        bot.botIcon = None
    if namespace.stage == "prequest-ares":
            print ("ares")
            bot.botMessage = "Новые изменения добавлены в основную ветку"
            bot.setPretext()
            bot.botIcon = None
    bot.sendTelegramBot(commits)