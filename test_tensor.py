import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

link = "https://yandex.ru/"

@pytest.fixture(scope="class")
def browser():
    print("\nstart browser for test..")
    browser = webdriver.Chrome()
    yield browser
    print("\nquit browser..")
    browser.quit()

class Test_01():
    def test_check_search_field(self, browser):
        '''Проверка таблицы с подсказками в поле поиска Yandex'''
        browser.get(link)
        # поиск элемента для ввода текста поиска
        search_field = browser.find_element_by_id("text")
        search_field.send_keys("Тензор")
        assert search_field is not None, "Отсутствует поле поиска"
        suggest_list = browser.find_element_by_class_name("mini-suggest__popup-content").find_elements_by_tag_name("li")        
        # если длина таблицы с подсказками = 0, от подсказок нет
        assert len(suggest_list) > 0, "Нет таблицы с подсказками"
        search_field.send_keys(Keys.ENTER)

    def test_link_to_tensor_5(self, browser):
        '''В первых 5 результатах test_check_search_field есть ссылка на tensor.ru'''
        # определим список с результатами поиска
        serp_list = browser.find_element_by_class_name("serp-list")
        serp_item = serp_list.find_elements_by_class_name("serp-item")
        link_theme_outer = serp_list.find_elements_by_class_name("link_theme_outer")
        link_5=False
        # в списке, в атрибутах href найдем строку tensor.ru
        for el in link_theme_outer[0:min(5, len(serp_item))]:
            if "tensor.ru" in el.get_attribute("href"):
                link_5 = True
        assert link_5, "Нет ссылки на tensor.ru в 5 результатах поиска Yandex"


class Test_02():
    def test_check_for_link_images(self, browser):
        '''Переход на ресурс Картинки https://yandex.ru/images/...'''
        browser.get(link)
        data_id_images = browser.find_element_by_css_selector('a[data-id="images"]')
        data_id_images_href = data_id_images.get_attribute("href")
        assert data_id_images_href is not None, "Отсутствует ссылка Картинки"
        # переход по ссылке в элементе Картинки
        browser.get(data_id_images_href)
        # сравним  ссылку с ожидаемым ресурсом
        assert data_id_images_href == 'https://yandex.ru/images/', f'{data_id_images_href} - неверная ссылка'

    def test_check_navigate_image(self, browser):
        ''' Проверка навигации картинок на https://yandex.ru/images/'''
        # клик по первой картинке
        list_cl_teaser_link = browser.find_elements_by_class_name("cl-teaser__link")
        list_cl_teaser_link[0].click()
        # первая картинка
        source_img_01 = browser.find_element_by_xpath('//img[@class="image__image"]').get_attribute("src")
        
        navigate_right = browser.find_element_by_class_name("cl-viewer-navigate__item_right")
        navigate_right.click()
        # вторая картинка
        source_img_02 = browser.find_element_by_xpath('//img[@class="image__image"]').get_attribute("src")

        navigate_left = browser.find_element_by_class_name("cl-viewer-navigate__item_left")
        navigate_left.click()
        #  третья картинка, она же должна быть первой
        source_img_03 = browser.find_element_by_xpath('//img[@class="image__image"]').get_attribute("src")

        assert source_img_01 == source_img_03, "Разные картинки"
            


