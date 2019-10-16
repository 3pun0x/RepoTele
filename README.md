![RepoTele](https://i.imgur.com/orNBRgU.jpg)

# RepoTele - Hunting Abused Telegram Accounts

The following is a part of my talk called "Leveraging Yara Rules to Hunt for Abused Telegram Accounts", that script is the second step in my research to hunt for malicious Telegram accounts using Telethon. To perform its activity, the script gets a config file with Phone Number, Telegram API ID, and HASH which you can create through the Telegram API website. The next mandatory step is to input the script with a list of Telegram Accounts to scan. 

## Prerequisites
* [Python3](https://www.python.org/download/releases/3.0/)
* [Telethon](https://github.com/LonamiWebs/Telethon)
* [Telegram API](https://my.telegram.org/auth)

## Getting Started
1. Clone the project
2. Add Telethon library
3. Get your Telegram api_id and api_hash through Telegram API website
3. Create config file in CSV format by order of "[phoneNum],[api_id],[api_hash]"
4. Create a TXT file named "file_telegram_names.txt" with the list of Telegram accounts to scan
5. Execute the script using Python3
```
Python3 RepoTele.py
```
6. Import the 'output.csv' to Google Sheets to read the file clearly.

## References
1. [BSidesCyprus](https://bsidescyprus.com/agenda.html)
2. [Code Blue 2019 Tokyo-Japan](https://codeblue.jp/2019/en/talks/?content=talks_13)


## Authors
**Asaf Aprozper (3pun0x)** - *Creator* - [Twitter](https://twitter.com/3pun0x) - [GitHub](https://github.com/3pun0x) 

## License
This project is licensed under the GPLv3 License - see the [LICENSE.md](https://www.gnu.org/licenses/gpl.html) file for details
Copyright © 2019 Asaf Aprozper.  All rights reserved.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
