import datetime

def main(chatFile, wordFile):
  # Create the word list with the word file
  wordList = load_words(wordFile)
  # Open chat file
  whatsAppFile = open(chatFile, "r")
  # Open the results file to write in
  results = open('results.txt', 'w')

  # Total Message Count [0]
  # Person 1 [1], Message Counter [2], Word Counter [3], Question Counter [4], One Word Replies [5]
  # Person 2 [6], Message Counter [7], Word Counter [8], Question Counter [9], One Word Replies [10]
  # Person 1 Words Dictionary [11], Person 2 Words Dictionary [12]
  count = [0, "", 0, 0, 0, 0, "", 0, 0, 0, 0, {}, {}]

  setNames = True
  month = 0
  year = 2000

  for line in whatsAppFile:
    try:
      messageList = parseLine(line)
      if setNames:
        if count[1] == "":
          count[1] = messageList[1]
          month = messageList[0].month
          year = messageList[0].year
        elif count[6] == "" and messageList[1] != count[1]:
          count[6] = messageList[1]
          setNames = False
      if messageList[0].month != month:
        results.write("%s/%s\n" % (month, year))
        printResults(results, count)
        person1 = count[1]
        person2 = count[6]
        count = [0, person1, 0, 0, 0, 0, person2, 0, 0, 0, 0, {}, {}]
        month = messageList[0].month
        year = messageList[0].year
      else:
        messageCounts(messageList, count, wordList)
        parseWords(messageList, count, wordList)
    except:
      print(line)

  results.write("%s/%s\n" % (month, year))
  printResults(results, count)

  whatsAppFile.close()
  results.close()



def printResults(fileObj, count):
  fileObj.write("Total Messages: %s\n\n" % (count[0]))
  fileObj.write("%s\n" % (count[1]))
  fileObj.write("Messages: %s\n" % (count[2]))
  fileObj.write("Words: %s\n" % (count[3]))
  fileObj.write("Questions: %s\n" % (count[4]))
  fileObj.write("One Word Replies: %s\n" % (count[5]))
  fileObj.write("Most Used Words: %s\n" % (sorted(count[11], key=count[11].get, reverse=True)[:50]))
  fileObj.write("\n")
  fileObj.write("%s\n" % (count[6]))
  fileObj.write("Messages: %s\n" % (count[7]))
  fileObj.write("Words: %s\n" % (count[8]))
  fileObj.write("Questions: %s\n" % (count[9]))
  fileObj.write("One Word Replies: %s\n" % (count[10]))
  fileObj.write("Most Used Words: %s\n" % (sorted(count[12], key=count[12].get, reverse=True)[:50]))
  fileObj.write("\n")

def messageCounts(messageList, countList, wordList):
  '''
  messageList (list): a list containing the message words.
  countList (list): the variable list used store word counts.
  Input: ["3/27/14", "Kunal", "<\u200eimage", "omitted>"]

  Returns: the count list with updated values for total message increment, person message increment, word counter, question counter, and one word reply counter.
  Output: None. (bi-product changes the lists)
  '''
  wordCounter = len(messageList[2:])
  questionCounter = 0
  oneWordReply = 0

  for word in messageList[2:]:
    if "?" in word:
      questionCounter += 1

  if wordCounter == 1:
    oneWordReply = 1

  if messageList[1] == countList[1]:
    countList[0] += 1
    countList[2] += 1
    countList[3] += wordCounter
    countList[4] += questionCounter
    countList[5] += oneWordReply
  elif messageList[1] == countList[6]:
    countList[0] += 1
    countList[7] += 1
    countList[8] += wordCounter
    countList[9] += questionCounter
    countList[10] += oneWordReply

def parseWords(messageList, countList, wordList):
  for word in messageList[2:]:
    if word.lower() not in wordList and "'" not in word and len(word) > 2:
      if messageList[1] == countList[1]:
        countList[11][word] = countList[11].get(word, 0) + 1
      elif messageList[1] == countList[6]:
        countList[12][word] = countList[12].get(word, 0) + 1


def parseLine(line):
  '''
  line (string): a line read from the opened file.
  Input: 3/27/14, 10:21:13 AM: Kunal Patel: <‎image omitted>

  Returns: a list with the date at the [0] spot, name at the [1] spot, and the messaged from [2:].
  Output: ["3/27/14", "Kunal", "<\u200eimage", "omitted>"]
  '''
  messageList = []
  lineList = line.strip().split(" ")
  messageList.append(datetime.datetime.strptime(lineList[0].strip(","),"%m/%d/%y"))
  messageList.append(lineList[3].strip(":"))
  for i in range(3, len(lineList)):
    if ":" in lineList[i]:
      messageList = messageList + lineList[i+1:]
  return messageList

def load_words(file_name):
  '''
  file_name (string): the name of the file containing
  the list of words to load

  Returns: a list of valid words. Words are strings of lowercase letters.

  Depending on the size of the word list, this function may
  take a while to finish.
  '''
  # inFile: file
  in_file = open(file_name, 'r')
  # line: string
  line = in_file.readline()
  # word_list: list of strings
  word_list = line.split()
  in_file.close()
  return word_list

main("_chat.txt", "words.txt")