# 📟 MyPager.py
import os
import importlib
import time
import sys
import json
import requests

def type_out(text, delay=0.05):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def list_scripts(directory):
    return [f.replace('.py', '') for f in os.listdir(directory) if f.endswith('.py')]

def run_script(script_command):
    try:
        directory, script_name = script_command.split('.')
        module = importlib.import_module(f"{directory}.{script_name}")
        module.main()
    except ModuleNotFoundError:
        type_out(f"🚨 Script '{script_name}' not found in '{directory}'!")
    except AttributeError:
        type_out(f"🚨 Script '{script_name}' does not have a 'main' function!")

def show_menu():
    with open('data/show_menu.json', 'r', encoding='utf-8') as file:
        menu_options = json.load(file)['menu']
    
    type_out("📟 MyPager Menu:")
    for option in menu_options:
        type_out(f"{option['key']}️⃣  {option['description']}")

def load_commands():
    with open('commands.json', 'r', encoding='utf-8') as file:
        return json.load(file)

def load_auto_start():
    try:
        with open('data/auto_start.json', 'r', encoding='utf-8') as file:
            return json.load(file).get("auto_start", [])
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        type_out("🚨 Failed to decode 'data/auto_start.json'. Check the file format.")
        return []

def auto_start():
    auto_start_commands = load_auto_start()
    for command in auto_start_commands:
        type_out(f"⏩ Auto-starting {command}...")
        run_script(command)

def menu_mode():
    commands = load_commands()
    
    while True:
        try:
            show_menu()
            choice = input("Select an option or type a command: ").strip().lower()
            
            if choice in commands['menu']:
                script_command = commands['menu'][choice]
                if script_command == 'quit':
                    type_out("👋 Exiting MyPager. Goodbye! 🚀")
                    break
                run_script(script_command)
            else:
                found = False
                for command_type in ['run', 'install']:
                    if choice in commands[command_type]:
                        run_script(commands[command_type][choice])
                        found = True
                        break
                if not found:
                    type_out("🚨 Invalid option! Please select a valid number or command.")
        except KeyboardInterrupt:
            type_out("\n🚨 Detected Ctrl+C!")
            restart_choice = input("Do you want to restart the menu, reboot, or exit? (r/reboot/e): ").strip().lower()
            if restart_choice == 'e':
                type_out("👋 Exiting MyPager. Goodbye! 🚀")
                break
            elif restart_choice == 'reboot':
                type_out("🔄 Rebooting MyPager... 🚀")
                os.execv(sys.executable, ['python'] + sys.argv)

def direct_mode():
    if len(sys.argv) < 3:
        print("Usage: python MyPager.py [run|install] [script_name]")
        return
    
    command = sys.argv[1]
    script_name = sys.argv[2]
    
    if command == "run":
        run_script("run." + script_name)
    elif command == "install":
        run_script("install." + script_name)
    else:
        print("🚨 Unknown command! Use 'run' or 'install'.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        direct_mode()
    else:
        auto_start()
        menu_mode()
