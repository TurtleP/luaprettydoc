## server.lua File Reference,

[
    {
        'source': 'server',
        'name': 'log',
        'args': "['format', '...']",

        'comments': [ '@brief Log a message with the current date and time to the console.' ]
    },

    {
        'source': 'server',
        'name': 'init',
        'args': '[]',
        'comments': ['@brief Initialize the server protocol.']
    },

    {
        'source': 'server',
        'name': 'config',
        'args': "['config']",
        'comments':
        [
            '@brief Configure the server settings.',
            '@param `config` -> table of { port = `number`, addresses = { `address1`, `address2`, `...` } }'
        ]
    },

    {
        'source': 'server',
        'name': 'receive',
        'args': "['client']",
        'comments':
        [
            '@brief Handle receiving of data per line.',
            '@param client -> Client object that was accepted in `client:update()`.',
            "@note If there's no data and the Client timed out, we want to wait for more data.",
            "@note If there's no data and we get any other message, close the Client connection",
            "@note If there's data, we want to return it to the main server to log that we got it"
        ]
    },

    {
        'source': 'server',
        'name': 'onConnect',
        'args': "['client']",
        'comments':
        [
            '@brief Handle when we get a Client to connect.',
            '@param client -> Client object from `server:update()`',
            '@note This function also handls receiving data from the Client.',
            "@note The server expects already-parsed Lua data from the Client's end."
        ]
    },

    {
        'source': 'server',
        'name': 'checkAddressAllowed',
        'args': "['hostname']",
        'comments':
        [
            '@brief Check if an IP address is allowed to connect.',
            '@param `hostname` -> Address to check.',
            '@note `server.allowedAddresses` handles this, so add IP addresses that you trust.',
            '@note However, setting the table to either nil or "*" can allow any connection.'
        ]
    },

    {
        'source': 'server',
        'name': 'update',
        'args': '[]',
        'comments':
        [
            '@brief Update the server protocol.',
            '@note Waits and accepts clients to be useable for data reception.',
            '@note Once a Client is accepted, it is checked against `server.allowedAddresses`.',
            '@note It is then kept alive until the server has been told that the Client disconnects.'
        ]
    },

    {
        'source': 'server',
        'name': 'close',
        'args': '[]',
        'comments': ['@file server.lua', '@brief This is the server file that the client connects to']
    }
]
