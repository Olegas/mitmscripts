# MiTM Scripts

Scripts for mitmproxy to serve files from local drive

## Installing

Instructions for Mac OS X

 1. Get mitmproxy

    ```
        brew install mitmproxy
    ```

 2. Clone this repo

    ```
        git clone https://github.com/Olegas/mitmscripts.git
    ```
     
 3. Set desired adapter in `.adapter` file. If you use ethernet connection set `ADAPTER="Ethernet"`, 
    in case WiFi is used - set `ADAPTER="Wi-Fi"`
    
 4. Configure proxy
 
    ```
        ./set_proxy.sh
    ```
    
 5. Turn it on
 
    ```
        ./proxy_on.sh
    ```
    
 6. Run mitm
 
    ```
        ./run_mitm.sh
    ```

 7. Point your browser to [mitm.it](http://mitm.it) and follow the instructions how to install certificate to SSL interception
 
## Proxy configuration

Open `local_proxy.py` with your favorite text editor and configure `hosts` and `replacements` variables. 
See comments for more info.

## Disabling a proxy

Just run ```./proxy_off.sh```. Also you can always disable it using system preferences app.

## Known bugs

If you already have active Cisco AnyConnect session - disconnect it before starting and configuring mitm.
Changes made to system proxy settings while AnyConnect session is active will not be used by clients until AnyConnect is disconnected and connected again.  
 