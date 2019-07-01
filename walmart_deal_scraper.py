from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from secrets import dynamic_link
import time, pyperclip

# main driver
driver = webdriver.Chrome()
# goes to the initial link
driver.get(dynamic_link)


# locating the main products on the page
product_div = driver.find_element_by_id("searchProductResult")

# getting the list of all items in the page
ul = product_div.find_element_by_class_name("search-result-gridview-items")

# getting all list items that contain each item
li_items = ul.find_elements_by_class_name("Grid-col")

# counter for pagination used to check and update the link to navigate
page_counter = 0

item_counter = 0
for i in range(len(li_items[:1])):
  # getting inside the list item so I can get more data for each item
  li_inner = li_items[i].find_element_by_class_name("search-result-gridview-item")

  # getting the name 
  product_name = li_inner.find_element_by_class_name("product-title-link").get_attribute("title")

  # getting the item link to its details page
  product_link = li_inner.find_element_by_class_name("product-title-link").get_attribute("href")

  # getting the item price
  item_price = li_inner.find_element_by_class_name("price-group").get_attribute("aria-label")

  # # TWO WAYS TO DO THE SAME THING:
  # ## 1: I get the company name in this method by opening a new window which caused the connection to temporarily timeout
  # # creating another driver to bypass a stale element exception/issue
  # driver_two = webdriver.Chrome()
  # # navigating to the product's details page
  # driver_two.get(product_link)
  # # locating the area of the page for the company name for the product
  # # learned: to get the text in a span tag, you can jsut call the text method on the parent element
  # company_name = driver_two.find_element_by_class_name("prod-brandName").get_attribute('text')
  # # navigating back to the page with all other products and repeating process
  # driver_two.close()

  # ------------------------- TODO: generateTab func ---------------------------------------
  ## 2: I get the company name by opening a new tab in the same window, process is faster
  # opens a new empty tab
  driver.execute_script("window.open('');")
  time.sleep(.5)
  # Switches the driver focus to the new window
  driver.switch_to.window(driver.window_handles[1])
  # navigate to the prouct details page
  driver.get(product_link)
  time.sleep(.5)
  # locating the area of the page for the company name for the product and getting the company name
  try:
    # the try-atch is due to walmart sometimes not being able to load the product details page
    company_name = driver.find_element_by_class_name("prod-brandName").get_attribute('text')
  except:
    print("company name page bugged out")
    company_name = "couldn't find"
  # close the active tab
  driver.close()
  # Switch the focus back to the first tab
  driver.switch_to.window(driver.window_handles[0])
  time.sleep(.5)
  #---------------------------------------------------------------------------------------
  print(product_name, "\n", item_price, "\n", product_link, "\n", company_name, "\n------------")
  print(i, len(li_items[:1]))
  # hook to see if all items have been scraped on the page and use it to navigate to next page
  if i+1 == len(li_items[:1]):
    print("page 2")
    # incrementing the page number to match the links page number 
    page_counter = page_counter + 1
    # finding the page number and storing the index
    page_no = dynamic_link.find(str(page_counter), 245, 254)
    # creating the new link by replacing the (page=1) part of the link with my incremented counter
    # replacign the entire page=1 part because if I only do the number it will change other numbers as well
    next_page_link = dynamic_link.replace("page="+dynamic_link[page_no], "page="+str(page_counter+1))
    # navigating to next page
    driver.get(next_page_link)
  
  item_counter = item_counter + 1

# TODO 1: figure out navigation between pages by changing the (dynamic_link) imported from secrets - hz 07/01
# TODO 2: switch to another category when there is no more products to scrape in one category - hz 07/02
# TODO 3: figure out optimal way to modify the link and automate moving categories -hz
# TODO 4: Put all product data in a dictionary, the key should be number or name?
# TODO 4: turn code into componenets through functions (GENERAL GOAL)

driver.close()

