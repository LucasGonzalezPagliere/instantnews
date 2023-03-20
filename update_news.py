from server import update_news_data
import time

if __name__ == '__main__':
    update_news_data()  # Fetch and process news data initially
    print('News data updated')
    # Update news data every 2 hours (7200 seconds)
    while True:
        time.sleep(7200)
        update_news_data()