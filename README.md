For reference:
- 192.168.122.1   is the NAT (can be a router in our home)
- 192.168.122.79  is Ubuntu (the Victim, trying to select his favorite Світоглядне ядро courses)
- 192.168.122.189 is Kali (with Ettercap)

In a network, when a device asks "Who has IP xxx?" (using ARP - address resolution protocol), it broadcasts it to all members of the network. What if we, instead of router, reply that we have the ip of the router? Then, the device would use us as the router, and we can do whatever we want with the traffic (i.e. we are the man in the middle).

But hey, when the device asks for the MAC of the IP, the router will be surely first, wouldn't it? Probably yes, but we are smart! There is this thing, called gratuitous ARP. It is an unsolicited ARP - the one nobody asked for. So we can just spam dozens of these gratuitous ARPs into the network and persuade all devices that we are indeed the router.

Very cool! Now, when the device makes a DNS request of our domain of choice, we will respond with our IP address (probably, local, but can be somewhere on the internet), instead of the real one.

It turns out that dekanat.ucu.edu.ua is an http website, which means the browser can't check, whether the ip given is really of dekanat or not. Let's spoof dekanat - nobody can notice, literally!

```
Device -----------------------> We (Ettercap) --------------------> e.g. 8.8.8.8 (Google DNS, unencrypted)
    who is dekanat.ucu.edu.ua?     |      who is dekanat.ucu.edu.ua?         |
                                   |                                         |
                                   |                                         |
               It's me, Mario!     |                                         |
       <---------------------------+                                         |
                                                                             |
Okay, so dekanat.ucu.edu.ua is 192.168.122.189                               |
                                                                             |
                                                                             |
                                         It's <Some real IP addr>            |
       <---------------------------------------------------------------------+

Idk, man, I trust my first response (I cached it and no longer consider any new ones), I still believe that 192.168.122.189 is the one


---------------------------------------> |
Hey, Mario, can I login with             |
husiev.pn:P@$$w0rd ?                     |
                                         |
                                         |
  Idk, man, some issues, try again later |
        <--------------------------------+


                                          --------------------------------------------------> real dekanat.ucu.edu.ua
                                          Do you know husiev.pn:P@$$w0rd ? Can I log in, pls?
```


