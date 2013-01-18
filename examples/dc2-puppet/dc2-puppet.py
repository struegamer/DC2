#!/usr/bin/python


from dc2.puppet.application import app
import settings

app.config.from_object(settings)

if __name__=='__main__':
    app.run()

