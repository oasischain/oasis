console_msg_welcome = \
'''
/**************************************************/
   ___            _        ____ _           _       
  / _ \  __ _ ___(_)___   / ___| |__   __ _(_)_ __  
 | | | |/ _` / __| / __| | |   | '_ \ / _` | | '_ \ 
 | |_| | (_| \__ \ \__ \ | |___| | | | (_| | | | | |
  \___/ \__,_|___/_|___/  \____|_| |_|\__,_|_|_| |_|
                                                    
/**************************************************/
'''


web_msg_instructions = \
'''
<h1>/**** OASIS CHAIN ****/</h1>
<h2>Avaiable API commands:</h2>
<h3>/txion</h3>
Method: Post, E.g. curl "url:5555/txion" -H "Content-Type:applicaiton/json" -d '{"from":"tai","to":"chris","amount":3}' <br>
<h3>/blocks</h3>
Method: Get, list currenct blocks <br>
<h3>/test</h3>
Method: Test consensus function, if found longer chain, reset current<br>
'''