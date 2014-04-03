#!/usr/bin/env python
import re
import csv
import sqlite3

def print_inconsistent_ballot_box(row):
    print("Inconsistency! (" + row[1] + ", " + str(row[2]) + ")")

def read_bb_from_csv(csv_reader):
    data = []
    header = []
    rownum = 0
    for row in csv_reader:
        if rownum > 0:
            data.append(row)
        else:
            header = [col.replace(' ', '_') for col in row]
        rownum += 1
    return (header, data)

def main():
    in_file = open("ANKARA.csv", "r")
    f = csv.reader(in_file)

    (header, rows) = read_bb_from_csv(f)

    in_file.close()
    print('CSV parsed.')

    party_dict = {}

    for party in header[13:30]:
        party_dict[party] = 0

    extras = 0
    num_extras = 0
    fazlalik = 0
    num_fazlalik = 0
    eksiklik = 0
    num_eksiklik = 0
    for row in rows:
        row = row[:5] + [int(col) for col in row[5:]]
        fault_noted = False

        if row[9] + row[10] != row[11]:
            print_inconsistent_ballot_box(row)
            fault_noted = True
            print("Itirazsiz(" + str(row[9]) + ") ve itirazli(" +\
                  str(row[10]) + ") gecerli oylarin toplami gecerli oylara(" +\
                  str(row[11]) + ") esit degil.")

        if row[11] + row[12] != row[8]:
            if not fault_noted:
                print_inconsistent_ballot_box(row)
            fault_noted = True
            print("Gecerli(" + str(row[11]) + ") ve gecersiz(" +\
                  str(row[12]) + ") oylarin toplami kullanilan toplam oya(" +\
                  str(row[8]) + ") esit degil.")
        
        if row[8] > row[5]:
            if not fault_noted:
                print_inconsistent_ballot_box(row)
            fault_noted = True
            print("Kayitli secmen sayisindan(" + str(row[5]) +\
                  ") fazla oy(" + str(row[8]) + ") kullanilmis.")
            extras += row[8] -row[5]
            num_extras += 1

        sum_votes = 0
        for i in range(13, 30):
            party_dict[header[i]] += row[i]
            sum_votes += row[i]

#        if row[30] != row[11]:
#            if not fault_noted:
#                print_inconsistent_ballot_box(row)
#            fault_noted = True
#            print("Partilerin oylarinin toplami(" + str(row[11]) +\
#                  ") STS'deki \"Partilerin Toplam Oyu\"na(" + str(row[30]) +\
#                  ") esit degil.")

        if sum_votes != row[11]:
            if not fault_noted:
                print_inconsistent_ballot_box(row)
            fault_noted = True
            print("Partilerin oylarinin toplami(" + str(sum_votes) +\
                  ") gecerli oy sayisina(" + str(row[11]) + ") esit degil.")
            if sum_votes > row[11]:
                fazlalik += sum_votes - row[11]
                num_fazlalik += 1
            else:
                eksiklik += row[11] - sum_votes
                num_eksiklik += 1

    print('')
    for vote_pair in party_dict.items():
        print(vote_pair[0] + " toplam oyu: " + str(vote_pair[1]))
    print("\nkayit-fazlasi secmenden gelen fazlalik oy: " + str(extras))
    print("bu durumun karsilasildigi sandik sayisi: " + str(num_extras) + "\n")
    print("parti oylari toplaminin gecerli oy sayisini astigi sandiklardaki "+\
          "fazlalik oy: " + str(fazlalik))
    print("bu durumun karsilasildigi sandik sayisi: " + str(num_fazlalik) + "\n")
    print("parti oylari toplaminin gecerli oy sayisinin altinda kaldigi "+\
          "sandiklardaki buharlasan oy: " + str(eksiklik))
    print("bu durumun karsilasildigi sandik sayisi: " + str(num_eksiklik) + "\n")



if __name__ == '__main__':
    main()
