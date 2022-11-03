<p align="center" style="background:white;">
<img align="center" src="https://github.com/ArdaBakici/parkingintech/blob/main/static/logo.png" width=414 height=152>  
</p>

<br>

# **<a href="https://akilli-otopark.herokuapp.com/">Parking-in.tech</a>**

Frontend and backend side codes for the website <a href="https://akilli-otopark.herokuapp.com/">Parking-in.tech</a>.

Parking-in.tech is a project that aims to find a practical and economical solution
to parking in cities thus minimizing energy and time lost.

<br>

### For client and arduino codes visit ![parkingintech-client](https://github.com/ArdaBakici/parkingintech-client/)

All the codes for detecting empty parking lots with arduino and sending this information to server is present at ![parkingintech-client](https://github.com/ArdaBakici/parkingintech-client/)

# How it Works? 
Server holds a sqlite database for 3 different types of objects  
**Smart Parking Lot:** Parking lots with Parking-in.tech system. Automatic payment process and avaiable park space detection.  
**Normal Car Parks:** Alternative car parks that are near the smart parking lots.  
**Developer:** Accounts with permissions for updating smart parking lot status.  

Database is updated via POST request to /data/update/<dev_id>. Every developer has a dev_id, password and array of parking lots they can modify.
Every normal car park has an address and avarage traffic jam value. Traffic jam value is updated every 5 minutes using HERE Maps REST APIs.
Every smart parking lot has aviable space, total space and address values. Avaible space value can be modified by developer accounts.

License
---
Commercial use is forbidden.
