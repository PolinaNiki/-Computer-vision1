import time
import pyautogui as gui
import cv2
import mss
import numpy as np

# Переменные улучшения изображений
IMPROVE_THRESH_TYPE = cv2.THRESH_BINARY
IMPROVE_THRESH_LOWER = 127
IMPROVE_THRESH_UPPER = 255
IMPROVE_EROSION_KERNEL = np.ones((3, 3))
IMPROVE_EROSION_ITERATIONS = 1
IMPROVE_DILATION_KERNEL = np.ones((3, 3))
IMPROVE_DILATION_ITERATIONS = 1


def improve(image):
    """Бинаризация и улучшение изображения перед считыванием"""

    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    _, binary = cv2.threshold(image, IMPROVE_THRESH_LOWER,
                              IMPROVE_THRESH_UPPER, IMPROVE_THRESH_TYPE)

    binary = cv2.dilate(binary,
                        IMPROVE_EROSION_KERNEL,
                        iterations=IMPROVE_DILATION_ITERATIONS)
    result = cv2.erode(binary,
                       IMPROVE_DILATION_KERNEL,
                       iterations=IMPROVE_EROSION_ITERATIONS).astype(np.uint8)

    return result


def dino_start():
    """Запуск игры"""

    gui.press('enter')


def dino_jump():
    """Прыжок"""

    gui.press('space')


def dino_duck(trigger):
    """Наклон/падение динозавра"""

    if trigger:
        gui.keyDown('down')
    else:
        gui.keyUp('down')


def get_area(img, area):
    """Получение зоны из массива для проверки"""

    return img[area["p1"][1]:area["p2"][1] + 1,
               area["p1"][0]:area["p2"][0] + 1]


def check_area(out_img, area):
    """Проверка зоны на наличие объектов с отрисовкой на экран"""

    found = False
    if 0 in area["line"]:
        area["color"] = (0, 0, 255)
        found = True
    else:
        area["color"] = (0, 255, 255)
        found = False
    cv2.rectangle(out_img, area["p1"], area["p2"], area["color"], thickness=2)

    return found


def main():
    """Главная функция"""

    # Кнопки и их состояния
    buttons = {"up": "idle", "down": "idle", "enter": "idle"}

    # Ближняя зона спереди
    close = {
        "p1": (60, 120),
        "p2": (150, 120),
        "line": np.empty(1),
        "color": (0, 255, 255),
        "check": False
    }

    # Отдалённая зона спереди
    medium = {
        "p1": (151, 120),
        "p2": (240, 120),
        "line": np.empty(1),
        "color": (0, 255, 255),
        "check": False
    }

    # Дальняя зона спереди
    far = {
        "p1": (375, 120),
        "p2": (450, 120),
        "line": np.empty(1),
        "color": (0, 255, 255),
        "check": False
    }

    # Зона под динозавром
    under = {
        "p1": (45, 135),
        "p2": (45, 160),
        "line": np.empty(1),
        "color": (0, 255, 255),
        "check": False
    }

    # Зона над динозавром
    top = {
        "p1": (0, 80),
        "p2": (200, 95),
        "line": np.empty(1),
        "color": (0, 255, 255),
        "check": False
    }

    # Зона позади динозавра
    behind = {
        "p1": (0, 120),
        "p2": (30, 120),
        "line": np.empty(1),
        "color": (0, 255, 255),
        "check": False
    }

    # Зоны проверки на проигрыш
    gameover_1 = {
        "p1": (290, 85),
        "p2": (310, 90),
        "line": np.empty(1),
        "color": (0, 255, 255),
        "check": False
    }
    gameover_2 = {
        "p1": (200, 50),
        "p2": (400, 60),
        "line": np.empty(1),
        "color": (0, 255, 255),
        "check": False
    }

    with mss.mss() as sct:
        gui.FAILSAFE = False

        dino_area = {"top": 180, "left": 0, "width": 600, "height": 160}

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter("dino.mp4", fourcc, 2, (600, 160))

        while "Screen capturing":
            # Рассчёт времени для вывода кол-ва кадров в секунду
            last_time = time.time()

            # Получение изображения и бинаризация
            img = np.array(sct.grab(dino_area))
            img = improve(img)

            # Получение разницы во времени
            delta = (time.time() - last_time)

            # Получение зон для проверки
            close["line"] = get_area(img, close)
            top["line"] = get_area(img, top)
            under["line"] = get_area(img, under)
            behind["line"] = get_area(img, behind)
            medium["line"] = get_area(img, medium)
            far["line"] = get_area(img, far)
            gameover_1["line"] = get_area(img, gameover_1)
            gameover_2["line"] = get_area(img, gameover_2)

            # Создание кадра для вывода
            out_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR).astype(np.uint8)

            # Вывод фреймрейта
            if delta != 0:
                fps = str(round(1 / delta))
                # print("fps: " + fps)

                cv2.putText(out_img, "fps: " + fps, (10, 20),
                            cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1,
                            cv2.LINE_AA)

            # Проверка зон на наличие объектов
            top["check"] = check_area(out_img, top)
            close["check"] = check_area(out_img, close)
            under["check"] = check_area(out_img, under)
            behind["check"] = check_area(out_img, behind)
            medium["check"] = check_area(out_img, medium)
            far["check"] = check_area(out_img, far)
            gameover_1["check"] = check_area(out_img, gameover_1)
            gameover_2["check"] = check_area(out_img, gameover_2)

            # Проверка на проигрыш
            if gameover_1["check"] and gameover_2["check"]:
                if buttons["down"] != "idle":
                    dino_duck(False)
                    buttons["down"] = "idle"
                    print("unduck!")
                if buttons["enter"] != "active":
                    buttons["enter"] = "active"
                    dino_start()
                    print("start!")
            else:
                if buttons["enter"] != "idle":
                    buttons["enter"] = "idle"

                if under["check"]:
                    if buttons["up"] != "idle":
                        buttons["up"] = "idle"
                    if top["check"]:
                        if not close["check"]:
                            if buttons["down"] != "active":
                                dino_duck(True)
                                buttons["down"] = "active"
                                print("duck!")
                    else:
                        if buttons["down"] != "idle":
                            dino_duck(False)
                            buttons["down"] = "idle"
                            print("unduck!")
                else:
                    if behind["check"]:
                        if not close["check"]:
                            if buttons["down"] != "active":
                                dino_duck(True)
                                buttons["down"] = "active"
                                print("duck!")
                if close["check"]:
                    if buttons["up"] != "active":
                        dino_jump()
                        buttons["up"] = "active"
                        print("jump!")
                else:
                    if medium["check"]:
                        if far["check"]:
                            if buttons["up"] != "active":
                                dino_jump()
                                buttons["up"] = "active"
                                print("pre-jump!")

            # Вывод состояний кнопок
            cv2.putText(out_img,
                        "up: " + buttons["up"] + "   down: " + buttons["down"],
                        (100, 20), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1,
                        cv2.LINE_AA)

            # Вывод и запись
            out.write(out_img)
            cv2.imshow("Dino capture", out_img)

            # Выход из программы
            if cv2.waitKey(25) & 0xFF == ord("q"):
                out.release()
                cv2.destroyAllWindows()
                break

        out.release()


if __name__ == "__main__":
    main()