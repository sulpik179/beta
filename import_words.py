from db_manager import Database


def main():
    #csv_path = 'csv/add.csv'
    csv_path = 'csv/words.csv'
    db = Database()
    db.add_words_from_csv(csv_path)
    print('Загрузка завершена')
    db.close()


if __name__ == '__main__':
    main()