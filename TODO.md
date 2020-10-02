### TODO:

Security:

- replace in settings.py:
  - Django secret. Generate unique
- Generate unique MySQL user/password
- python3 manage.py check --deploy

- cron log. add timestamp
- Router model. add incoming RADIUS port, default 3799. router type (?)
- Customer model. add ~~fullname~~, other fields
- Customer admin. Format datetime (min, sec, ...)
- Disable REST API. Temporary until React/redux

### Features:

- Settings in admin  
  - Accounting interval  
  - Show password in password field (on field focus). JS (?)  
  - timezone  
- Timezone set/check/fix  
- Create customer services instead of a customer  
- IP networks. Use IP address from network  
- Add button 'Show password' for password fields  
- Tariff billing day (?)  
- Localization ?  
- Django messages ?   
~~- coa, disconnect in other thread~~  
- radius_accounting. get customer only once  
