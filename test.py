from vicleaners import cleaners



def main(text):
    ret = cleaners(text).do()
    print(ret)


if __name__ == '__main__':
    txt = '10cm 1km 1hz 1g 10 g 10 kg'
    main(txt)