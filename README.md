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
* [000_dns.srs](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/000_dns.srs)
* [001_urltest.srs](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/001_urltest.srs)
* [002_controld.srs](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/002_controld.srs)
* [003_doh.srs](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/003_doh.srs)
* [004_googleapis.srs](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/004_googleapis.srs)
* [005_bank-id.srs](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/005_bank-id.srs)
* [006_ewallet.srs](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/006_ewallet.srs)
* [007_marketplace.srs](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/007_marketplace.srs)
* [008_operatorseluler.srs](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/008_operatorseluler.srs)
* [009_ipcheck.srs](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/009_ipcheck.srs)
* [010_rule-speedtest.srs](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/010_rule-speedtest.srs)
* [011_youtube.srs](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/011_youtube.srs)
* [012_google.srs](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/012_google.srs)
* [013_whatsapp.srs](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/013_whatsapp.srs)
* [014_instagram.srs](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/014_instagram.srs)
* [015_facebook.srs](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/015_facebook.srs)
* [016_twitter.srs](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/016_twitter.srs)
* [017_telegram.srs](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/017_telegram.srs)
* [018_line.srs](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/018_line.srs)
* [019_netflix.srs](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/019_netflix.srs)
* [020_catchplay.srs](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/020_catchplay.srs)
* [021_hotstar.srs](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/021_hotstar.srs)
* [022_disney.srs](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/022_disney.srs)
* [023_spotify.srs](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/023_spotify.srs)
* [024_viu.srs](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/024_viu.srs)
* [025_bilibili.srs](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/025_bilibili.srs)
* [026_rctiplus.srs](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/026_rctiplus.srs)
* [027_mncplus.srs](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/027_mncplus.srs)
* [028_molatv.srs](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/028_molatv.srs)
* [029_indihometv.srs](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/029_indihometv.srs)
* [030_transvision.srs](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/030_transvision.srs)
* [031_visionplus.srs](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/031_visionplus.srs)
* [032_wetviflix.srs](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/032_wetviflix.srs)
* [033_vidio.srs](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/033_vidio.srs)
* [034_streamindo.srs](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/034_streamindo.srs)
* [035_tlds-id.srs](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/035_tlds-id.srs)
* [036_reddit.srs](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/036_reddit.srs)
* [037_yandex.srs](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/037_yandex.srs)
* [038_microsoft.srs](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/038_microsoft.srs)
* [039_riot.srs](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/039_riot.srs)
* [040_steam.srs](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/040_steam.srs)
* [041_remotevpn.srs](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/041_remotevpn.srs)

## Notes
* Make sure to update the `config.json` file with your own input sources and routing rules.
* The script assumes that the Sing-box binary is installed and available in the system's PATH.

## Contributing
If you want to contribute to this project, feel free to fork the repository and submit a pull request.