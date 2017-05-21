# SSH_Server Script

#### What is it?
A simple bash script that greps all hostnames from `~/.ssh/config` then prompts the user for which hostname they want to connect to and then executes `ssh <hostname>` 

#### Usage
* Make sure the file has the right permissions via `ls -l ssh_server` or just run `chmod +x ssh_server`
* Copy file into a folder in your environment `PATH` such as `/usr/local/bin` or `/usr/bin` I'd recommend `/usr/local/bin`
    * If `/usr/local/bin` is not in your PATH variable then add it to your PATH
* If everything went correctly then you should be able to type `ssh_server` which will then list all hostnames located in your `~/.ssh/config file` with the `|` as a seperator between the hostnames and prompt you with which host you want to ssh to
* Type the hostname and press enter

#### Future Improvements
* Add autocomplete for hostnames
* Resolve errors if ssh fails
* Cleaner delimiters for the hostnames
