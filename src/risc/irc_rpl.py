# Defines some IRC RPL - Preacher

RPL_WELCOME                 = "001"             # :Welcome_msg... <nick>!<user>@<host>
RPL_TOPIC                   = "332"             # <channel> :<topic>
RPL_TOPICWHOTIME            = "333"
RPL_NAMEREPLY               = "353"             # ( '='|'*'|'@' ) <channel> ' ' : ['@'|'+'] <nick> *( ' ' ['@'|'+'] <nick> )
RPL_ENDOFNAMES              = "366"             # <channel> :<info>
RPL_MOTD                    = "372"             # :- <string>
ERR_NICKNAMEINUSE           = "433"             # <nick> :<reason>
