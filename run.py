from human_input import HumanLikeInput

# for tests
import time

TIME_TO_TYPE = 2.0

# text = "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et"
text = "Привет! Как дела?"

def run():
    input_handler = HumanLikeInput()
    try:
        print(f"waiting for open any text field {TIME_TO_TYPE} seconds...")
        time.sleep(TIME_TO_TYPE) 
        input_handler.type_text(text)
    finally:
        input_handler.disconnect()

if __name__ == "__main__":
    run()