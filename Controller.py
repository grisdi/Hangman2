from tkinter import simpledialog

from GameTime import GameTime
from Model import Model
from View import View


class Controller:
    def __init__(self, db_name=None):
        self.__model = Model()
        self.__view = View(self, self.__model)
        if db_name is not None:
            self.__model.database = db_name
        self.__game_time = GameTime(self.__view.lbl_time)

    def main(self):
        self.__view.main()

    def btn_scoreboard_click(self):
        window = self.__view.create_scoareboard_window()
        data = self.__model.read_scores_data()
        self.__view.draw_scoreboard(window, data)

    def buttons_no_game(self):
        self.__view.btn_new['state'] = 'normal'
        self.__view.btn_cancel['state'] = 'disabled'
        self.__view.btn_send['state'] = 'disabled'
        self.__view.char_input.delete(0, 'end')  # Sisestuskast tühjaks  enne peab olema delete
        self.__view.char_input['state'] = 'disabled'  # Nüüd alles disabled, kui eelmisega vahetuses, ei tööta

    def buttons_to_game(self):
        self.__view.btn_new['state'] = 'disabled'
        self.__view.btn_cancel['state'] = 'normal'
        self.__view.btn_send['state'] = 'normal'
        self.__view.char_input['state'] = 'normal'
        self.__view.char_input.focus()

    def btn_new_click(self):
        self.buttons_to_game()
        self.__view.change_image(0)
        self.__model.setup_new_game()
        self.__view.lbl_result.config(text=self.__model.hidden_word)
        # self.__view.lbl_error.config(text="Vigased tähed" + self.__model.get_wrong_letters_string(), fg='black')
        self.__game_time.reset()
        self.__game_time.start()

    def btn_cancel_click(self):
        self.__model.setup_new_game()
        self.__view.change_image(len(self.__model.image_files)-1)
        self.__view.lbl_result.config(text=self.__model.hidden_word)
        self.__view.lbl_error.config(text="Vigased tähed ", fg='black')
        self.__game_time.stop()
        self.buttons_no_game()
        # self.btn_new_click()

    def btn_send_click(self):
        if self.__model.misses >= 11:
            self.btn_cancel_click()

        user_input = self.__view.char_input.get()
        if user_input not in self.__model.random_word:
            self.__model.check_user_input(user_input)
            self.__view.lbl_result.config(text=self.__model.hidden_word)
            self.__view.char_input.delete(0, 'end')
            self.__view.lbl_error.config(text=f"Vigased tähed: " + self.__model.get_wrong_letters_string(), fg='red')
            self.__view.change_image(self.__model.misses)
        else:
            self.__view.lbl_error.config(text=f"Vigased tähed", fg='black')
        # self.__view.lbl_error.config(text="Vigased tähed: " + self.__model.get_wrong_letters_string(), fg="red")

        if self.__model.hidden_word == self.__model.random_word:
            # self.btn_cancel_click()
            player_name= simpledialog.askstring("Mäng läbi!", "Sisesta oma nimi: ")
            if player_name:
                self.__model.save_score(player_name, self.__game_time.counter)
                return