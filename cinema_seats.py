import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class cinema_hack(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        #getting the browser navigation
        try:
            self.driver.get('https://eventbook.ro/hall/cinema-florin-piersic-cluj-napoca')
        except:
            raise 'website error'

    def test_hack(self):
        driver = self.driver
        try:
            html_elem = driver.find_element_by_tag_name('html')
            print('Found <%s> element with that class name!' % (html_elem.tag_name))
        except:
            print('Was not able to find an element with that name.')

        try:
            movie_button = driver.find_elements_by_css_selector('a[role="button"]')[1]
            movie_button.click()
        except:
            raise 'movie_button error'

        time.sleep(5)
        seats = [12611, 12612, 12613, 12614, 12569, 12570, 12526, 12527, 12528, 12529]
        # html_elem.send_keys(Keys.END)

        for seat in seats:
            seat_button = driver.find_element_by_css_selector('g[id="{}"]'.format(seat))
            seat_button.click()
            time.sleep(0.2)

        try:
            buy_tickets_button = WebDriverWait(driver, 10).until( EC.invisibility_of_element_located((By.CLASS_NAME, "button.btn.btn-danger")))
            print(buy_tickets_button)

            #buy_tickets_button.click()  #can't click cuz it's invisible/hidden
            """buy_tickets_button = WebDriverWait(driver, 10).until(EC.visibility_of())
            print(buy_tickets_button)"""
        except:
            raise 'buy_tickets_button not found'

        try:
            target = driver.find_element_by_css_selector("button.btn.btn-danger")
            actions = ActionChains(driver)
            actions.move_to_element(target)
            actions.perform()
            driver.execute_script("arguments[0].click();", target)
        except:
            raise 'button still hidden'

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main(verbosity=2)
