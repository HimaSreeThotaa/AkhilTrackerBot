import random

ROASTS = {
    "inactive": [
        "You missed so many tasks, even your shadow stopped following you.",
        "No tasks logged? Even my grandma is more productive than this.",
        "You treating this sheet like your gym membership? Ignored and forgotten.",
        "This productivity sheet turned into a ghost town.",
        "You and productivity had a fight, and clearly productivity won.",
        "Aaj bhi kuch nahi kiya? Matlab tu calendar ka weekend hai kya?",
        "Yeh sheet blank hai... jaise tumhara career goals.",
        "Kya tum meditation kar rahe ho ya bas kuch bhi nahi kar rahe ho?",
        "Sheet ne bhi socha hoga – kaash main kisi aur ke haath mein hoti.",
        "Tumhe dekhke WiFi bhi stable feel karta hai – bilkul hilta nahi ho.",
        "Sheet itni khaali hai, lagta hai Google Sheets ne bhi break le liya.",
        "Tum productivity ko left swipe kar diye kya?",
        "Tumhare logs dekh ke lagta hai Excel bhi bore ho gaya.",
        "Arre bhai, yeh sheet hai ya desert? Sukha hi sukha.",
        "Kuch toh sharam karo, bot bhi bore ho gaya.",
        "Tum ho productivity ke anti-hero."
    ],
    "progress_only": [
        "Always progress, never done — you’re a forever beta product.",
        "You started every task like a trailer, never released the full movie.",
        "Your tasks are stuck in progress like a bad traffic jam.",
        "You’re writing a book called ‘How to Start Everything and Finish Nothing.’",
        "Kaam shuru toh karte ho, par khatam karna tumse na ho payega.",
        "Progress bar kab full hoga, Windows 98 bhi wait kar raha hai.",
        "Tumhare tasks complete nahi hote, sirf evolve hote hain.",
        "Tumhari productivity dekh ke lagta hai ki deadline bhi resign kar de.",
        "Tum progress ke naam pe bas hope bech rahe ho.",
        "Tum toh ‘Kaam chalu hai’ board ban gaye ho – hamesha lage rahte ho.",
        "Progress toh dikha rahe ho, par result dikh raha hi nahi.",
        "Tum bas trailor ke king ho, movie kab release hogi?",
        "Tumhare tasks dekh ke lagta hai sabhi projects web series ban gaye hain – never-ending.",
        "Ek kaam pura karlo toh chhutti mil jaaye shayad!",
        "Tumko kaam se zyada uska progress report banana pasand hai."
    ],
    "missed_only": [
        "Missed tasks ka score dekh ke bot ko panic attack aa gaya.",
        "You’re setting a world record… for missing everything!",
        "Itna miss kiya, lagta hai tum tasks ko ghost kar rahe ho.",
        "Tumhare tasks tumse breakup chahte hain – tum kabhi milte hi nahi ho.",
        "Even your calendar gave up and joined Tinder.",
        "Missed tasks ka tsunami aaya hua hai idhar.",
        "Tumhare sheet ka naam hona chahiye ‘Lost and Found’.",
        "Kaash tumhara guilt bhi sheet mein dikhta. Missed, missed, missed!",
        "Missed tasks dekh ke MS Dhoni bhi retire ho jaata.",
        "Lagta hai tum tasks se social distancing maintain kar rahe ho.",
        "Har din miss karte ho, sheet bhi confuse ho gayi hai.",
        "Kya tum ghost mode mein ho? Har task miss!",
        "Sheet ka naam badal ke RIP kar dete hain kya?",
        "Tumhare tasks bhi tumse dosti tod diye lagte hain.",
        "Kya tum tasks se dushmani nikaal rahe ho?"
    ],
    "done_only": [
        "Perfect logs? Who are you trying to fool, bot ya khud ko?",
        "Every task done? Matlab sach ya GPT ne kara diya?",
        "You’re either ultra productive… or ultra good at faking it.",
        "Sheet dekh ke lag raha hai tum multi-universe ke Iron Man ho.",
        "Yeh sab complete kaise hua? Time travel use kiya kya?",
        "Even Tony Stark would doubt these stats.",
        "HR bhi kahega – ‘Itna perfect? Rejected for being too fake.’",
        "Sheet chilla chilla ke keh rahi hai – kuch toh gadbad hai daya!",
        "100% done? Matlab ya toh superhuman ho ya super cheater.",
        "Bot confused ho gaya – yeh log sach hai ya simulation?",
        "Perfect sheet, imperfect human – equation doesn’t match!",
        "Tum perfect logs bhejte ho, jaise students last night padte hain – sab yaad aata hai suddenly!",
        "Lagta hai tumhe future pata hai, sab kuch pehle se complete!",
        "Bot bol raha hai – ‘Yeh banda sach bol raha hai? Kya proof hai?’",
        "Yeh perfection dekh ke lagta hai ya toh coding sheet hai, ya cheating sheet."
    ],
    "universal": [
        "This isn’t productivity, this is professional procrastination.",
        "Your task sheet is emptier than my wallet after salary day.",
        "I’ve seen potatoes do more in a day.",
        "Your work ethic called, it’s on a long vacation.",
        "Tumhare logs dekh ke Google Sheets bhi crash ho gayi.",
        "Sheet pe itna white space hai, lagta hai Antarctica export kar diye ho.",
        "Productivity level: buffering since 2023.",
        "Tumhara ‘to-do’ list ab ‘never-do’ list ban gaya hai.",
        "Your motivation took a coffee break and never returned.",
        "Kya tum sheet dekh ke so jaate ho ya so ke dekhte ho?",
        "Tumhare jaise logon ke liye alarm clocks bhi resignation de dete hain.",
        "Tumse productive toh NPCs hote hain.",
        "Sheet ka naam productivity hai ya tragedy?",
        "Google bhi pooch raha hai – ‘Yeh kya kar raha hai banda?’",
        "Productivity ko tumne block kar diya kya?"
    ]
}

def get_random_roast(category):
    return random.choice(ROASTS.get(category, ROASTS["universal"]))

def get_roast_for_summary(summary_text):
    summary_text_lower = summary_text.lower()

    if "✅" in summary_text and "❌" not in summary_text and "🟡" not in summary_text:
        return get_random_roast("done_only")
    elif "❌" in summary_text and "✅" not in summary_text and "🟡" not in summary_text:
        return get_random_roast("missed_only")
    elif "🟡" in summary_text and "✅" not in summary_text and "❌" not in summary_text:
        return get_random_roast("progress_only")
    elif "✅" not in summary_text and "❌" not in summary_text and "🟡" not in summary_text:
        return get_random_roast("inactive")
    else:
        return get_random_roast("universal")

def get_roast_for_task(task_type):
    if task_type == "done":
        return get_random_roast("done_only")
    elif task_type == "missed":
        return get_random_roast("missed_only")
    elif task_type == "progress":
        return get_random_roast("progress_only")
    else:
        return get_random_roast("universal")
