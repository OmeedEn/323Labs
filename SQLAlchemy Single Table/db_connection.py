"""
To get getpass to work properly in PyCharm, you need to configure your project:
Click on the Run Menu at the very top of your PyCharm window.
Select the Edit Configurations menu item.
Select the "Emulate terminal in output console" checkbox.
This will allow getpass to display the prompt and receive your password in the console.
"""
import getpass

# Don't forget to install the sqlalchemy package into your project.
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
# Even though you don't import anything from the psycopg2 package, you still need
# to install it into your SQLAlchemy project.

"""Small utility function whose only job is to manage the connection to the database."""

# This is the URL to my local PostgresSql database.
"""The breakdown of the fields in the URL and what they signify follows:
postgresql -        The relational database dialect.  Note that 'postgres' is no longer 
                    supported by sqlalchemy as a name for this dialect.
psycopg2 -          The database API employed.  It turns out that the default is psycopg2,
                    but I prefer to be explicit.  One less chance of failure.
userID:password     The user credentials used for logging into the database.
host                The name of the "machine" where PostgreSQL is running.
                    "localhost" signifies that the PostgreSQL instance is running on the
                    same machine where the application is running.
port                The default port # for PostgreSQL is 5432, but I already had a
                    database using that port, so that's why it defaults to 5433.
database            The name of the database within this particular instance of 
                    PostgreSQL.  Every PostgreSQL has a postgres database, but
                    you can create additional databases as needed.  Each CECS 323
                    section has their own database in the campus PostgreSQL instance."""
userID: str = input('User ID [postgres]--> ') or "postgres"
"""In order to get getpass to prompt you on the console, go to Run | Edit Configurations
in the top menu, and check the box: 'Emulate terminal in output console'.  Otherwise,
you will never see the prompt for the database password."""

"""If the user simply hits enter when any of these input prompts comes up, the result 
of the input function is a null string, which evaluates to False from a Boolean 
standpoint.  Which then means that the or with a text literal will result in that
literal as the output from the or operator.  Sort of a ghetto way to implement a
default, but it works.  What can I say."""
password: str = getpass.getpass(prompt=userID + ' password--> ')
host: str = input('hostname [localhost]--> ') or "localhost"
port: str = input('port number [5433]--> ') or "5433"
database: str = input('database [postgres]--> ') or "postgres"
# 'psycopg2' in this part of the db_url instructs SQLAlchemy that we are connecting to a PostgreSQL database.
db_url: str = f"postgresql+psycopg2://{userID}:{password}@{host}:{port}/{database}"
db_url_display: str = f"postgresql+psycopg2://{userID}:********@{host}:{port}/{database}"
print("DB URL: " + db_url_display)
engine = create_engine(db_url, pool_size=5, pool_recycle=3600, echo=False)

session_factory = sessionmaker(bind=engine)
# I am told that this next line contributes to making the code thread safe since the
# scoped_session returns the same Session every time it's called for any given thread.
# I personally don't expect to try to run concurrent threads from Python using
# SQLAlchemy anytime soon, but if I do, I'll be ready!
Session = scoped_session(session_factory)
