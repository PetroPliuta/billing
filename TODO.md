### TODO:

- settings.py
  replace:

  - Debug: False + Django secret. Generate unique

- cron log. add timestamp
- Generate unique MySQL user/password
- Router model. add incoming RADIUS port, default 3799
- Customer model. add fullname, other fields

### Features:

- Settings in admin
  - Accounting interval
  - Show password in password field (on field focus). JS (?)
  - timezone
- Timezone set/check/fix
- Send CoA RADIUS packet when tariff changed (optionally)
- Create customer services instead of a customer
- IP networks. Use IP address from network
- Add button 'Show password' for password fields