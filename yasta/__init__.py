from flask import Flask

app = Flask('yasta')
app.debug = True

app.config.from_object('yasta.settings')

import restapi

