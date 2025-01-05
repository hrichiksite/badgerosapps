import badger2040
import re

badger = badger2040.Badger2040()
display = badger.display

# Global variables
main_text = ""
input_mode = "morse"  # Default input mode

# Initialize Morse code mapping
morse_code_map = {
    'A': '.-',    'B': '-...',  'C': '-.-.',  'D': '-..',   'E': '.',
    'F': '..-.',  'G': '--.',   'H': '....',  'I': '..',    'J': '.---',
    'K': '-.-',   'L': '.-..',  'M': '--',    'N': '-.',    'O': '---',
    'P': '.--.',  'Q': '--.-',  'R': '.-.',   'S': '...',   'T': '-',
    'U': '..-',   'V': '...-',  'W': '.--',   'X': '-..-',  'Y': '-.--',
    'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
}

# Functions

def clear_display():
    display.set_pen(15)
    display.clear()
    display.update()

def display_text(text):
    display.set_pen(0)
    display.set_font("bitmap8")
    display.set_thickness(3)
    display.text(text, 10, 10, scale=2)
    #display.partial_update(0, 0, display.measure_text(text, 2) + 10, 32)
    display.update()


def reset_text():
    global main_text
    main_text = ""
    clear_display()
    display_text("Text Reset")

def switch_input_mode():
    global input_mode
    input_mode = "alphabet" if input_mode == "morse" else "morse"
    clear_display()
    display_text(f"Input: {input_mode}")

def append_dot():
    if input_mode == "morse" and len(re.sub(r'[^.-]', '', main_text)) < 5:
        update_main_text(".")

def append_dash():
    if input_mode == "morse" and len(re.sub(r'[^.-]', '', main_text)) < 5:
        update_main_text("-")

def convert_to_alphabet():
    temp_text = re.sub(r'[^.-]', '', main_text)
    for char, code in morse_code_map.items():
        if temp_text == code:
            update_main_text(char, replace=True)
            break

def update_main_text(new_content, replace=False):
    global main_text
    if replace:
        main_text = main_text[:-len(re.sub(r'[^.-]', '', main_text))] + new_content
    else:
        main_text += new_content
    display_text(main_text)

def display_help():
    clear_display()
    help_text = (
        "Commands:\n"
        "A - Dot\n"
        "B - Convert\n"
        "C - Dash\n"
        "Down - Switch Mode\n"
        "AB - Reset\n"
        "UP - Help\n"
    )
    display_text(help_text)

def handle_button_press():
    if badger.pressed(badger2040.BUTTON_C):
        append_dash()
        draw_interface()
    elif badger.pressed(badger2040.BUTTON_A) and badger.pressed(badger2040.BUTTON_B):
        reset_text()
        draw_interface()
    elif badger.pressed(badger2040.BUTTON_A):
        append_dot()
        draw_interface()
    elif badger.pressed(badger2040.BUTTON_B):
        convert_to_alphabet()
        draw_interface()
    elif badger.pressed(badger2040.BUTTON_DOWN):
        switch_input_mode()
        draw_interface()
    elif badger.pressed(badger2040.BUTTON_UP):
        display_help()
        draw_interface()
    

def draw_interface():
    clear_display()
    display_text(f"Mode: {input_mode}\n{main_text}")

def initialize_display():
    display.set_update_speed(badger2040.UPDATE_FAST)
    display.clear()
    display.update()
    display.set_update_speed(badger2040.UPDATE_TURBO)
    badger2040.system_speed(badger2040.SYSTEM_TURBO)
    clear_display()
    display_text("Ready")


def log_debug_message(message):
    print(f"DEBUG: {message}")

initialize_display()

while True:
    try:
        handle_button_press()
        

        log_debug_message(f"Current text: {main_text}, Mode: {input_mode}")

        #badger.sleep(0.1)
    except Exception as e:
        log_debug_message(f"Error encountered: {str(e)}")
        display_help()

