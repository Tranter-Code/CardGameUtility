from app import CardGameApp
from utils.style import setup_style

if __name__ == "__main__": 
    setup_style(mode="system", theme="blue") #set global style for the app
    app = CardGameApp() #create and run the GUI app
    app.mainloop() #start the main event loop