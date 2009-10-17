test:
	cp testing/*.py ~/Sites/cgi-bin
	cp testing/*.html testing/*.php ~/Sites/testing

db:
	rm test.db
	sqlite3 test.db < testing.sql