Turkey Mayoral Elections Data
===============

This is just an attempt to help analysts get the mayoral election data of Ankara easier. You can find the data in .csv and .sql formats.

Data
---------------

Data is fetched from the online election stats system STS(http://sts.chp.org.tr) provided by the main opposition party of Turkey(CHP). In STS, each ballot box data had a different timestamp indicating when the data was obtained from the Supreme Electoral Council(YSK) of Turkey. Those timestamps are preserved in the data as well.

You should take into account two details when utilizing the data. First is that, probably due to the lack of effort from the relevant CHP staff, <b>data of 25248 ballot boxes are missing from STS</b>, which accounts for roughly 10% of the whole ballot boxes. I plan to locate soon the origin of those boxes information of which are missing.

Second thing to be cautious about is the total number of ballot boxes present in the archive of STS. On the elections web page of Hurriyet(http://secim2014.hurriyet.com.tr/) it is stated that there are 194507 ballot boxes nationwide, but there appears to be data on 194695 ballot boxex on STS. While forming the SQL dump I inserted data to an actual SQL database, and no error due to primary key occured. So, even though I could not find the source of these extra boxes, I can state that they all have different values for the tuple (city, district, id).

I am planning to update the data, as it may be subject to change. Note that, though, this is a separate effort from the opposition party CHP and it is bound by their capability of obtaining the most recent data from YSK and publishing it through their website.

Initial Analysis
---------------

I also wrote a tiny bit of code which checks simple arithmetics that should hold for each properly counted ballot box. You can run it using the Makefile provided, or manually entering the commands it contains to the command line.

In the section below I briefly summarize the results of my initial checks. I encourage anyone interested to check out the code itself and correct me if I am wrong, as well as offer me suggestions as to what I should analyze/check next. After all, this was a really a naive attempt made in the late hours of the night.

I found two types of irregularities. First is an inconsistency between the number of people assigned to a ballot box and the number of votes that came out of that box. The second is and inconsistency between the sum of the votes all the parties got from a ballot box and total amount of valid votes that came out of that box.

On the national scale, 2414 of the ballot boxes contained more votes than the number of people assigned to those boxes. Overall, this irregularity caused 22707 <b>extra</b> votes. The number of such ballot boxes for Ankara is 180, and a number of 593 extra votes came out of them.

Again on national scale, in 23128 of the ballot boxes there were missing votes. In other words, the summation of the votes each party got from a ballot box is less than total number of valid votes that came out of that box. Due to this inconsistency, there appears to be 231031 valid votes that are somehow missing. The pair of numbers regarding this type of irregularity in Ankara scale is 2857-many ballot boxes and 3835 votes.

Though this late-night analysis could not find game changing results, I hope people can benefit from the data I am providing, and perhaps find some more interesting facts about this weird mayoral election tornado Turkey has gone through.
