rule Telegram_Pages {
   meta:
      author = "Asaf Aprozper"
      description = "Detects Telegram account pages on the Internet"
      reference = "github.com/3pun0x/repotele"
   strings:
      $string = /tg:\/\/resolve\?domain\=([^"]+)/
   condition:
      all of them
}

rule Telegram_Links {
   meta:
      author = "Asaf Aprozper"
      description = "Detects Telegram links on the Internet"
      reference = "github.com/3pun0x/repotele"
   strings:
      $string = /t.me\/([\w]+)/
   condition:
      all of them
}

rule Telegram_APIs {
   meta:
      author = "Asaf Aprozper"
      description = "Detects Exposed Telegram APIs on the Internet"
      reference = "github.com/3pun0x/repotele"
   strings:
      $string = /api\.telegram\.org\/([^\/]+)/
   condition:
      all of them
}
