# Who are you?

This is a basic SSH Server implementation based on Twisted and Python. 
It's only purpose is to demonstrate that by default a ssh client sends all public keys to the remote server.
This is not a security concern (because the keys are public anyway) but you can do interesting things with them.

For example FiloSottile [compares](https://github.com/FiloSottile/whosthere) your public key with Github's database and is able to retrieve your Github nickname.

# How to run this demo?
1. Install twisted and the required crypto modules: `pip install -r requirements.txt'
2. Create a key pair for the server in the same directory: `ckeygen -t rsa -f ssh_host_rsa_key`
3. Run:`python3 ssh.py`

You can now ssh onto your machine (default port is 5022) and will get a output similar to this:
```
➜  ~ ssh localhost -p 5022    

    +---------------------------------------------------------------------+
    |                                                                     |
    |  Hello there! :-)                                                   |
    |                                                                     |
    |                                                                     |
    |  This is demo to demonstrate that SSH sends all your public keys    |
    |  by default.                                                        |
    |  The original idea comes from @FiloSottile  and is available here:  |  
    |  https://github.com/FiloSottile/whosthere                           |
    |                                                                     |
    |                                                                     |
    |                                                                     |
    |                                                                     |
    |  P.S. This version is written in 100% pure Python                   |
    |  https://github.com/M0r13n/some_repo                                |
    |                                                                     |
    |  -- C u                                                             |
    |                                                                     |
    |---------------------------YOUR KEYS --------------------------------|
    |<RSA Public Key (2048 bits)                                          |
    |attr e:                                                              |
    |    01:00:01                                                         |
    |attr n:                                                              |
    |    00:d4:24:16:f4:01:9d:0f:fa:69:75:1e:e6:87:6e:                    |
    |    6d:ff:88:52:51:2e:f1:4f:97:c6:3a:85:44:e8:e9:                    |
    |    10:61:16:ff:42:42:b4:80:5a:88:07:2e:26:a7:c6:                    |
    |    4d:dc:cd:79:70:b3:85:2d:05:4b:ee:76:61:fe:11:                    |
    |    a3:93:53:a6:3e:db:11:1c:b4:b1:47:98:26:99:8a:                    |
    |    f2:28:21:ae:32:84:e3:04:6d:72:ad:b7:88:e4:16:                    |
    |    db:4d:a0:23:e2:33:c3:24:5f:88:01:0f:cb:f5:69:                    |
    |    81:be:83:57:1f:38:8a:c5:26:f2:9f:b4:a7:65:7f:                    |
    |    35:83:5a:29:cb:64:df:64:0c:0b:86:24:d5:2b:f9:                    |
    |    5b:14:96:59:79:7c:33:ad:e3:29:c4:35:fc:b1:97:                    |
    |    dd:8f:13:df:3e:ad:4c:e7:97:84:da:38:6b:16:36:                    |
    |    0b:cb:71:03:71:05:45:96:95:6e:66:c0:39:c7:f1:                    |
    |    e1:47:f2:7b:89:8e:df:de:0d:3c:bc:39:e8:67:2b:                    |
    |    28:02:bc:3e:01:00:da:de:cb:68:47:ff:18:55:7c:                    |
    |    b8:b0:77:9f:de:47:8c:1b:1d:5e:87:a9:99:12:86:                    |
    |    4a:26:67:58:71:07:8a:dc:1a:df:5f:20:fe:12:d2:                    |
    |    7d:e8:4a:bb:a7:45:9a:55:3d:d9:21:03:05:ea:f5:                    |
    |    17:29>                                                           |
    |<RSA Public Key (2048 bits)                                          |
    |attr e:                                                              |
    |    01:00:01                                                         |
    |attr n:                                                              |
    |    00:ec:87:be:c2:c5:b7:0e:ee:e0:50:c5:97:11:dc:                    |
    |    bd:a7:1f:c2:23:8e:25:33:fb:3f:62:93:59:14:55:                    |
    |    d6:f3:a5:32:30:db:cc:f7:ed:b1:0a:7f:44:b2:a0:                    |
    |    c2:ff:11:2b:42:04:da:32:ac:93:57:1d:09:23:04:                    |
    |    57:f6:8d:e0:fc:90:3c:ff:e0:05:e5:1e:4c:aa:10:                    |
    |    f4:a5:53:1a:2d:eb:c3:15:46:97:07:0f:4c:ab:32:                    |
    |    c8:94:84:89:04:c1:2c:a9:46:60:41:dc:44:38:a1:                    |
    |    d2:9e:97:a5:fb:10:05:c0:35:8c:cb:05:db:9e:1b:                    |
    |    9f:55:b1:b9:02:a0:98:f8:d2:d2:a0:93:eb:f9:de:                    |
    |    12:e7:9f:85:c9:9d:ff:30:54:89:c6:d9:a3:0f:74:                    |
    |    00:10:f2:62:f1:ec:44:6d:62:f0:0d:0f:97:74:1b:                    |
    |    38:8b:7e:10:6f:1e:a9:e2:34:ef:dd:45:48:50:11:                    |
    |    3a:b7:16:17:67:89:7d:33:5e:87:11:42:7e:b1:75:                    |
    |    ef:a0:ab:b9:8a:87:7d:58:45:04:10:4b:4c:b1:30:                    |
    |    6e:20:49:fe:4b:03:de:c9:2a:ae:de:ea:b1:6f:b8:                    |
    |    b2:80:5e:55:90:58:12:b8:04:60:f5:9a:93:d9:12:                    |
    |    de:fc:6f:37:6d:a3:15:2d:0b:85:e2:f7:6f:c0:aa:                    |
    |    79:79>                                                           |
    +---------------------------------------------------------------------+

```
