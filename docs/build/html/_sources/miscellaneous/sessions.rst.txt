Sessions
========

LuDeimAPI sessions are persistent. That is if you are logged in you will stay logged in until you either clear your cache or the server running LuDeimAPI is restarted. To clear your session, call the **logout** method.

As a convenience, your account's **uuid** and **type** are stored in your server session whenever **login** is called. As a result, once **login** has been called the uuid field of all requests can be safely omitted.

Additionally, the contents of the current session can be returned by calling **get_sess**, and arbitrary string key-value pairs can be added to the session via the **put_sess**. Note that if **put_sess** is called with a key-value pair whose key is already defined in the session, then the value for that key will get overwritten with the new one.