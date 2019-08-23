from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
"""

NR_OF_MOVES = 500

browser = webdriver.Chrome((ChromeDriverManager().install()))
browser.get('https://play2048.co/')

try:
    html_elem = browser.find_element_by_tag_name('html')
    print('Found <%s> element with that class name!' % (html_elem.tag_name))
except:
    print('Was not able to find an element with that name.')

def game_loop():
    try_again_button = None
    game_nr = 0

    for i in range(NR_OF_MOVES):
        html_elem.send_keys(Keys.UP)
        html_elem.send_keys(Keys.RIGHT)
        html_elem.send_keys(Keys.DOWN)
        html_elem.send_keys(Keys.LEFT)

        #restart_button = browser.find_element_by_class_name('restart-button')
        try:
            try_again_button = browser.find_element_by_link_text('Try again')
        except:
            # pass because the game isn't finished
            pass # I just don't want the program to crash

        if try_again_button != None:
            #actual_score = browser.find_element_by_class_name('score-container')
            best_score = browser.find_element_by_class_name('best-container')
            #actual_score_int = int(actual_score.text)
            #best_score_int = int(best_score.text)
            game_nr += 1
            print(f'Game #{game_nr}: ' + best_score.text)

            try_again_button.click()
            try_again_button = None


game_loop()
browser.quit()

#--------------------------------------------------------------------
