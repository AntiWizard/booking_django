wsgi_app = 'booking.wsgi.application'
loglevel = 'debug'
workers = 2
bind = '0.0.0.0:8000'

accesslog = '/var/log/gunicore/booking.log'
errorlog = '/var/log/gunicore/booking.log'

capture_output = True
