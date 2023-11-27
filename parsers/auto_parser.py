from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from parsers.objects import AUTO_CLASSES, AUTO_FEATURES_DICT, WEBDRIVER_OPTIONS, WEBDRIVER_EX_OPTIONS, BUTTON_TEXT
from parsers.parser_utils import time_calc
from config_data.config import Config, load_config
import csv
import re

config: Config = load_config()

# Парсер Авто


class AutoParser:
    def __init__(self) -> None:
        options = Options()
        for option in WEBDRIVER_OPTIONS.get('options_list'):
            options.add_argument(option)
        for option in WEBDRIVER_EX_OPTIONS.keys():
            options.add_experimental_option(option, WEBDRIVER_EX_OPTIONS[option])
        self.driver = webdriver.Remote(
            "http://"
            + config.webdriver_config.host
            + ":"
            + config.webdriver_config.port
            + "/wd/hub",
            options=options,
        )
        self.driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )
        self.wait = WebDriverWait(self.driver, 120)

    async def quit_webdriver(self) -> None: # Отключение вебдрайвера
        self.driver.close()
        self.driver.quit()

    async def set_price(self, feature, locator) -> None:  # Установка значения цены
        if feature != "skip":
            self.wait.until(
                ec.presence_of_element_located((By.CLASS_NAME, AUTO_CLASSES["price"]))
            )
            price_class = self.driver.find_elements(
                By.CLASS_NAME, AUTO_CLASSES["price"]
            )
            if locator == 2:
                ActionChains(self.driver).move_to_element(price_class[locator]).click(
                    price_class[locator]
                ).send_keys(feature).perform()
            else:
                ActionChains(self.driver).move_to_element(price_class[locator]).click(
                    price_class[locator]
                ).send_keys(feature).perform()

    async def set_year_mileage(self, feature, locator) -> None: # Установка значения года/пробега
        if feature != "skip":
            self.wait.until(
                ec.presence_of_element_located((By.CLASS_NAME, AUTO_CLASSES["year"]))
            )
            year_mileage = self.driver.find_elements(
                By.CLASS_NAME, AUTO_CLASSES["year"]
            )
            ActionChains(self.driver).move_to_element(year_mileage[locator]).click(
                year_mileage[locator]
            ).send_keys(feature).perform()

    async def set_engine(self, feature) -> None:  # Установка значения типа двигателя
        gear_engine_list = AUTO_FEATURES_DICT.get("gear_engine_list")
        self.wait.until(
            ec.presence_of_element_located((By.CLASS_NAME, AUTO_CLASSES["expand"]))
        )
        expand = self.driver.find_element(By.CLASS_NAME, AUTO_CLASSES["expand"])
        ActionChains(self.driver).move_to_element(expand).click(expand).perform()
        self.wait.until(
            ec.presence_of_element_located((By.CLASS_NAME, AUTO_CLASSES["checkbox"]))
        )
        checkboxes = self.driver.find_elements(By.CLASS_NAME, AUTO_CLASSES["checkbox"])
        if feature != "skip":
            ActionChains(self.driver).move_to_element(
                checkboxes[gear_engine_list.index(feature)]
            ).click(checkboxes[gear_engine_list.index(feature)]).perform()

    async def set_gear(self, feature) -> None:  # Установка значения типа привода
        if feature != "skip":
            gear_engine_list = AUTO_FEATURES_DICT.get("gear_engine_list")
            checkboxes = self.driver.find_elements(
                By.CLASS_NAME, AUTO_CLASSES["checkbox"]
            )
            ActionChains(self.driver).move_to_element(
                checkboxes[gear_engine_list.index(feature)]
            ).click(checkboxes[gear_engine_list.index(feature)]).perform()

    async def set_transmission(self, feature) -> None:  # Установка значения типа КПП
        transmission_list = AUTO_FEATURES_DICT.get("transmission_list")
        self.wait.until(
            ec.presence_of_element_located(
                (By.CLASS_NAME, AUTO_CLASSES["transmission"])
            )
        )
        transmission_field = self.driver.find_elements(
            By.CLASS_NAME, AUTO_CLASSES["transmission"]
        )[4]
        ActionChains(self.driver).scroll_by_amount(0, 600).move_to_element(
            transmission_field
        ).click(transmission_field).perform()
        self.wait.until(
            ec.presence_of_element_located(
                (By.CLASS_NAME, AUTO_CLASSES["transmission_list"])
            )
        )
        ActionChains(self.driver).move_to_element(transmission_field).click(
            transmission_field
        ).perform()
        self.wait.until(
            ec.presence_of_element_located(
                (By.CLASS_NAME, AUTO_CLASSES["transmission_list"])
            )
        )
        transmission_value = self.driver.find_elements(
            By.CLASS_NAME, AUTO_CLASSES["transmission_list"]
        )
        if feature != "skip":
            ActionChains(self.driver).move_to_element(
                transmission_value[transmission_list.index(feature)]
            ).click(transmission_value[transmission_list.index(feature)]).perform()

    async def find_clicker(self, link_items) -> str:  # Установка значения города поиска
        self.wait.until(
            ec.presence_of_element_located((By.CLASS_NAME, AUTO_CLASSES["location"]))
        )
        location = self.driver.find_element(By.CLASS_NAME, AUTO_CLASSES["location"])
        ActionChains(self.driver).click(location).perform()
        self.wait.until(
            ec.presence_of_element_located(
                (By.CLASS_NAME, AUTO_CLASSES["popup_clear_button"])
            )
        )
        self.wait.until(
            ec.presence_of_element_located(
                (By.CLASS_NAME, AUTO_CLASSES["popup_find_button"])
            )
        )
        popup_input_line = self.driver.find_element(
            By.CLASS_NAME, AUTO_CLASSES["popup_input_line"]
        )
        ActionChains(self.driver).move_to_element(popup_input_line).click(
            popup_input_line
        ).key_down(Keys.CONTROL).send_keys("A").key_up(Keys.CONTROL).send_keys(
            link_items.get("geo")
        ).perform()
        self.wait.until(
            ec.presence_of_element_located(
                (By.CLASS_NAME, AUTO_CLASSES["popup_selected_region"])
            )
        )
        selected_region = self.driver.find_element(
            By.CLASS_NAME, AUTO_CLASSES["popup_selected_region"]
        )
        button = self.driver.find_element(
            By.CLASS_NAME, AUTO_CLASSES["popup_find_button"]
        )
        if button.text not in BUTTON_TEXT:
            ActionChains(self.driver).move_to_element(selected_region).click(
                selected_region
            ).click(button).perform()
            self.wait.until(
                ec.presence_of_element_located(
                    (By.CLASS_NAME, AUTO_CLASSES["find_button"])
                )
            )
            return re.sub(
                r"\?radius.*",
                "?localPriority=1&radius="
                + link_items.get("radius")
                + "&searchRadius="
                + link_items.get("radius"),
                self.driver.current_url,
            )
        await self.quit_webdriver()
        return "no-results"

    async def url_master(self, link_items) -> None | bool:  # Генератор начальной ссылки
        url = "https://www.avito.ru/all/avtomobili/"
        if link_items.get("mark") != "skip":
            url = url + link_items.get("mark").replace(" ", "_")
        if link_items.get("model") != "skip":
            url = (
                url
                + "/"
                + link_items.get("model")
                .replace(" ", "_")
                .replace("серия", "seriya")
                .replace("класс", "class")
            )
        try:
            self.driver.get(url)
        except TimeoutException:
            self.driver.execute_script("window.stop();")
        if "404" not in self.driver.title:
            return True
        await self.quit_webdriver()

    async def data_analyse(self, url) -> tuple[int, int] | str:  # Анализ количества объявлений, подсчёт времени
        self.driver.get(url)
        if "404" in self.driver.title:
            return "no-results"
        self.wait.until(
            ec.presence_of_element_located((By.CLASS_NAME, AUTO_CLASSES["find_button"]))
        )
        try:
            self.driver.find_element(By.CLASS_NAME, AUTO_CLASSES["no_results"])
            return "no-results"
        except NoSuchElementException:
            self.wait.until(
                ec.presence_of_element_located(
                    (By.CLASS_NAME, AUTO_CLASSES["ads_number"])
                )
            )
            # Общее количество объявлений
            ads_number = int(
                "".join(
                    self.driver.find_elements(
                        By.CLASS_NAME, AUTO_CLASSES["ads_number"]
                    )[0].text.split()
                )
            )
            return ads_number, await time_calc(ads_number)

    async def data_parse(self, url, telegram_id, ads_number) -> str:  # Парсинг объявлений
        ad_attributes = AUTO_FEATURES_DICT.get("ad_attributes")
        ad_info = {ad_attributes[i]: "" for i in range(len(ad_attributes))}
        pages_number = int(ads_number) // 50 + 1
        filename = f"{telegram_id}" + ".csv"
        with open(filename, "a+", encoding="utf-8") as csvfile:
            csvfile.truncate(0)
            writer = csv.DictWriter(csvfile, fieldnames=ad_attributes, delimiter=";")
            writer.writeheader()
            for i in range(pages_number):
                self.wait.until(
                    ec.presence_of_element_located((By.CLASS_NAME, AUTO_CLASSES["ads"]))
                )
                elements_by_class_name = self.driver.find_elements(
                    By.CLASS_NAME, AUTO_CLASSES["ads"]
                )[0]
                self.wait.until(
                    ec.presence_of_element_located((By.CLASS_NAME, AUTO_CLASSES["ad"]))
                )
                adverts = elements_by_class_name.find_elements(
                    By.CLASS_NAME, AUTO_CLASSES["ad"]
                )
                for ad in adverts:
                    link = ad.find_element(By.TAG_NAME, "a").get_attribute("href")
                    ad_info["link"] = (
                        "https://www.avito.ru/" + link[link.rfind("_") + 1 :]
                    )
                    price = ad.find_element(By.TAG_NAME, "p").text
                    try:
                        ad_info["price"] = price[
                            re.search("от ", price).span()[1] : -2
                        ].replace(" ", "")
                    except AttributeError:
                        ad_info["price"] = price[:-2].replace(" ", "")
                    parameters = ad.find_element(By.TAG_NAME, "h3").text
                    info = parameters[: parameters.find(",")]
                    edited_parameters = info[: -(len(info[info.rfind(" ") :][1:]) + 1)]
                    ad_info["auto"] = edited_parameters[: edited_parameters.rfind(" ")]
                    ad_info["engine"] = edited_parameters[
                        edited_parameters.rfind(" ") + 1 :
                    ]
                    ad_info["transmission"] = info[info.rfind(" ") :][1:]
                    ad_info["year"] = parameters[parameters.find(",") + 2 :][0:4]
                    mileage = parameters[parameters.find(",") + 2 :][6:-3].replace(
                        " ", ""
                    )
                    try:
                        ad_info["mileage"] = mileage[
                            re.search("битый,", mileage).span()[1]:
                        ]
                    except AttributeError:
                        ad_info["mileage"] = mileage
                    try:
                        geo = ad.find_elements(By.CLASS_NAME, AUTO_CLASSES["geo"])[
                            0
                        ].text
                        try:
                            ad_info["geo"] = geo[
                                0 : re.search("до [0-9]", geo).span()[0]
                            ]
                        except AttributeError:
                            try:
                                ad_info["geo"] = geo[
                                    0 : re.search("от [0-9]", geo).span()[0]
                                ]
                            except AttributeError:
                                try:
                                    ad_info["geo"] = geo[
                                        0 : re.search("[0-9]", geo).span()[0]
                                    ]
                                except AttributeError:
                                    ad_info["geo"] = geo
                    except IndexError:
                        ad_info["geo"] = ""
                    try:
                        ad_info["date"] = ad.find_elements(
                            By.CLASS_NAME, AUTO_CLASSES["date"]
                        )[0].text
                    except IndexError:
                        ad_info["date"] = ""
                    try:
                        ad_info["description"] = ad.find_elements(
                            By.CLASS_NAME, AUTO_CLASSES["description"]
                        )[0].text
                    except IndexError:
                        ad_info["description"] = ""
                    writer.writerows([ad_info])
                if i + 1 < pages_number != 0:
                    self.driver.get(
                        url.replace("&radius", "&p=" + str(i + 1) + "&radius")
                    )
            csvfile.close()
        await self.quit_webdriver()
        return filename
