# WhatsApp Chat Analyzer
# Input: Chat text file
# Output:
          # For Each Person:
            # Number of Messages
            # Number of Words
            # Top 50 Most Used Words
            # Number of Questions
            # 1 Word Replies
import datetime

# Word List
wordFile = open("words.txt", "r")
wordLine = wordFile.readline()
wordList = wordLine.split()

whatsAppFile = open('_chat.txt', "r")

results = open('results.txt', 'w')

totalMessageCount = 0
kunal = {}
kunalMessageCounter = 0
kunalWordCounter = 0
kunalQuestionCounter = 0
kunalOneWordReplies = 0
akshar = {}
aksharMessageCounter = 0
aksharWordCounter = 0
aksharQuestionCounter = 0
aksharOneWordReplies = 0

# Start Date and End Date
startDate = datetime.date(2014, 3, 1)
endDate = datetime.date(2017, 3, 1)

for line in whatsAppFile:
  messageList = line.strip().split(" ")
  date = messageList[0].strip(",").split("/")
  try:
    dateObj = datetime.date(int("20" + date[2]), int(date[0]), int(date[1]))
    if dateObj >= startDate and dateObj <= endDate:
      totalMessageCount += 1
      if messageList[3].strip(" :") == "Kunal":
        length = len(messageList[4:])
        kunalMessageCounter += 1
        if length == 1:
          kunalOneWordReplies += 1
        kunalWordCounter += length
        for word in messageList[4:]:
          if "?" in word:
            kunalQuestionCounter += 1
          cleanWord = word.lower().strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
          if cleanWord not in wordList and "'" not in cleanWord and len(cleanWord) > 2:
            kunal[cleanWord] = kunal.get(cleanWord, 0) + 1
      elif messageList[3].strip(" :") == "Akshar":
        length = len(messageList[5:])
        aksharMessageCounter += 1
        if length == 1:
          aksharOneWordReplies += 1
        aksharWordCounter += length
        for word in messageList[5:]:
          if "?" in word:
            aksharQuestionCounter += 1
          cleanWord = word.lower().strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
          if cleanWord not in wordList and "'" not in cleanWord and len(cleanWord) > 2:
            akshar[cleanWord] = akshar.get(cleanWord, 0) + 1
  except:
    pass


results.write("Total Messages: %s\n\n" % (totalMessageCount))
results.write("Kunal\n")
results.write("Messages: %s\n" % (kunalMessageCounter))
results.write("Words: %s\n" % (kunalWordCounter))
results.write("Questions: %s\n" % (kunalQuestionCounter))
results.write("One Word Replies: %s\n" % (kunalOneWordReplies))
results.write("Most Used Words: %s\n" % (sorted(kunal, key=kunal.get, reverse=True)[:50]))
results.write("\n")
results.write("Akshar\n")
results.write("Messages: %s\n" % (aksharMessageCounter))
results.write("Words: %s\n" % (aksharWordCounter))
results.write("Questions: %s\n" % (aksharQuestionCounter))
results.write("One Word Replies: %s\n" % (aksharOneWordReplies))
results.write("Most Used Words: %s\n" % (sorted(akshar, key=akshar.get, reverse=True)[:50]))
results.write("\n")



whatsAppFile.close()
results.close()