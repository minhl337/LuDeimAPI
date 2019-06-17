Sessions
========

LuDeimAPI sessions are persistent. That is if you are logged in you will stay logged in until you either clear your cache or the server running LuDeimAPI is restarted. To clear your session, call the :func:`logout` method.

As a convenience, your account's :literal:`user_id` and :literal:`type` are stored in your server session whenever :func:`login` is called. As a result, once :func:`login` has been called the uuid field of all requests can be safely omitted.

Additionally, the contents of the current session can be returned by calling :func:`get_sess`, and arbitrary string key-value pairs can be added to the session via the :func:`put_sess`. Note that if :func:`put_sess` is called with a key-value pair whose key is already defined in the session, then the value for that key will get overwritten with the new one.