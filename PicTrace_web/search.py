import logging
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import SIMILARITY_THRESHOLD, MAX_ADDITIONAL_IMAGES, MAX_TOTAL_RECORDS, MAX_ADDITIONAL_SEARCHES_PER_IMAGE
from utils import get_ip_address, click_element_js
from image_matcher import ImageMatcher

def perform_additional_search(driver, query, matcher, data_list, record_counter, processed_ips, source_embedding):
    if not query:
        logging.warning("Empty query. Skipping additional search.")
        return
    if len(query) > 100:
        logging.warning(f"Query too long: {query[:100]}... Skipping.")
        return
    try:
        driver.get('https://yandex.ru/')
        wait = WebDriverWait(driver, 20)
        search_input = wait.until(EC.presence_of_element_located((By.NAME, "text")))
        search_input.clear()
        search_input.send_keys(query)
        search_input.submit()
        logging.info(f"Performed additional search for query: {query}")
        driver.save_screenshot(f'yandex_additional_search_{query[:50]}.png')
        time.sleep(3)
        items = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.serp-item")))
        logging.info(f"Found {len(items)} results for additional search for query: {query}")
        for item in items:
            try:
                link_element = item.find_element(By.CSS_SELECTOR, 'a.Link')
                site_link = link_element.get_attribute('href')
                if site_link:
                    ip_address = get_ip_address(site_link)
                    if ip_address and ip_address not in processed_ips:
                        processed_ips.add(ip_address)
                        response = requests.get(site_link, timeout=10)
                        soup = BeautifulSoup(response.content, 'html.parser')
                        img_tag = soup.find('img')
                        if img_tag and img_tag.get('src'):
                            img_url = requests.compat.urljoin(site_link, img_tag.get('src'))
                            comparison_embedding = matcher.download_and_process_image(img_url)
                            if comparison_embedding is not None:
                                similarity = matcher.compare_images(source_embedding, comparison_embedding)
                                if similarity > SIMILARITY_THRESHOLD:
                                    row_data = {
                                        'Query': query,
                                        'Site URL': site_link,
                                        'IP Address': ip_address,
                                        'Similarity': f"{similarity:.4f}"
                                    }
                                    data_list.append(row_data)
                                    record_counter[0] += 1
                                    logging.info(
                                        f"Added data from additional search: {site_link} (Similarity: {similarity:.4f})")
                                    if record_counter[0] >= MAX_TOTAL_RECORDS:
                                        return
            except Exception as e:
                logging.warning(f"Error processing additional result: {str(e)}")
                continue
    except Exception as e:
        logging.error(f"Error during additional search for query '{query}': {str(e)}")

def collect_similar_images(driver, wait, matcher, source_embedding, image_name, data_list, record_counter):
    try:
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            try:
                more_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "CbirSites-MoreButton")))
                click_element_js(driver, more_button)
                logging.info("Clicked 'See All' button on Yandex.")
                driver.save_screenshot('yandex_step_clicked_more.png')
                time.sleep(3)
            except Exception as e:
                logging.error(f"Failed to click 'See All' button: {str(e)}")
                break
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            time.sleep(2)
        items = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.CbirSites-Item")))
        logging.info(f"Found {len(items)} elements with class 'CbirSites-Item'")
        processed_ips = set()
        for idx, item in enumerate(items):
            try:
                img_element = item.find_element(By.TAG_NAME, 'img')
                thumbnail_url = img_element.get_attribute('src')
                site_link_element = item.find_element(By.CSS_SELECTOR, 'a.Link_view_outer.CbirSites-ItemDomain')
                site_link = site_link_element.get_attribute('href')
                logging.info(f"Processing item {idx + 1}/{len(items)}")
                logging.info(f"Thumbnail URL: {thumbnail_url}")
                logging.info(f"Site URL: {site_link}")
                similarity = 0.0
                row_data = {
                    'Source': 'Yandex',
                    'Image Name': image_name,
                    'Thumbnail URL': thumbnail_url,
                    'Site URL': site_link
                }
                if thumbnail_url and site_link:
                    comparison_embedding = matcher.download_and_process_image(thumbnail_url)
                    if comparison_embedding is not None:
                        similarity = matcher.compare_images(source_embedding, comparison_embedding)
                        row_data['Similarity'] = f"{similarity:.4f}"
                        logging.info(f"Similarity score: {similarity}")
                if similarity > SIMILARITY_THRESHOLD:
                    try:
                        driver.execute_script("window.open('');")
                        driver.switch_to.window(driver.window_handles[1])
                        driver.get(site_link)
                        wait_short = WebDriverWait(driver, WAIT_TIME)
                        wait_short.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
                        page_content = driver.page_source
                        soup = BeautifulSoup(page_content, 'html.parser')
                        publication_date = matcher.extract_publication_date(soup)
                        row_data['Publication Date'] = publication_date
                        footer_info = matcher.parse_footer(soup)
                        if 'menu_links' in footer_info:
                            for key, value in footer_info['menu_links'].items():
                                row_data[f'Footer Menu Link - {key}'] = value
                        if 'phone_numbers' in footer_info:
                            row_data['Footer Phone Numbers'] = '; '.join(footer_info['phone_numbers'])
                        if 'privacy_policy' in footer_info:
                            row_data['Footer Privacy Policy'] = footer_info['privacy_policy']
                        if 'public_offer' in footer_info:
                            row_data['Footer Public Offer'] = footer_info['public_offer']
                        if 'developer' in footer_info and footer_info['developer']:
                            row_data['Footer Developer Name'] = footer_info['developer'].get('name')
                            row_data['Footer Developer URL'] = footer_info['developer'].get('url')
                        additional_images = matcher.find_and_parse_images(soup, driver)
                        for i, img_info in enumerate(additional_images[:MAX_ADDITIONAL_IMAGES], 1):
                            row_data[f'Additional Image {i} Src'] = img_info.get('src')
                            row_data[f'Additional Image {i} Alt'] = img_info.get('alt')
                            row_data[f'Additional Image {i} Title'] = img_info.get('title')
                        footer_text = matcher.extract_footer_text(soup)
                        important_info = matcher.generate_important_info(footer_text)
                        row_data['Important Info'] = important_info

                        # Extracting Post Text and Forward From
                        post_text = ''
                        forward_from = ''
                        post_body = soup.find('div', class_='post-body')
                        if post_body:
                            post_text_element = post_body.find('div', class_='post-text')
                            if post_text_element:
                                post_text = post_text_element.get_text(separator=' ', strip=True)
                            forward_info = post_body.find('div', class_='post-from')
                            if forward_info:
                                forward_from = forward_info.get_text(strip=True).replace('Forward from: ', '')
                        row_data['Post Text'] = post_text
                        row_data['Forward From'] = forward_from

                        # Generate Title
                        title = matcher.generate_title(post_text)
                        row_data['Item Title'] = title

                        # Add IP Address
                        ip_address = get_ip_address(site_link)
                        row_data['IP Address'] = ip_address

                        data_list.append(row_data)
                        record_counter[0] += 1
                        logging.info(f"Added data for: {image_name} (Total records: {record_counter[0]})")

                        # Formulate Search Queries Based on Metadata
                        search_queries = []
                        if title:
                            search_queries.append(f'"{title}"')
                        if post_text:
                            search_queries.append(post_text)
                        if forward_from:
                            search_queries.append(forward_from)

                        # Limit the number of additional searches per image
                        additional_searches_done = 0
                        for query in search_queries:
                            if record_counter[0] >= MAX_TOTAL_RECORDS:
                                break
                            if additional_searches_done >= MAX_ADDITIONAL_SEARCHES_PER_IMAGE:
                                break
                            perform_additional_search(driver, query, matcher, data_list, record_counter, processed_ips,
                                                      source_embedding)
                            additional_searches_done += 1

                        if record_counter[0] >= MAX_TOTAL_RECORDS:
                            logging.info(f"Reached maximum number of records: {MAX_TOTAL_RECORDS}")
                            break
                    except Exception as e:
                        logging.error(f"Error processing high similarity link {site_link}: {str(e)}")
                    finally:
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
            except Exception as e:
                logging.error(f"Error processing item {idx + 1}: {str(e)}")
                continue
    except Exception as e:
        logging.error(f"Error collecting images: {str(e)}")
