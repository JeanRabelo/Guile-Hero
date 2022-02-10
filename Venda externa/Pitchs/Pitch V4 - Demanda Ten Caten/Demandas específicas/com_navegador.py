# -*- coding: utf-8 -*-
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class AppDynamicsJob(unittest.TestCase):
    def setUp(self):
        # AppDynamics will automatically override this web driver
        # as documented in https://docs.appdynamics.com/display/PRO44/Write+Your+First+Script
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.google.com/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_app_dynamics_job(self):
        driver = self.driver
        driver.get("http://inter04.tse.jus.br/ords/eletse/f?p=111:1::PESQUISAR:NO:::")
        driver.find_element_by_id("P1_UF").click()
        Select(driver.find_element_by_id("P1_UF")).select_by_visible_text("PA")
        driver.find_element_by_id("P1_MUN").click()
        Select(driver.find_element_by_id("P1_MUN")).select_by_visible_text(u"MARABÁ")
        driver.find_element_by_id("P1_ZONA").click()
        Select(driver.find_element_by_id("P1_ZONA")).select_by_visible_text("0023")
        driver.find_element_by_id("P1_SECAO").click()
        Select(driver.find_element_by_id("P1_SECAO")).select_by_visible_text("0051")
        driver.find_element_by_xpath("//button[@id='PESQUISAR']/span[2]").click()

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True

    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True

    def tearDown(self):
        # To know more about the difference between verify and assert,
        # visit https://www.seleniumhq.org/docs/06_test_design_considerations.jsp#validating-results
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
