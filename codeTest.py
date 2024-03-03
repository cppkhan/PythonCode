import csv
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def save_results_to_csv(results):
    with open('election_results.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Question', 'Response'])
        writer.writerows(results)

def get_input(response):
    response[0] = input("Enter Start:").lower()

# Function to press the start button
def press_start_button(driver, response):
    start_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'button--big'))
    )
    threading.Thread(target=get_input, args=(response,)).start()

    while not response[0] or response[0] not in {'start'}:
        pass  # Wait for user input

    start_button.click()
    # Navigate and answer questions
    results = navigate_and_answer_questions(driver)
    # Save results to CSV
    save_results_to_csv(results)

# Function to navigate through questions and record answers
def navigate_and_answer_questions(driver):
    results = []

    # Wait for the question elements to appear
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'theses__box-inner')))
    
    # Find total number of questions
    total_questions = len(driver.find_elements(By.CLASS_NAME, 'theses__box-inner'))
    print("Total Questions:", total_questions)
    current_question_index = 0
    while current_question_index < total_questions:
        # Find all question elements
        question_elements = driver.find_elements(By.CLASS_NAME, 'theses__box-inner')
        question_element = question_elements[current_question_index]

        # Use BeautifulSoup to extract question text
        question_text = question_element.find_element(By.CLASS_NAME, 'theses__text').text
        print("Question:", question_text)

        # Get available options for the current question
        options_elements = question_element.find_elements(By.CLASS_NAME, 'theses-btn')
        
        # Ask user for response
        while True:
            response = input("Enter your response (ich stimme zu/neutral/ich stimme nicht zu): ").lower()
            if response in {"ich stimme zu", "neutral", "ich stimme nicht zu"}:
                break
            print("Invalid response. Please enter 'ich stimme zu', 'ich stimme nicht zu', or 'neutral'.")
        
        # Select radio button based on user response
        if response == "ich stimme zu":
            options_elements[0].click()
        elif response == "neutral":
            options_elements[1].click()
        elif response == "ich stimme nicht zu":
            options_elements[2].click()
        
        # Save question and response
        results.append([question_text, response])
        # Move to next question
        current_question_index += 1

    return results

# Main function
def main():
    # Open the URL with Selenium
    url = "https://www.wahl-o-mat.de/bundestagswahl2021/app/main_app.html"
    driver = webdriver.Chrome()  
    driver.get(url)

    response = [None]  # A list to hold the user input asynchronously
    # Press the start button
    press_start_button(driver, response)

    # Close the browser
    driver.quit()

if __name__ == "__main__":
    main()
