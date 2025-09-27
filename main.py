import os

class Player:
    def __init__(self, name, starting_lp=8000):
        self.name = name
        self.lp = starting_lp
    
    def damage(self, value):
        self.lp = max(0, self.lp - value)
        clear_console()
    
    def heal(self, value):
        self.lp += value
        clear_console()

    def halve_lp(self):
        self.lp //= 2
        clear_console()

    def reset_lp(self, starting_lp=8000):
        self.lp = starting_lp
        clear_console()
    
    def __str__(self):
        return  f"{self.name}: {self.lp}"
    
class Game:
    def __init__(self):
        self.player1 = Player("Player 1")
        self.player2 = Player("Player 2")

    def show_state(self):
        print(self.player1)
        print(self.player2)

    def get_player(self, number):
        if number == 1:
            return self.player1
        elif number == 2:
            return self.player2
        else:
            return None

def clear_console():
    os.system("cls" if os.name == "nt" else "clear")

def main():
    # For now, just test in console
    game = Game()
    while True:
        print("\n--- Life Point Tracker ---")
        game.show_state()
        print("\nChoose an action:")
        print("1. Damage")
        print("2. Heal")
        print("3. Halve LP")
        print("4. Reset LP")
        print("5. Show State")
        print("0. Quit")

        choice = input("Action: ")
        if choice == "0":
            break
        elif choice in ["1", "2", "3", "4"]:
            player_num = int(input("Which player? (1 or 2): "))
            player = game.get_player(player_num)
            if not player:
                print("Invalid player.")
                continue
            
            if choice == "1":  # Damage
                value = int(input("Damage value: "))
                player.damage(value)
            elif choice == "2":  # Heal
                value = int(input("Heal value: "))
                player.heal(value)
            elif choice == "3":  # Halve
                player.halve_lp()
            elif choice == "4":  # Reset
                player.reset_lp()
        
        
        elif choice == "5":
            game.show_state()
        else:
            print("Invalid choice. Try again.")
    


if __name__ == "__main__":
    main()