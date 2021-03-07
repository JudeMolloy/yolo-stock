from app import app


from flask_script import Manager
manager = Manager(app)

from flask_migrate import MigrateCommand
manager.add_command('db', MigrateCommand)

from commands.update_tickers import UpdateTickersCommand
manager.add_command('update_tickers', UpdateTickersCommand)

if __name__ == '__main__':
	manager.run()