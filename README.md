# Board Game Website
Open project for CS316: Database Systems

Github link: https://github.com/ChrstphrHll/316project

Group Name: Weak Entity Set

Contributors:
Christopher Hall, 
Kegan Lovell,
Molly Borowiak,
Adam Kosinski,
Aryan Mathur

# Setup

## Installing
1. Clone the repository.
2. Change directory into the repository directory and run `./install.sh`
3. Run `source env/bin/activate` to start the virtual environment. While the environment is activated, you should see a `(env)` prefix in the command prompt in your VM shell.
You should only run Flask while inside this environment; otherwise it will produce an error.
4. Use the database setup script by running `./db/setup.sh`

## Running the Website

1. Ensure the virtual environment is active. If it is not, run `source env/bin/activate` again to start it.
2. Run `flask run`
3. Flask should give you an address to visit to view the site, something like `http://(example_url):5000/`
4. To stop the website, use <kbd>Ctrl</kbd>+<kbd>C</kbd> in the VM shell where flask is running.
5. To deactivate the environment, run `deactivate`.