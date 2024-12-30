def search_yandex_image(driver, image_path, matcher, source_embedding, image_name, data_list, record_counter):
    try:
        driver.get('https://yandex.ru/images/')
        logging.info("Navigating to Yandex Images.")
        driver.save_screenshot('yandex_step_navigate.png')
        wait = WebDriverWait(driver, 20)
        try:
            consent_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Согласен')]")))
            consent_button.click()
            logging.info("Closed consent popup on Yandex.")
            driver.save_screenshot('yandex_step_closed_consent.png')
        except:
            logging.info("Consent popup on Yandex not found.")
            driver.save_screenshot('yandex_step_no_consent.png')
        try:
            upload_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
            upload_input.send_keys(os.path.abspath(image_path))
            logging.info(f"Uploaded image to Yandex: {image_path}")
            driver.save_screenshot('yandex_step_uploaded_image.png')
        except Exception as e:
            logging.error("Failed to find or interact with the upload field on Yandex.")
            driver.save_screenshot('yandex_step_upload_error.png')
            raise e
        time.sleep(5)
        try:
            popup_close = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "NeuroOnboarding-Close")))
            popup_close.click()
            logging.info("Closed popup on Yandex.")
            driver.save_screenshot('yandex_step_closed_popup.png')
        except:
            logging.info("Popup on Yandex not found or already closed.")
            driver.save_screenshot('yandex_step_no_popup.png')
        collect_similar_images(driver, wait, matcher, source_embedding, image_name, data_list, record_counter)
    except Exception as e:
        logging.error(f"Error searching on Yandex: {str(e)}")
        driver.save_screenshot('yandex_step_search_error.png')
