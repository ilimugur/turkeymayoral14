ANKARA Mayoral Elections Data
===============


This is just an attempt to help analysts get the mayoral election data of Ankara easier. You can find the data in .csv and .sql formats.

Data
---------------

Data is fetched from the online election stats system STS(http://sts.chp.org.tr) provided by the main opposition party of Turkey(CHP). In STS, each ballot box data had a different timestamp indicating when the data was obtained from the Supreme Electoral Council(YSK) of Turkey. Those timestamps are preserved in the data as well.

I am planning to update the data, as it may be subject to change. Note that, though, this is a separate effort from the opposition party CHP and it is bound by their capability of obtaining the most recent data from YSK and publishing it through their website.

Initial Analysis
---------------

I also wrote a tiny bit of code which checks simple arithmetics that should hold for each properly counted ballot box. In the section below I briefly summarize the results of my initial checks. I encourage anyone interested to check out the code itself and correct me if I am wrong, as well as offer me suggestions as to what I should analyze/check next. After all, this was a really a naive attempt made in the late hours of the night.

First and foremost, my preliminary evaluation shows a 32011-vote difference between AKP and CHP candidates.

I found two types of irregularities. First is an inconsistency between the number of people assigned to a ballot box and the number of votes that came out of that box. The second is and inconsistency between the sum of the votes all the parties got from a ballot box and total amount of valid votes that came out of that box.

180 of the ballot boxes contained more votes than the number of people assigned to those boxes. Overall, this irregularity caused 593 <b>extra</b> votes which apparently should not belong to those ballot boxes.

In 2857 of the ballot boxes there were missing votes. In other words, the summation of the votes each party got from a ballot box is less than total number of valid votes that came out of that box. Due to this inconsistency, there appears to be 3835 valid votes that are somehow missing.

Though this late-night analysis could not find game changing results, I hope people can benefit from the data I am providing, and perhaps find some more interesting facts about this weird mayoral election tornado Turkey has gone through.

Note to Self
---------------

Pull a nationwide-version of the data soon as I find the time. I am guessing there may be something more interesting in that scale, as Ankara was really the spot people focused on to. Who knows what happened far from sight in some distant county.
