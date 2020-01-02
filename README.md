# Who are you?

This is a basic SSH Server implementation based on Twisted and Python. 
It's only purpose is to demonstrate, that by default a ssh client sends all public keys.
This is not a security concern, because the keys are public anyway, 
but you can do interesting things with them.

For example FiloSottile [compares](https://github.com/FiloSottile/whosthere) your public key with Github public keys and is able to retrieve your Github Nickname.
