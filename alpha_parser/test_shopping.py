from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotInteractableException


def amazon_search(driver, item_for_search):
    result = []
    driver.get("https://amazon.com")
    driver.find_element(By.ID, "twotabsearchtextbox").send_keys(item_for_search)
    driver.find_element(By.ID, "nav-search-submit-button").click()
    result_search = driver.find_elements(By.CSS_SELECTOR, 'div.s-result-item.s-asin.sg-col-0-of-12.sg-col-16-of-20'
                                                          '.sg-col.s-widget-spacing-small.sg-col-12-of-16')

    if result_search:
        for item in result_search:
            try:
                price = round(float(item.find_element(By.CLASS_NAME, 'a-price-whole').text))
                reviews = int(item.find_element(By.CSS_SELECTOR, 'span.a-size-base').text.replace(',', ''))
                result.append((price, reviews))
            except:
                continue

        amazon_result = max(result, key=lambda t: t[1])     # finding the most count of reviews
        return amazon_result[0]

    else:
        amazon_result = 0
        print("Amazon haven't same items")
        return amazon_result


def bestbuy_search(driver, item_for_search):
    logged_results = []
    driver.get("https://bestbuy.com")
    driver.find_element(By.CLASS_NAME, 'us-link').click()
    driver.find_element(By.CSS_SELECTOR, 'button.c-close-icon.c-modal-close-icon').click()
    while True:
        try:
            driver.find_element(By.XPATH, '//*[@id="gh-search-input"]').send_keys(item_for_search)
            driver.find_element(By.CLASS_NAME, 'header-search-button').click()
            break
        except ElementNotInteractableException:
            driver.implicitly_wait(1)

    driver.implicitly_wait(5)    # bestbuy have long loading
    result_search = driver.find_elements(By.CSS_SELECTOR, 'div.list-item.lv')

    if result_search:
        for i in result_search:
            try:
                div_price = i.find_element(By.CSS_SELECTOR, 'div.priceView-hero-price.priceView-customer-price')
                price = round(float(div_price.find_element(By.CSS_SELECTOR, 'span').text.replace('$', '')))
                reviews = int(i.find_element(By.CSS_SELECTOR, 'span.c-reviews-v4.c-reviews.order-2').text
                              .replace('(', '').replace(' ', '').replace(')', ''))
                logged_results.append((price, reviews))
            except:
                continue

        bestbuy_results = [i for i in logged_results if i[0] > int(logged_results[0][0] / 3)]
        bb_result = max(bestbuy_results, key=lambda t: t[1])    # finding the most count of reviews
        return bb_result[0]

    else:
        bb_result = 0
        print("Bestbuy haven't same items")
        return bb_result


def test_shopping():
    driver = webdriver.Chrome()
    item_for_search = 'Apple iPhone X'    #Apple iPhone XR, Black, 128GB
    amazon_price = amazon_search(driver, item_for_search)
    bestbuy_price = bestbuy_search(driver, item_for_search)
    assert amazon_price > bestbuy_price