# OpenVPN-Monitor
A monitor script to alert when remote OpenVPN devices come up.

# Requirements
You'll need a mailserver to point the script at, and this assumes OpenVPN is running from the /etc/ directory.

```
touch /var/log/vpnignoreusers.txt
touch /var/log/vpnactivity.log
```

Modify the script and replace variables: 
	MAIL_SERVER_IP
	Sender-EMAIL-HERE
	Recipient-EMAIL-HERE