import analyzer
import datetime
import pygal


# list to hold dates, message counts, and word counts for each user
# dataList = [[], "", [], [], "", [], []]
dataList = analyzer.main("_chat.txt", "words.txt")

# bar graph of the message count between the two users
chart = pygal.Bar(x_label_rotation=20, width=2000, height=1000, truncate_legend=50)
chart.title = 'WhatsApp Chat Analysis: Messages'
chart.x_title = "Months"
chart.y_title = "Messages"
chart.x_labels = map(lambda d: d.strftime('%Y/%m'), dataList[0])
chart.add("%s's Messages" % (dataList[1]), dataList[2])
chart.add("%s's Messages" % (dataList[4]), dataList[5])
chart.render_to_file('messagesChart.svg')

# bar graph of the word count between the two users
chart = pygal.Bar(x_label_rotation=20, width=2000, height=1000, truncate_legend=50)
chart.title = 'WhatsApp Chat Analysis: Words'
chart.x_title = "Months"
chart.y_title = "Words"
chart.x_labels = map(lambda d: d.strftime('%Y/%m'), dataList[0])
chart.add("%s's Words" % (dataList[1]), dataList[3])
chart.add("%s's Words" % (dataList[4]), dataList[6])
chart.render_to_file('wordsChart.svg')