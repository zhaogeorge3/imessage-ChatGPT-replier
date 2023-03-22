from imessage_reader import fetch_data
import os
from time import sleep
import openai

openai.api_key = ""

WIFE_NUMBER = ""

SENDER_NUMBER_INDEX = 0
MESSAGE_INDEX = 1
DATE_INDEX = 2
MESSAGE_TYPE_INDEX = 3
YOUR_NUMBER_INDEX = 4
WHO_SENT_THIS_TEXT_INDEX = 5

SENT_FROM_YOU = 1
SENT_FROM_WIFE = 0

def getChatGptResponse(wifeText):
  return openai.Completion.create(
    model="text-davinci-003",
    prompt="write me a response for this text from my wife \"" + wifeText + "\" only return the response",
    temperature=0.5,
    max_tokens=60,
    top_p=1,
    frequency_penalty=0.5,
    presence_penalty=0,
    stop=["You:"]
  )
last_text = ""
answered_texts = ["", "", "", "", "", "", ""]
while True:
  fd = fetch_data.FetchData()
  messages = fd.get_messages()

  wife_messages = []
  unanswered_messaged = []
  for message in messages:
    if WIFE_NUMBER == message[0]:
      wife_messages.append(message)
  for i in range(1, 5):
    if wife_messages[-i][WHO_SENT_THIS_TEXT_INDEX] == SENT_FROM_WIFE and wife_messages[-i] not in answered_texts:
      unanswered_messaged.append(wife_messages[-i])
      answered_texts.append(wife_messages[-i])
      answered_texts.pop(0)
    else:
      break
  unanswered_messaged.reverse()
  full_text = ""
  for message in unanswered_messaged:
    full_text += message[1]+"\n"
  print(full_text)
  if (len(full_text) and full_text != last_text):
    last_text = full_text
    response = getChatGptResponse(full_text)
    reply = response["choices"][0]["text"]
    f = reply.strip()
    print(f)
    os.system("osascript sendMessage.applescript {} {}".format(WIFE_NUMBER, "\"" + f + "\""))
  sleep(15)





