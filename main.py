import main_window as mw
import database as db
import dev as dev

# if you did not created database yet use dev.start() to put some fake data in to database
#db.create()

main = mw.Main_Window()
main.start()