import datetime

def main(chatFile, wordFile):
  # Create the word list with the word file
  wordList = load_words(wordFile)
  # Open chat file
  whatsAppFile = open(chatFile, "r")
  # Open the results file to write in
  results = open('results.txt', 'w')

  # List to hold Dates, Message Counts, and Word Counts for each Person
  dataList = [[], "", [], [], "", [], []]

  # Total Message Count [0]
  # Person 1 [1], Message Counter [2], Word Counter [3], Question Counter [4], One Word Replies [5]
  # Person 2 [6], Message Counter [7], Word Counter [8], Question Counter [9], One Word Replies [10]
  # Person 1 Words Dictionary [11], Person 2 Words Dictionary [12]
  count = [0, "", 0, 0, 0, 0, "", 0, 0, 0, 0, {}, {}]

  invalidLines = 0
  setNames = True
  month = 0
  year = 2000

  for line in whatsAppFile:
    try:
      messageList = parseLine(line)
      if setNames:
        if count[1] == "":
          count[1] = messageList[1]
          dataList[1] = messageList[1]
          month = messageList[0].month
          year = messageList[0].year
        elif count[6] == "" and messageList[1] != count[1]:
          count[6] = messageList[1]
          dataList[4] = messageList[1]
          setNames = False
      if messageList[0].month != month:
        updateResults(month, year, count, dataList, results)
        person1 = count[1]
        person2 = count[6]
        count = [0, person1, 0, 0, 0, 0, person2, 0, 0, 0, 0, {}, {}]
        month = messageList[0].month
        year = messageList[0].year
      messageCounts(messageList, count)
      parseWords(messageList, count, wordList)
    except:
      invalidLines += 1
      print(invalidLines)

  updateResults(month, year, count, dataList, results)

  whatsAppFile.close()
  results.close()
  return dataList

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

def messageCounts(messageList, countList):
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
    word = word.lower().strip(" :?.!")
    if len(word) > 3 and word not in wordList and "'" not in word and "<" not in word and ">" not in word:
      if messageList[1] == countList[1]:
        countList[11][word] = countList[11].get(word, 0) + 1
      elif messageList[1] == countList[6]:
        countList[12][word] = countList[12].get(word, 0) + 1

def updateResults(month, year, countList, dataList, resultsFile):
  dataList[0].append(datetime.datetime(year, month, 1))
  dataList[2].append(countList[2])
  dataList[5].append(countList[7])
  dataList[3].append(countList[3])
  dataList[6].append(countList[8])
  resultsFile.write("%s/%s\n" % (month, year))
  printResults(resultsFile, countList)

def printResults(resultsFile, count):
  resultsFile.write("Total Messages: %s\n\n" % (count[0]))
  resultsFile.write("%s\n" % (count[1]))
  resultsFile.write("Messages: %s\n" % (count[2]))
  resultsFile.write("Words: %s\n" % (count[3]))
  resultsFile.write("Questions: %s\n" % (count[4]))
  resultsFile.write("One Word Replies: %s\n" % (count[5]))
  resultsFile.write("Most Used Words: %s\n" % (sorted(count[11], key=count[11].get, reverse=True)[:50]))
  resultsFile.write("\n")
  resultsFile.write("%s\n" % (count[6]))
  resultsFile.write("Messages: %s\n" % (count[7]))
  resultsFile.write("Words: %s\n" % (count[8]))
  resultsFile.write("Questions: %s\n" % (count[9]))
  resultsFile.write("One Word Replies: %s\n" % (count[10]))
  resultsFile.write("Most Used Words: %s\n" % (sorted(count[12], key=count[12].get, reverse=True)[:50]))
  resultsFile.write("\n")