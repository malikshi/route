# Route Converter Script
This script converts routing rules from various sources into Sing-box compatible format.

## Features
* Supports multiple input formats: V2Ray, Clash, and plain text
* Converts domain rules into Sing-box compatible format
* Supports IP CIDR, port, and port range rules
* Generates SRS files for Sing-box

## Usage
1. Clone the repository: `git clone https://github.com/malikshi/route.git`
2. Run the script: `python compile.py`
3. The script will generate SRS files in the `release/srs/convert` directory

## Configuration
The script uses a `config.json` file to configure the input sources and routing rules. You can modify this file to suit your needs.

## Download Pre-Generated SRS Files
You can download pre-generated SRS files from the following links:

### SRS Files
* [dns](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/dns.srs)
* [urltest](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/urltest.srs)
* [controld](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/controld.srs)
* [doh](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/doh.srs)
* [googleapis](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/googleapis.srs)
* [google-ads](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/google-ads.srs)
* [bank-id](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/bank-id.srs)
* [ewallet](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/ewallet.srs)
* [marketplace](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/marketplace.srs)
* [operatorseluler](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/operatorseluler.srs)
* [ipcheck](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/ipcheck.srs)
* [rule-speedtest](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/rule-speedtest.srs)
* [youtube](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/youtube.srs)
* [google](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/google.srs)
* [whatsapp](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/whatsapp.srs)
* [instagram](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/instagram.srs)
* [facebook](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/facebook.srs)
* [twitter](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/twitter.srs)
* [telegram](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/telegram.srs)
* [line](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/line.srs)
* [netflix](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/netflix.srs)
* [catchplay](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/catchplay.srs)
* [hotstar](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/hotstar.srs)
* [disney](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/disney.srs)
* [spotify](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/spotify.srs)
* [viu](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/viu.srs)
* [bilibili](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/bilibili.srs)
* [rctiplus](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/rctiplus.srs)
* [mncplus](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/mncplus.srs)
* [molatv](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/molatv.srs)
* [indihometv](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/indihometv.srs)
* [transvision](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/transvision.srs)
* [visionplus](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/visionplus.srs)
* [wetviflix](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/wetviflix.srs)
* [vidio](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/vidio.srs)
* [streamindo](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/streamindo.srs)
* [tlds-id](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/tlds-id.srs)
* [reddit](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/reddit.srs)
* [yandex](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/yandex.srs)
* [microsoft](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/microsoft.srs)
* [riot](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/riot.srs)
* [steam](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/steam.srs)
* [remotevpn](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/remotevpn.srs)

## Notes
* Make sure to update the `config.json` file with your own input sources and routing rules.
* The script assumes that the Sing-box binary is installed and available in the system's PATH.

## Contributing
If you want to contribute to this project, feel free to fork the repository and submit a pull request.