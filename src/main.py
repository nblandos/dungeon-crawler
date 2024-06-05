from login_system import LoginSystem
from game import Game


def main():
    # Initialises the login system and the game once the user has logged in
    login_system = LoginSystem()
    if login_system.logged_in:

        game = Game(login_system.username.get())
        game.run()


if __name__ == "__main__":
    main()
