# Hunt-the-Wampus

![Wampus Game](Images/wampus.gif)

Last semester, I was approached by a friend who was trying to improve his Python skills by recreating a game called “Hunt the Wampus”. He asked me if I could help him, and I told him that I would. Needless to say, a few months later (actually like 8), I 100% didn’t help him and instead programmed my own version of the game. As for how it plays, Hunt the Wamus was “a text-based adventure game developed by Gregory Yob in 1973. In the game, the player moves through a series of connected caves, arranged in a dodecahedron [see below], as they hunt a monster named the Wumpus.” 

<p align="center">
  <img src="https://github.com/ddritzenhoff/Hunt-the-Wampus/blob/master/Images/dod.PNG?raw=true" alt="Wampus 2D Matrix"/>
</p>

Beginning the project, since I didn’t know how to create or even pronounce dodecahedron (I still can’t), I figured that I should stick to a purely text based version of the game and iterate from there. I began by adding simple input statements which changed the outcome based off of the answer. Things like “up”, “down”, “left”, and “right” caused a purely textual “hero” to move around the Wampus universe. There, the hero encountered the Wampus, an endless pit of death, nothing, or bats that teleported you. After completing the rudimentary version, I began creating a text-based visual  representation of the Wampus world as seen below. The largest problem that I immediately ran into was how I wanted to transfer information throughout my program. I wasn’t sure whether it made the most sense to create an object for each character, store basic information in arrays, or something else. Also, I needed to solve problems like making sure that the entities in the game weren’t assigned to the same locations. Taking baby steps, I eventually found which data structures best served my purposes. After doing a bit more cleaning up, I had something working which actually resembled a game.

<p align="center">
  <img src="https://github.com/ddritzenhoff/Hunt-the-Wampus/blob/master/Images/wampus_2d_matrix.PNG?raw=true" alt="Wampus 2D Matrix"/>
</p>


Still, I didn’t think the project was entirely done. Although I had programmed a decent amount up until then, I thought the lackluster visuals gave the impression that I had accomplished very little. Initially thinking I would just upload the python code to a website using Flask and have it run with its own cute little domain name, I soon realized that what I wanted to do hadn’t really been done before. Everything that I could find was pretty jank. This soon caused me to change course and begin looking around at different Python libraries. During this time, I was using the Nano text editor a fair bit since I liked playing around in Ubuntu. I thought that the program looked nice and simple enough, so after a bit of digging, I found the library used to mimic the look. Shortly afterwards, I began reworking my project to fit the library’s specifications. But it still wasn’t finished. I realized someone playing the game for the first time would have no idea where to start and how to win. Thus, a main menu needed to be added. Also, it made the project look more complex with a marginal amount of effort. After another bit of coding and a whole lot more debugging, I had a finished product. Overall, I’m happy with the result, and I learned a decent amount along the way.

Once you have the necessary python libraries installed on your machine, simply run “python3 wampus.py” to start.

Cheers

