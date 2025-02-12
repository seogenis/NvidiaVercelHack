import pyautogui
import time
import os


def control_browser(phrase):
    # Add small delay to give time to switch to Chrome
    time.sleep(2)

    # Type the phrase
    pyautogui.write(phrase)

    pyautogui.press("enter")


def should_press_dbg():
    try:
        # take a screenshot
        a = pyautogui.locateOnScreen("fixv0.png")
        b = pyautogui.center(a)
        pyautogui.click(pyautogui.Point(b.x / 2, b.y / 2))
        print("a: ", a)
        print("b: ", b)
        time.sleep(30)
        should_press_fullscreen()
    except Exception as e:
        print("dbg block error")
        print(f"Error: {e}")
        time.sleep(3)
        should_press_fullscreen()


def should_press_fullscreen():
    try:
        # take a screenshot
        a = pyautogui.locateOnScreen("fullscreen.png")
        b = pyautogui.center(a)
        pyautogui.click(pyautogui.Point(b.x / 2, b.y / 2))
        print("a: ", a)
        print("b: ", b) 
        time.sleep(1)
        pyautogui.press("enter") #exits fullscreen
    except Exception as e:
        print("fullscreen block error")
        print(f"Error: {e}")


def vzero(prompt):
    # press escape
    user_phrase = (
        "Please make a interactive webpage to supplement the lesson based on the instructions "
        + prompt
        + " -- keep it relatively simple, it should look like a presentation slide, but be a react component"
    )
    control_browser(user_phrase)
    time.sleep(25)
    should_press_dbg()


if __name__ == "__main__":
    os.system("open -a 'Google Chrome'")
    time.sleep(2)
    pyautogui.write("https://v0.dev")
    time.sleep(0.5)
    pyautogui.press("enter")
    time.sleep(0.5)
    vzero("Make a powerpoint slide about the history of the internet")
