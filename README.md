# acquisition.md — Rihards Zeila's LinkedIn content system

Code, rules and decks for the lead-magnet posting system (wordmark on everything public: rihardszeila.com).
Read `CLAUDE.md` first; it says what lives in this repo, what lives elsewhere (n8n, Supabase, Notion, the
claude.ai project and its Sunday scheduled task), and the rules that are not negotiable.

    pip install -r decks/requirements.txt
    cd decks && python3 deck2.py        # draws the specimen decks into out2/specimen-*/
    cd decks && python3 build2.py       # the seven Batch One kit decks (navy, colour brand marks)
    cd decks && python3 build_take.py   # the opinion deck
