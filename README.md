## Personal weekly status generator

Uses [Wunderlist](https://wunderlist.com) as the backend. It also depends on
the [pass tool](https://www.passwordstore.org) for storing the secret, and the
client id. Currently it just prints the report on the STDOUT, idea is to pipe
it where ever we want it.

### Other configuration

~/.weeklyreport.ini contains the following information

    [wunderlist]
    inbox=ID_OF_INBOX

### pass values

* wunderlist/secret
* wunderlist/clientid

### Requires patched version of wunderpy2

In my github account, I have a fork copy of wunderpy2 with patches to get comments
details. Use that module :)

