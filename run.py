from human_input import HumanLikeInput

# for tests
import time

# text = "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et"
text = "Hello, World! This is a human-like typing"

def run():
    input_handler = HumanLikeInput()
    try:
        print("waiting for open any text field 3 seconds...")
        time.sleep(3) 
        input_handler.type_text(text)
    finally:
        input_handler.disconnect()

if __name__ == "__main__":
    run()