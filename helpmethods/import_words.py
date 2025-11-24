from db_manage import Database


def main():
    csv_path = 'csv/o.csv'
    db = Database()
    db.add_words_from_csv(csv_path)
    print('The download is completed')
    db.close()


if __name__ == '__main__':
    main()