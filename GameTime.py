"""
Ajaga manipuleemise jaoks
"""
import time


class GameTime:
    def __init__(self, lbl_time):
        self.__lbl_time = lbl_time
        self.__counter = 0  # Kui counter väärtus pannakse jooksma, siis see suureneb iga sekund.
        self.__running = False
        self.__start_time = time.time()

    def get_time_seconds(self):
        return int(time.time() - self.__start_time)

    @property
    def counter(self):
        return self.__counter

    def update(self):
        if self.__running:
            if self.__counter == 0:
                display = '00:00:00'
            else:
                display = time.strftime('%H:%M:%S', time.gmtime(self.__counter))

            self.__lbl_time['text'] = display
            self.__lbl_time.after(1000, self.update)  # 1000 on üks millisekund
            self.__counter += 1  # Suurendab labelit ühe sekundi võrra displayl

    def start(self):
        self.__running = True
        self.update()

    def stop(self):
        self.__running = False

    def reset(self):
        self.__counter = 0
        self.__lbl_time['text'] = '00:00:00'
