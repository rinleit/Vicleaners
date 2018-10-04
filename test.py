from vicleaners import cleaners



def main(text):
    ret = cleaners(text).do()
    print(ret)


if __name__ == '__main__':
    txt = 'csgt cscđ trường thpt hà Trung pc14'
    main(txt)