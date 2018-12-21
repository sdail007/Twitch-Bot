from BotInterfaces.BotComponent import BotComponent
from Commands.Trigger import Trigger
from Commands.Response import CodeResponse, Response

import pygsheets

import codecs, json
from threading import Timer, Lock


class MovieNightPoll(BotComponent):
    OpenPollMessage = 'The submission window for Movie Night nominations has ' \
                      'opened! ' \
                      'Submit your vote with !vote {movie}. To view ' \
                      'current standings and rules: !movies'

    ClosePollMessage = 'The current submission window has ended! Thank you ' \
                       'for your submissions <3 To view ' \
                       'current standings and rules: !movies'

    RankingsMessage = 'Current Movie Night submission Rankings and Rules: {}'

    def __init__(self, connection, file):
        super(MovieNightPoll, self).__init__(connection)

        #read settings in from file
        if file is not None:
            with codecs.open(file, encoding="utf-8-sig", mode="r") as f:
                settings = json.load(f, encoding="utf-8")
            self.submissionWindowLength = int(settings["WindowLength"])
            self.intervalLength = int(settings["IntervalLength"])
            self.confirmSubmissions = settings["ConfirmVotes"]
            self.spreadsheetUrl = settings["SpreadsheetUrl"]
            self.spreadsheetName = settings["SpreadsheetName"]
        else:
            self.submissionWindowLength = 10  # 60 * 1
            self.intervalLength = 30 * 60
            self.confirmSubmissions = False

        print self.submissionWindowLength, self.intervalLength,\
            self.confirmSubmissions

        vote = Trigger("!vote")
        voter = CodeResponse(0, self.RegisterVote)
        voter.addTrigger(vote)
        self.triggers.append(vote)

        openpoll = Trigger("!openpoll")
        openpollr = CodeResponse(0, self.OpenPollResponse)
        openpollr.addTrigger(openpoll)
        #self.triggers.append(openpoll)

        rankingst = Trigger("!movies")
        rankingsr = Response(MovieNightPoll.RankingsMessage
                             .format(self.spreadsheetUrl), 30)
        rankingsr.addTrigger(rankingst)
        self.triggers.append(rankingst)

        self.poll = PollWriter(self.spreadsheetName)

        #prepare timers
        self.submissionWindowTimer = None
        self.intervalTimer = Timer(10, self.IntervalTick)
        self.intervalTimer.start()

        self.PollOpen = False

        self.voters = []
        return

    def IntervalTick(self):
        self.intervalTimer = Timer(self.intervalLength, self.IntervalTick)
        self.intervalTimer.start()

        self.OpenPoll()
        return

    def OpenPollResponse(self, sender, message, *args):
        self.OpenPoll()

    def OpenPoll(self):
        print 'opening submission window'
        #prevent submission window from being opened twice
        if self.submissionWindowTimer is not None:
            if self.submissionWindowTimer.is_alive():
                return

        #start submission window timer
        self.submissionWindowTimer = Timer(self.submissionWindowLength,
                                           self.ClosePoll)
        self.submissionWindowTimer.start()

        #notify chat the poll has started
        self.connection.send_message(MovieNightPoll.OpenPollMessage)

        self.voters = []
        self.PollOpen = True
        return

    def ClosePoll(self):
        print 'closing poll'
        if self.submissionWindowTimer is not None:
            if self.submissionWindowTimer.is_alive():
                self.submissionWindowTimer.cancel()

        self.PollOpen = False

        self.poll.Close()

        self.submissionWindowTimer = None

        self.connection.send_message(MovieNightPoll.ClosePollMessage)
        print 'poll closed'
        return

    def RegisterVote(self, sender, message, *args):
        if not self.PollOpen:
            return
        # no duplicate votes
        if message.Sender in self.voters:
            return

        self.voters.append(message.Sender)

        vote = message.Message[5:].lstrip(' ')

        if self.poll.RegisterVote(vote) and self.confirmSubmissions:
            sender.send_message("vote registered")
        return

    def shutdown(self):
        if self.intervalTimer is not None:
            if self.intervalTimer.is_alive():
                self.intervalTimer.cancel()

        if self.submissionWindowTimer is not None:
            if self.submissionWindowTimer.is_alive():
                self.submissionWindowTimer.cancel()

        self.poll.Close()
        return


class PollWriter(object):
    def __init__(self, spreadsheetName):
        self.mutex = Lock()

        self.client = pygsheets.authorize()

        self.sh = self.client.open(spreadsheetName)
        self.wks = self.sh.sheet1

        existing = self.wks.get_values('A2', 'B500', include_empty=False)

        self.previous_votes = {}
        self.CalculatePreviousVotes()
        return

    def CalculatePreviousVotes(self):
        existing = self.wks.get_values('A2', 'B500', include_empty=False)

        self.previous_votes = {}
        row = 1

        for previous_vote in existing:
            if len(previous_vote) > 1:
                row += 1

                movie = previous_vote[0]
                votes = int(previous_vote[1])

                self.previous_votes[movie] = (votes, row)
        return


    def RegisterVote(self, vote):
        self.mutex.acquire()

        capitalized = [word.lower().capitalize() for word in vote.split()]
        vote = ' '.join(capitalized)

        print vote, len(vote)

        if len(vote) == 0:
            return False

        try:
            #voting for existing movie
            if vote in self.previous_votes:
                votes = self.previous_votes[vote][0]
                row = self.previous_votes[vote][1]

                newVotes = votes + 1

                self.previous_votes[vote] = (newVotes, row)
                cell = 'B' + str(row)

                self.wks.update_value(cell, str(newVotes))
            else:
                #new movie added!
                row = len(self.previous_votes) + 2  #header row + 1
                self.previous_votes[vote] = (1, row)

                self.wks.update_values(crange='A' + str(row) + ':B' + str(row),
                                       values=[[vote, '1']])

        finally:
            self.mutex.release()
        return True



    def Close(self):
        self.wks.sort_range('A2', 'B500', basecolumnindex=1,
                            sortorder='DESCENDING')

        self.CalculatePreviousVotes()
        return
