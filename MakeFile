start : 
	bin/python main.py

install :
	bin/pip install -r requirements.txt

init_db :
	bin/python main.py initdb

drop_db:
	rm -rf /tmp/alayatodo.db