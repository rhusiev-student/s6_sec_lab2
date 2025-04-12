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
husiev.pn:PASSWORD!SECRET ?                     |
                                         |
                                         |
  Idk, man, some issues, try again later |
        <--------------------------------+


                                          --------------------------------------------------> real dekanat.ucu.edu.ua
                                          Do you know husiev.pn:PASSWORD!SECRET ? Can I log in, pls?
```

As we can see, **even if the DNS is from the outside network** (e.g. Google's 8.8.8.8 or some other like 9.9.9.9, 1.1.1.1, 9.9.9.11, etc.), we **can still spoof** the DNS! That's because by default DNS is not transmitted over HTTPS, TLS or any other encrypted way. So the Ettercap can see DNS requests respond to them with spoofed stuff.

**What might be a local company's DNS for**?
- (even I used it) add domains for some local resources (local websites, printers, databases etc.) I used one on a pihole to redirect, e.g., pi.hole to the configuration page of it. It has some inherent limitations, though, as e.g. it can't produce good https by default (the connection is not secure)
- block certain requests (I used it too!) - block unwanted content like nsfw or use it as a DNS adblocker (PiHole!)
- or just faster response time (somehow, I used it too, with `unbound`) - results get cached and new users don't have to Google or smth, what is the IP, they get the result directly from the router

**What can make this attack harder/impossible?**
- User side:
    - As mentioned, DNS over HTTPS or DNS over TLS would require the response to have valid certificates, so the MITM couldn't respond correctly (the device would reject it's offer, if the attacker could understand that it is asked about DNS in the first place)
    - Using only HTTPS sites for sensitive data (including anything that has accounts) -- looking at you, UCU's dekanat
- Router side: restrict, so that peers can't see each other in the network. If I can't tell you that I am router, you can't be deceived that I am a router

A very cool demonstration of an ordinary person trying to choose courses for the next semester:

![demonstration](./dekanat_spoof.mp4)

Here are the pcap files:
- ![./UBUNTU.pcap](./UBUNTU.pcap)
- ![./KALI.pcap](./KALI.pcap)

# The configuration

FastAPI server that listens on GET /receive

Some HTML files with JS to send requests to dekanat.ucu.edu.ua/receive with username:password

Apache2 to host HTML files on Kali

So when dekanat.ucu.edu.ua is spoofed, it gets HTML from Kali and sends the data to Kali to the python server

The things I did with Ettercap:
- Set `ec_uid` (and `ec_guid`) to 0, so that the ettercap has rights to read `/etc/ettercap/etter.dns` (at least I understand so. It did not work previouslyr)
- Uncomment `redir_command_on ...` (and off) - if I understand correctly, to redirect incoming traffic into ettercap
- Add `dekanat.ucu.edu.ua` A record to point to `192.168.122.189` - self. (Same for `www.dekanat.ucu.edu.ua` just in case; but here it is a redirect)

Then, in ettercap, I say to the victim and to the nat that I am the router (hehe). I get their IPs through ettercap's scan and convince using ARP

Then I enable the dns_spoofing plugin - and voila!
