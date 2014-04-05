#!/usr/bin/env python
import re
import csv
import sqlite3
import sys

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
    file_name = sys.argv[1]
    in_file = open(file_name, "r")
    f = csv.reader(in_file)

    (header, rows) = read_bb_from_csv(f)

    in_file.close()
    print('CSV parsed.')

    party_dict = {}

    for party in header[13:-1]:
        party_dict[party] = 0

    tum_partilerin_toplam_oyu = 0
    toplam_gecerli_oy = 0

    itirazli_siz_eksiklik = 0
    num_itirazli_siz_eksiklik = 0

    itirazli_siz_fazlalik = 0
    num_itirazli_siz_fazlalik = 0

    gecerli_siz_eksiklik = 0
    num_gecerli_siz_eksiklik = 0

    gecerli_siz_fazlalik = 0
    num_gecerli_siz_fazlalik = 0

    extras = 0
    num_extras = 0

    fazlalik = 0
    num_fazlalik = 0
    eksiklik = 0
    num_eksiklik = 0

    sts_total_fazlalik = 0
    num_sts_total_fazlalik = 0
    sts_total_eksiklik = 0
    num_sts_total_eksiklik = 0

    data_not_present_in_sts = 0
    data_present_in_sts = 0

    for row in rows:
        if row[4] == '-':
            data_not_present_in_sts += 1
            continue

        data_present_in_sts += 1

        row = row[:5] + [int(col) for col in row[5:]]
        fault_noted = False

        toplam_gecerli_oy += row[11]

        if row[9] + row[10] < row[11]:
            print_inconsistent_ballot_box(row)
            fault_noted = True
            print("Itirazsiz(" + str(row[9]) + ") ve itirazli(" +\
                  str(row[10]) + ") gecerli oylarin toplami gecerli oylardan(" +\
                  str(row[11]) + ") az.")
            itirazli_siz_eksiklik += row[8] - row[11] + row[12]
            num_itirazli_siz_eksiklik += 1

        if row[9] + row[10] > row[11]:
            print_inconsistent_ballot_box(row)
            fault_noted = True
            print("Itirazsiz(" + str(row[9]) + ") ve itirazli(" +\
                  str(row[10]) + ") gecerli oylarin toplami gecerli oylardan(" +\
                  str(row[11]) + ") fazla.")
            itirazli_siz_fazlalik += row[8] - row[11] + row[12]
            num_itirazli_siz_fazlalik += 1

        if row[11] + row[12] < row[8]:
            if not fault_noted:
                print_inconsistent_ballot_box(row)
            fault_noted = True
            print("Gecerli(" + str(row[11]) + ") ve gecersiz(" +\
                  str(row[12]) + ") oylarin toplami kullanilan toplam oydan(" +\
                  str(row[8]) + ") az.")
            gecerli_siz_eksiklik += row[8] - row[11] + row[12]
            num_gecerli_siz_eksiklik += 1

        if row[11] + row[12] > row[8]:
            if not fault_noted:
                print_inconsistent_ballot_box(row)
            fault_noted = True
            print("Gecerli(" + str(row[11]) + ") ve gecersiz(" +\
                  str(row[12]) + ") oylarin toplami kullanilan toplam oya(" +\
                  str(row[8]) + ") fazla.")
            gecerli_siz_fazlalik += row[11] + row[12] - row[8]
            num_gecerli_siz_fazlalik += 1
        
        if row[8] > row[5]:
            if not fault_noted:
                print_inconsistent_ballot_box(row)
            fault_noted = True
            print("Kayitli secmen sayisindan(" + str(row[5]) +\
                  ") fazla oy(" + str(row[8]) + ") kullanilmis.")
            extras += row[8] -row[5]
            num_extras += 1

        sum_votes = 0
        for i in range(13, len(header) - 1):
            party_dict[header[i]] += row[i]
            sum_votes += row[i]

#        if row[-1] != row[11]:
#            if not fault_noted:
#                print_inconsistent_ballot_box(row)
#            fault_noted = True
#            print("Partilerin oylarinin toplami(" + str(row[11]) +\
#                  ") STS'deki \"Partilerin Toplam Oyu\"nda(" + str(row[-1]) +\
#                  ") esit degil.")
#            if row[-1] > row[11]:
#                sts_total_fazlalik += row[-1] - row[11]
#                num_sts_total_fazlalik += 1
#            else:
#                sts_total_eksiklik += row[11] - row[-1]
#                num_sts_total_eksiklik += 1

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
    for vote_pair in sorted([(i[1], i[0]) for i in party_dict.items()]):
        tum_partilerin_toplam_oyu += vote_pair[0]
        print(vote_pair[1] + " toplam oyu: " + str(vote_pair[0]))
    print('\nTUM PARTILERIN TOPLAM OYU: ' + str(tum_partilerin_toplam_oyu))
    print('TOPLAM GECERLI OY: ' + str(toplam_gecerli_oy) + '\n')
    print("itirazli-itirazsiz gecerli oy toplaminin, gecerli oy sayisini astigi sandiklardaki "+\
          "fazlalik oylar toplami: " + str(gecerli_siz_fazlalik))
    print("bu durumun karsilasildigi sandik sayisi: " + str(num_gecerli_siz_fazlalik) + "\n")
    print("itirazli-itirazsiz gecerli oy toplaminin, gecerli oy sayisinin altinda kaldigi "+\
          "sandiklardaki buharlasan oy: " + str(gecerli_siz_eksiklik))
    print("bu durumun karsilasildigi sandik sayisi: " + str(num_gecerli_siz_eksiklik) + "\n")
    print("gecerli-gecersiz oy toplaminin, kullanilan oy sayisini astigi sandiklardaki "+\
          "fazlalik oylar toplami: " + str(gecerli_siz_fazlalik))
    print("bu durumun karsilasildigi sandik sayisi: " + str(num_gecerli_siz_fazlalik) + "\n")
    print("gecerli-gecersiz oy toplaminin, kullanilan oy sayisinin altinda kaldigi "+\
          "sandiklardaki buharlasan oy: " + str(gecerli_siz_eksiklik))
    print("bu durumun karsilasildigi sandik sayisi: " + str(num_gecerli_siz_eksiklik) + "\n")
    print("kayit-fazlasi secmenden gelen fazlalik oy: " + str(extras))
    print("bu durumun karsilasildigi sandik sayisi: " + str(num_extras) + "\n")
    print("parti oylari toplaminin gecerli oy sayisini astigi sandiklardaki "+\
          "fazlalik oy: " + str(fazlalik))
    print("bu durumun karsilasildigi sandik sayisi: " + str(num_fazlalik) + "\n")
    print("parti oylari toplaminin gecerli oy sayisinin altinda kaldigi "+\
          "sandiklardaki buharlasan oy: " + str(eksiklik))
    print("bu durumun karsilasildigi sandik sayisi: " + str(num_eksiklik) + "\n")
#    print("STS'deki \"Partilerin Toplam Oyu\" bilgisin gecerli oy sayisini astigi sandiklardaki "+\
#          "toplam oy farki: " + str(sts_total_fazlalik))
#    print("bu durumun karsilasildigi sandik sayisi: " + str(num_sts_total_fazlalik) + "\n")
#    print("STS'deki \"Partilerin Toplam Oyu\" bilgisin gecerli oy sayisinin altinda kaldigi "+\
#          "sandiklardaki toplam oy farki: " + str(sts_total_eksiklik))
#    print("bu durumun karsilasildigi sandik sayisi: " + str(num_sts_total_eksiklik) + "\n")

    print("bilgisi sts'de olmayan sandik sayisi: " + str(data_not_present_in_sts))
    print("bilgisi sts'de olan sandik sayisi: " + str(data_present_in_sts) + "\n")


if __name__ == '__main__':
    main()
