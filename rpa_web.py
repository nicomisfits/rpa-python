# -*- coding: utf-8 -*-
# $Autor: Nicolás Lista $
# $Fecha de Creación: 27/05/2020 $
# Fecha de Modificación: 19/05/2021 $
from rpa_robot.rpa_tools import *

from os import listdir
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.ie.options import Options as IEOptions
from selenium.webdriver.common.action_chains import ActionChains

class Web:
    def __init__(self, url, timeout=20, browser="", headless="", retry=1):
        self.timeout = timeout
        self.retry = retry
        if not browser: self.browser = config["GENERAL"]["BROWSER"]
        else: self.browser = browser
        if "mozilla" in self.browser: self.options = FirefoxOptions()
        if "chrome" in self.browser: self.options = ChromeOptions()
        if "explorer" in self.browser: self.options = IEOptions()

        if not headless: self.options.headless = output["--headless"]
        else: self.options.headless = str_to_bool(headless)
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--start-maximized")
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--ignore-ssl-errors=yes')
        self.options.add_argument('--ignore-certificate-errors')
        if not "explorer" in self.browser:
            if "windows" in sistema: self.options.add_experimental_option('excludeSwitches', ['enable-logging'])

        flag_connect = False
        path_drivers = os.path.dirname(os.path.abspath(__file__))+"/drivers"

        try:
            for driver_file in listdir(path_drivers):
                if(not(driver_file.startswith(self.browser))):
                    continue
                try:
                    if "mozilla" in self.browser:
                        self.driver = webdriver.Firefox(executable_path=path_drivers + "/" + driver_file, options=self.options)
                    if "chrome" in self.browser:
                        self.driver = webdriver.Chrome(executable_path=path_drivers + "/" + driver_file, options=self.options)
                    if "explorer" in self.browser:
                        self.driver = webdriver.Ie(executable_path=path_drivers + "/" + driver_file, options=self.options)
                    flag_connect = True
                    print("Conectado con el driver: " + driver_file)
                    break
                except Exception:
                    continue
                if not flag_connect:
                    raise Exception("\nNo pudo conectarse con el driver de Selenium")
            self.driver.get(url)
        except Exception as error:
            print("ERROR EN CONSTRUCTOR: "+str(error))



    #print all the elements which exists
    def print_all_elements(self):
        elements = self.driver.find_elements_by_xpath("//*")
        print("Elementos de la pantalla = "+str(len(elements)))
        for el in elements:
            print(el.id + " - texto: " + el.text)

    # wait for the element disappearence
    def wait_invisibility(self, value="//*", timeout="", locator="XPATH"):
        if not timeout: timeout = self.timeout
        wait = WebDriverWait(self.driver, timeout)
        try:
            if 'XPATH' in locator :         wait.until(EC.invisibility_of_element((By.XPATH, value)))
            if 'ID' in locator:             wait.until(EC.invisibility_of_element((By.ID, value)))
            if 'CSS' in locator :           wait.until(EC.invisibility_of_element((By.CSS_SELECTOR, value)))
            if 'CLASS' in locator :         wait.until(EC.invisibility_of_element((By.CLASS_NAME, value)))
            if 'NAME' in locator :          wait.until(EC.invisibility_of_element((By.NAME, value)))
            if 'LINK' in locator :          wait.until(EC.invisibility_of_element((By.LINK_TEXT, value)))
            if 'PARTIAL_LINK' in locator :  wait.until(EC.invisibility_of_element((By.PARTIAL_LINK_TEXT, value)))
            if 'TAG' in locator :           wait.until(EC.invisibility_of_element((By.TAG_NAME, value)))
            return True;
        except TimeoutException as e:
            return False;

    #wait for the element appearence
    def wait_presence(self, value="//*", timeout="", locator="XPATH"):
        if not timeout: timeout = self.timeout
        wait = WebDriverWait(self.driver, timeout)
        try:
            if 'XPATH' in locator :         wait.until(EC.presence_of_element_located((By.XPATH, value)))
            if 'CSS' in locator :           wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, value)))
            if 'CLASS' in locator :         wait.until(EC.presence_of_element_located((By.CLASS_NAME, value)))
            if 'NAME' in locator :          wait.until(EC.presence_of_element_located((By.NAME, value)))
            if 'LINK' in locator :          wait.until(EC.presence_of_element_located((By.LINK_TEXT, value)))
            if 'PARTIAL_LINK' in locator :  wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, value)))
            if 'TAG' in locator :           wait.until(EC.presence_of_element_located((By.TAG_NAME, value)))
            return True;
        except TimeoutException as e:
            return False;

    #wait for the element to be clickable
    def wait_is_clickable(self, value="//*", timeout="", locator="XPATH"):
        if not timeout: timeout = self.timeout
        wait = WebDriverWait(self.driver, timeout)
        try:
            if 'XPATH' in locator :         wait.until(EC.element_to_be_clickable((By.XPATH, value)))
            if 'CSS' in locator :           wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, value)))
            if 'CLASS' in locator :         wait.until(EC.element_to_be_clickable((By.CLASS_NAME, value)))
            if 'NAME' in locator :          wait.until(EC.element_to_be_clickable((By.NAME, value)))
            if 'LINK' in locator :          wait.until(EC.element_to_be_clickable((By.LINK_TEXT, value)))
            if 'PARTIAL_LINK' in locator :  wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, value)))
            if 'TAG' in locator :           wait.until(EC.element_to_be_clickable((By.TAG_NAME, value)))
            return True;
        except TimeoutException as e:
            return False;

    # return WebElement
    def get_element(self, value='//*', locator='XPATH'):
        if 'XPATH' in locator :         return self.driver.find_element_by_xpath(value)
        if 'CSS' in locator :           return self.driver.find_element_by_css_selector(value)
        if 'ID' in locator :            return self.driver.find_element_by_id(value)
        if 'CLASS' in locator :         return self.driver.find_element_by_class_name(value)
        if 'NAME' in locator :          return self.driver.find_element_by_name(value)
        if 'LINK' in locator :          return self.driver.find_element_by_link_text(value)
        if 'PARTIAL_LINK' in locator :  return self.driver.find_element_by_partial_link_text(value)
        if 'TAG' in locator :           return self.driver.find_element_by_tag_name(value)

    # return array of WebElements
    def get_elements(self, value='//*', locator='XPATH'):
        if 'XPATH' in locator :         return self.driver.find_elements_by_xpath(value)
        if 'CSS' in locator :           return self.driver.find_elements_by_css_selector(value)
        if 'CLASS' in locator :         return self.driver.find_elements_by_class_name(value)
        if 'NAME' in locator :          return self.driver.find_elements_by_name(value)
        if 'LINK' in locator :          return self.driver.find_elements_by_link_text(value)
        if 'PARTIAL_LINK' in locator :  return self.driver.find_elements_by_partial_link_text(value)
        if 'TAG' in locator :           return self.driver.find_elements_by_tag_name(value)

    #scroll to an element
    def scroll_at_element(self, path):
        actions = ActionChains(self.driver)
        actions.move_to_element(self.get_element(path)).perform()

    #scroll at the top
    def scroll_bottom(self, path = ""):

        if path == "":
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        else:
            self.driver.execute_script("arguments[0].scrollTo(0, 999999);", self.wizard(path))

    # Scroll a distance
    def scroll_at(self, scroll=1000):
        self.driver.execute_script("window.scrollBy(0,"+str(scroll)+")")

    # Save a screenshot
    def screenshot(self, add_to_path="", add_to_file_name=""):
        sep = config["PATHS"]["SEPARATOR"]
        pathToEvidences = os.path.abspath(__file__+ sep + "..") + sep + add_to_path

        if add_to_file_name == "":
            add_to_file_name = os.path.dirname(sys.argv[0]).replace("/", "_")

        file_name = add_to_file_name
        file_name = file_name.replace(r":","_")
        file_name = file_name.replace(r".","_")
        file_name = file_name.replace(r"-","_")
        file_name = file_name.replace(r" ","_")
        file_name += ".png"
        path = pathToEvidences + sep + file_name
        print("Se guardo screenshot correctamente en: " + path)
        self.driver.save_screenshot(path)

    def screenshot_file(self, filename=""):

        if filename == "":
            path_file = Path(os.path.abspath(__file__)).parent
            filename = str(path_file) + path_begin + ".png"

        print("Se guardo screenshot en: " + filename)
        self.driver.save_screenshot(filename)

    #Close the browser
    def close_browser(self):
        self.driver.quit()

    def js_click(self, path, timeout="", retry=0):
        el = self.wizard(path, timeout, retry)
        self.driver.execute_script("arguments[0].click();", el)

    def js_set_value(self, path, value, timeout="", retry=0):
        el = self.wizard(path, timeout, retry)
        self.driver.execute_script("arguments[0].setAttribute('value', '" + value + "');", el)
        return el

    def latch_web_status(self, path_begin):
        path_file = Path(os.path.abspath(__file__)).parent
        self.html_to_file(str(path_file) + path_begin + ".html")
        self.driver.save_screenshot(str(path_file) + path_begin + ".png")

    def latch_error(self, log_txt=""):
        if log_txt: log(log_txt)
        self.latch_web_status("/general_output/error")

    def have_txt(self, txt, path="//html"):
        e_html = self.driver.find_elements_by_xpath(path)[0]
        html = e_html.get_attribute('innerHTML')
        if txt in html: return True
        else: return False


    def html_to_file(self, file_name):
        e_html = self.driver.find_elements_by_xpath("//html")[0]
        html = e_html.get_attribute('innerHTML')
        open(file_name,'w+').write(html)

    def change_window(self, pos):
        window_after = self.driver.window_handles[pos]
        window_activa = self.driver.switch_to.window(window_after)

    def open_windows(self):
        handles = self.driver.window_handles
        size = len(handles)
        return size

    def minimize_all_windows(self):
        for window in range(0,self.open_windows()):
            self.change_window(window)
            self.driver.minimize_window()

    def maximize_all_windows(self):
        for window in range(0,self.open_windows()):
            self.change_window(window)
            self.driver.maximize_window()

    def switch_iframe(self, pathFrame):
        self.wait_presence(pathFrame)
        self.driver.switch_to.frame(self.driver.find_element_by_xpath(pathFrame))

    def select_element_by_keyboard_by_attr_value(self, value, key="", attr="id"):
        cant_elementos = len(self.driver.find_elements_by_xpath("//*"))
        if not key: key = Keys.TAB
        element = self.driver.switch_to.active_element
        element_primer_attr = element.get_attribute(attr)
        if element_primer_attr == value: return element
        cont = 0
        while cont <= cant_elementos:
            actions = ActionChains(self.driver)
            actions = actions.send_keys(key)
            actions.perform()
            element = self.driver.switch_to.active_element
            el_attr = element.get_attribute(attr)
            cont+=1
            if el_attr == value: return element
            if element_primer_attr == el_attr: return None



    def wizards(self, path ,timeout="", retry=0):
        if not timeout: timeout = self.timeout
        if not retry: retry = self.retry
        retry_count = 0
        while retry_count <= retry:
            elements = []
            try:
                try:
                    self.wait_presence(path, timeout)
                except:
                    None

                try:
                    self.scroll_at_element(path)
                except:
                    None

                elements = self.get_elements(path)
                if len(elements)==0:
                    raise Exception("No se encontró el elemento: "+str(path))
                break
            except:
                None
            retry_count+=1
        if len(elements)==0:
            self.latch_error("path_on_error: " + path)
            raise Exception("No se encontró el elemento: "+str(path))
        else:
            return elements


    def wizard(self, path,timeout="", retry=0):
        element = self.wizards(path, timeout, retry)
        if len(element)==0:
            raise Exception("No se encontró el elemento")
        else:
            return element[0]
