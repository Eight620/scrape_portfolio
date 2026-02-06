from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd # データ保存用

driver = webdriver.Chrome()
driver.implicitly_wait(10)
driver.get('https://books.toscrape.com/')

# Travelカテゴリへ移動
travel_link = driver.find_element(By.LINK_TEXT, 'Travel')
travel_link.click()

# 【重要】まずは「本の塊（記事枠）」を全部取得する
# 検証ツールで見ると <article class="product_pod"> が各本の枠です
books = driver.find_elements(By.CSS_SELECTOR, 'article.product_pod')

data_list = []

# 各本の枠のなかで、タイトルや価格を探す
for book in books:
    # book.find_element とすることで、その「枠内」だけを探せます
    
    # 1. タイトル取得
    # ※ .textだと長いタイトルが省略されることがあるので、title属性を取るのが確実です
    title_tag = book.find_element(By.CSS_SELECTOR, 'h3 a')
    title = title_tag.get_attribute('title') 
    
    # 2. 価格取得
    price_text = book.find_element(By.CSS_SELECTOR, '.price_color').text
    
    # 3. データ整形（ £54.23 → 54.23 ）
    # '£' を空文字に置換して、float(小数)に変換
    price = float(price_text.replace('£', ''))
    
    data = {
        'title': title,
        'price': price
    }
    data_list.append(data)

# 確認
print(data_list)

# Excel保存（Pandas）
df = pd.DataFrame(data_list)
df.to_excel('travel_books.xlsx', index=False)

driver.quit()