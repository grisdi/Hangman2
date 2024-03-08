import glob
import sqlite3
import datetime

from Score import Score


class Model:
    def __init__(self):
        self.__database = 'databases/hangman_words_ee.db'  # Andmebaas
        #  pip install Pillow -- terminalis - vajalik piltidega majandamiseks
        self.__image_files = glob.glob('images/*.png')  # List mängupildid (vaikimisi paneb tähestikulises järjekorras
        self.__random_word = ''
        self.__inserted_letters = []
        self.__wrong_letters = []
        self.__misses = 0
        self.__correct_letters = []
        self.hidden_word = ""

    @property
    def random_word(self):
        return self.__random_word

    @property
    def inserted_letters(self):
        return self.__inserted_letters

    @property
    def wrong_letters(self):
        return self.__wrong_letters

    @property
    def misses(self):
        return self.__misses

    @property
    def correct_letters(self):
        return self.__correct_letters

    @property
    def database(self):
        return self.__database

    @property
    def image_files(self):
        return self.__image_files

    @database.setter
    def database(self, value):
        self.__database = value

    def read_scores_data(self):
        """ Ametlik dokumentatsioon tuleks teha igal meetodil, siis tuleb kommentaari see return
        Loeb andmebaasi edetabelis kõik kirjed
        :return:
        """
        connection = None
        try:
            connection = sqlite3.connect(self.__database)
            sql = 'SELECT * FROM scores ORDER BY seconds;'
            cursor = connection.execute(sql)
            data = cursor.fetchall()
            result = []
            for row in data:
                result.append(Score(row[1], row[2], row[3], row[4], row[5]))

            return result
        except sqlite3.Error as error:
            print(f'Viga ühenduda andmebaasi edetabelis {self.__database}: {error}')
        finally:
            if connection:
                connection.close()

    def setup_new_game(self):
        self.__random_word = self.get_random_word()
        print(self.__random_word)
        self.hidden_word = '_' * len(self.__random_word)
        self.__inserted_letters = []
        self.__wrong_letters = []
        self.__misses = 0
        self.__correct_letters = ['_' for _ in range(len(self.random_word))]

    def get_random_word(self):
        connection = None
        try:
            connection = sqlite3.connect(self.__database)
            cursor = connection.cursor()
            cursor.execute('SELECT word FROM words ORDER BY RANDOM() LIMIT 1')
            random_word = cursor.fetchone()[0]
            connection.close()
            # print("Valitud juhuslik sõna:", random_word)  # Lisage see rida, et kontrollida valitud sõna väärtust
            return random_word.upper()
        except sqlite3.Error as error:
            print(f'Viga andmebaasist sõna valimisel: {error}')
        finally:
            if connection:
                connection.close()

    def check_user_input(self, user_input):
        if user_input:
            guessed_letter = user_input[0].upper()
            if guessed_letter in self.__inserted_letters:
                self.__wrong_letters.append(guessed_letter)
                self.__misses += 1
            else:
                self.__inserted_letters.append(guessed_letter)
                correct_guesses = [i for i, char in enumerate(self.__random_word) if char == guessed_letter]
                for i in correct_guesses:
                    self.__correct_letters[i] = guessed_letter
                self.hidden_word = ''.join(guessed_letter if i in correct_guesses else char if char != '_'
                else '_' for i, char in enumerate(self.hidden_word))
            if guessed_letter not in self.__random_word:
                self.__wrong_letters.append(guessed_letter)
                self.__misses += 1

    def get_wrong_letters_string(self):
        # wrong_list = self.__wrong_letters
        # wrong_string = ', '.join(wrong_list)
        # return wrong_string
        return ' ,'.join(self.__wrong_letters)

    def save_score(self, player_name, time_counter):
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        player_name = player_name.strip()
        connection = None
        try:
            connection = sqlite3.connect(self.__database)
            cursor = connection.cursor()
            cursor.execute('INSERT INTO scores (name, word, missing, seconds, date_time) VALUES (?, ?, ?, ?, ?);',
                           (player_name, self.random_word,
                            self.get_wrong_letters_string(), time_counter, current_time))
            connection.commit()
        except sqlite3.Error as error:
            print(f"Viga andmebaasi salvestamisel: {error}")
        finally:
            if connection:
                connection.close()