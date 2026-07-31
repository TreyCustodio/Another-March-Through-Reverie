from . import vec

#   16:9 Aspect Ratio   #
# SCREEN_SIZE = vec(640,360)
# SCREEN_SIZE = vec(500,240)
SCREEN_SIZE = vec(320,240)

               
#   Universal Upscale Value -- all images will be scaled to this value  #
SCALE_FACTOR = 1

# PLAYER_SCALE = 1.15
PLAYER_SCALE = 1

#   Upscaled Screen Size    #
UPSCALED = SCREEN_SIZE * SCALE_FACTOR

#   Gravity #
GRAVITY = 980

#   Wayweaver's Name    #
NAME = "Wayweaver"

#   FLAGS   #
FLAGS = {}
for f in range(2_000):
    FLAGS[f] = False

#   0 -> ?
#   1-499       -> Middleground
#   500-999     -> Underground
#   1000-1499   -> Overground
#   1500 - 1599 -> Item Flags
#   1600 - 1999 -> Anything Else

#   1   -> First talk with Marley Hill

SPEECH = {
    'intro_1':"\
    Welcome to %gEarth:%&&\n\
    A familiar place in a distant time.$$\
    The homeworld of the %rRevelers%,&&\n\
    or %rHumans%, as the ancient\n\
    ones refer to them.$$\
    Our universe has been at war with\n\
    this %rinvasive species% for millennia.$$\
    I am a %wWayweaver%.&&\n\
    *.%wI move through space as I please,*,\n\
    at whatever speed I desire%.$$\
    I am the only one of %wmy kind% in the universe.$$\
    I have no homeworld,\n\
    %wfor I was birthed by the stars%.$$\
    Long have I searced for another %wlike me%,\n\
    *,but to no aveil.$$\
    A century ago, the %pAllies of the Universe%\n\
    were successfull in forcing the\n\
    %rRevelers% to retreat\n\
    back to their %ghomeworld%.$$\
    My earliest memories are from around then,&&\n\
    aimlessly drifting through space,\n\
    watching a cataclysmic war\n\
    unfold before me.$$\
    I chose to help preserve the universe by hunting\n\
    %rRevelers% across space,\n\
    and the other beings\n\
    of the cosmos nourished me\n\
    with food and knowledge in return.$$\
    Now only %r11 Revelers% remain.&&\n\
    They’ve taken refuge on %gEarth%\n\
    for half a century.$$\
    But today,*. I’ve decided to put an end\n\
    to this chapter of the universe's history.$$\
    I'll hunt down %rall 11% of them\n\
    who have yet to perish.$$\
    However, traversing %gEarth% is like\n\
    stepping foot directly into into\n\
    a %rpredator’s claws%.$$\
    I’m no rabbit, but I am hunting\n\
    the universe’s %rapex predator%.&&\n\
    What they lack in numbers,\n\
    they far make up for in knowledge\n\
    of their first planet.$$\
    \n\n\
    *.*.%wI’ll need to tread carefully...%",

    "name_1":"%wThe Wayweaver%.&&\nMay he weave together a peaceful universe...$$%wWhat will you name him?%\n\n\n",



    "marley_1":"Something is wrong...\n",

    "marley_2":"So... the Wayweaver arrives...\n",

    "marley_3":"Who said that?\nWho are you?\n",

    "marley_4":"I'd be stupid if I told you\nwho I was.$$Surely, you know that.\n",

    "marley_5":"%wThis is... odd...$$I hear his voice, and I can sense\n that he is% %rhuman%,$$%wbut I am unable to discern where\n it's coming from...$$I am hearing his voice in my mind!%$$",

    "marley_6": "%rReveler%, how are you communicating\nwith me?",

    "marley_7": "It’s tricky to explain,\nand even trickier to believe.$$You know how you have an innate\nability to sense my kind?",

    "marley_8": "Yes. There are eleven of you,\n and all of you are here on Earth.$$I am coming for you.\n",

    "marley_9": "Yes, I know.$$I have accepted that fact.\n",

    "marley_10": "...",

    "marley_11":
    "My point is that I can sense\n\
your presence as well.$$\
%gI have a strong connection\n\
to Earth%.$$\
You could say that\n\
I see...$$\
%geverything that mother\n\
nature sees%.$$\
But don't let that\n\
worry you.$$\
I'm the only one\n\
%glike me%.$$\
None of the others know\n\
that you're here.",

    "marley_12":
    "That's...&&\
 to be expected...$$\
But why would you give me\n\
that information?",

    "marley_13":
    "%wCould this one\n\
truly be an ally?$$\
No.&& I must not be\n\
fooled by their trickery$$\
Such mischievous behavior\n\
is how they were able$$\
to wage war against\n\
the rest of the$$\
universe in the\n\
first place.",

    "marley_14":
    "I hope to gain your trust.$$\
You see, I'm different\n\
from the others.",

    "marley_15":
    "Regardless of your power,\n\
that's what %rthey all% say.",

    "marley_16":
    "I'm talking about my\n\
%ggoals%, not my power.$$\
I deeply love %gEarth%,\n\
%gmy Earth%.$$\
My only wish is to keep it\n\
safe and healthy.$$\
As you can see, that\n\
task is impossible.$$\
The rest of my species\n\
doesn't care like I do.$$\
They only care about\n\
making themselves stronger.",

    "marley_17": "...",

    "marley_18":
    "I know that I can't\n\
possibly gain your trust,$$\
but... please...$$\
From a servant of %gEarth%...$$\
Ensure that no other\n\
species ravages my home,$$\
like my own kind has done.",

    "marley_19":
    "%wFor the first time\n\
in my existence...$$\
I am at a loss for words.%"


}

"""
“The Wayweaver” 
"""