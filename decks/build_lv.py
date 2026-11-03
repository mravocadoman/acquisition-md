"""Latvian decks (2 Nov 2026). Rihards: "can we do carousels and videos and creatives for latvian version also in
latvian?" The Latvian posts go out from the Mārketinga Skola Facebook page and Instagram, so these are the five
carousel decks of build2.py / build_take.py rewritten in Latvian (latvian-writing rules: Tu, no dashes, 0,38 €, 20 %),
with marketingaskola.lv in the footer. deck2.py is untouched: DeckLV only swaps its English chrome (swipe, the gate,
the outro). Files end in -lv so they never overwrite the English ones. Run: python3 build_lv.py"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import deck2
from deck2 import Deck, contact_sheet, art_tiles, art_bars2, art_code_to_slide, art_circles2, L, W
import brand_icons  # official marks on the tool chips where a brand publishes one
from art_extra import art_two_empty
import matplotlib.pyplot as plt
# Same font set-up as build2.py: Arial measured and embedded (macOS Helvetica.ttc has no bold for matplotlib,
# core Helvetica has no euro width). Arial also carries every Latvian letter.
plt.rcParams["font.sans-serif"] = ["TeX Gyre Heros", "Arial", "Liberation Sans", "DejaVu Sans"]
plt.rcParams["pdf.use14corefonts"] = False; plt.rcParams["pdf.fonttype"] = 42

deck2.BRAND = "marketingaskola.lv"            # chrome() and the art read it at draw time
deck2.TOOL_GLYPH.update({"E-pasts": "mail", "Lead forma": "form"})

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out2")
os.makedirs(OUT, exist_ok=True)
built = []


# Latvian typography: a number stays on the line of the word or unit it counts ("2 %", "1 175 €", "3 stundām").
# deck2 wraps on any whitespace, a no-break space included, so the glue is a stand-in glyph of about a space's
# width while the slide is laid out, and becomes a real no-break space once the text is placed.
GLUE, NBSP = "\u00a6", "\u00a0"
def glue(s):
    if not isinstance(s, str): return s
    return re.sub(r"(?<=\d) (?=\S)", GLUE, s).replace("Bez maksas", "Bez" + GLUE + "maksas")


class DeckLV(Deck):
    def _unglue(self, n):
        for txt in self.ax.texts[n:]:
            if GLUE in txt.get_text(): txt.set_text(txt.get_text().replace(GLUE, NBSP))

    def tx(self, x, y, s, *a, **k):
        n = len(self.ax.texts); r = super().tx(x, y, glue(s), *a, **k); self._unglue(n); return r

    def rich(self, x, y, s, *a, **k):
        n = len(self.ax.texts); r = super().rich(x, y, glue(s), *a, **k); self._unglue(n); return r

    def cover(self, *a, **k):
        super().cover(*a, **k)
        for txt in self.ax.texts:
            if txt.get_text().startswith("swipe"): txt.set_text("velc  ›")

    def gate(self, keyword, what, extra=None):
        t = self.t; self.new()
        y = self.kicker("Materiāls")
        ask = "un saiti uz materiālu nosūtīsim privātā ziņā. Bez maksas."
        bh = 220
        h, _ = self.tx(L, y, what, 36, W, ls=1.25, max_h=260, min_size=30); y -= h + 44
        by = y - bh
        self.box(L, by, W, bh, t["gate"], r=16)
        self.tx(540, by + bh - 46, "Komentē", 30, W - 40, color=t["on_gate"], ha="center", va="center")
        self.tx(540, by + 84, keyword, 84, W - 40, color=t["on_gate"], weight="bold", ha="center", va="center", max_h=110, min_size=52)
        y = by - 36
        h, _ = self.tx(L, y, ask, 30, W, weight="bold", ls=1.25); y -= h + 26
        if extra: self.tx(L, y, extra, 30, W, color=t["muted"], ls=1.3, min_size=26)

    def outro(self, question, save_line):
        t = self.t; self.new()
        y = self.kicker("Tava kārta")
        bh = 160
        h, _ = self.tx(L, y, question, 50, W, weight="bold", ls=1.12, max_h=330, min_size=36); y -= h + 60
        by = y - bh
        self.box(L, by, W, bh, t["dim"], r=16)
        self.tx(540, by + bh / 2, save_line, 32, W - 60, ha="center", va="center", ls=1.2, max_h=bh - 30, min_size=26)
        h, _ = self.tx(L, 246, "Rihards Zeila · 12 gadi reklāmu pirkšanā · tagad būvēju sistēmas, kas to dara", 24, W, color=t["muted"], ls=1.25, count=False)
        self.tx(L, 246 - h - 18, deck2.BRAND, 26, W, color=t["accent_small"], weight="bold", count=False)


def done(d):
    pdf, n = d.save(); built.append((d.slug, n, pdf, max(d._words)))
    contact_sheet(os.path.join(OUT, d.slug), os.path.join(OUT, d.slug + "-sheet.png"))
    print(f"{d.slug}: {n} slides, {os.path.getsize(pdf)//1024} KB, densest slide {max(d._words)} words")

# ---------------------------------------------------------------- KOMANDA
d = DeckLV("team-department-lv", OUT, "navy")
d.cover("Manā mārketinga nodaļā ir **deviņi darbinieki**. Neviens nav cilvēks.", "Viens ķeksītis no manis, deviņdesmit sekundes dienā.",
        art=lambda d, x, y, w, h: art_tiles(d, x, y, w, h, 9, 7, "strādā", "sargā"),
        tools=["Claude", "n8n", "Notion", "LinkedIn"])
d.flow("Es uzrakstu. Pārējo izdara viņi", [
    "Viens ķeksītis to apstiprina",
    "8:00: sadala četrās daļās",
    "Slaidus zīmē no ieraksta skaitļiem",
    "10:00 publicēts, arī Facebook",
    "Pēc 3 stundām X un Threads"], kicker="kad ieraksts gatavs")
d.grid("Deviņi darbinieki. Septiņi publicē. Divi sargā.", 9, 7, "dara darbu", "ceļ trauksmi, kad kaut kas salūzt", kicker="nodaļa", cols=3)
d.statement("Viņiem aizliegts uzrakstīt kaut vienu vārdu.", kicker="vienīgais noteikums",
            sub="Katrs mašīnas rakstīts ieraksts bija normāls un uzreiz aizmirstams. Ja tekstu rakstīju es, viņi nedrīkst mainīt nevienu burtu.")
d.compare("Aizstāts. Nav aizstāts.", "Aizstāts", ["Plānotājs", "Dizainers", "Publicētājs"],
          "Nav aizstāts", ["Autors", "Gaume", "Sarunas ar Tevi"], kicker="godīgā daļa")
d.stats([("90 s", "no manas dienas", "viens ķeksītis, tad atbildu"),
         ("4", "daļas no ieraksta", "ieraksts, komentārs, slaidi, materiāls"),
         ("<1", "frīlansera rēķins", "visas izmaksas mēnesī")], kicker="skaitļos")
d.bullets("Kur tas lūzt", [
    "Reiz tas apstājās klusi. Vispirms iestati trauksmi",
    "Izmaiņas nestrādā, kamēr nenospied publicēt",
    "Bezmaksas datubāze aizmieg pēc klusas nedēļas",
    "Tas dod regularitāti, nevis sasniedzamību"], kicker="mācījos uz savas ādas")
d.gate("KOMANDA", "Visas deviņas automatizācijas vienkāršiem vārdiem un vietas, kur sistēma lūzt.")
done(d)

# ---------------------------------------------------------------- KARUSELIS
d = DeckLV("carousel-330-lines-lv", OUT, "navy")
d.cover("Katru karuseli manā profilā zīmē **kods**.", "Bez Canva, bez dizainera, 0 € par karuseli. Arī šo, kuru tagad skaties.",
        art=art_code_to_slide, tools=["Python", "LinkedIn", ("Canva", True)])
d.stats([("3x", "lielāka iesaiste", "slaidi salīdzinājumā ar teksta ierakstiem, 2026. g. septembris"),
         ("5x", "vērtīgāka par laiku", "viena saglabāšana")], kicker="kāpēc tas vajadzīgs")
d.compare("Agrāk. Tagad.", "Agrāk", ["Stunda Canvā katram ierakstam", "Katru nedēļu cits izskats", "Grafiki uz aci"],
          "Tagad", ["Sekundes vienam karuselim", "Viens izskats vienmēr", "Stabiņi no īstiem skaitļiem"], kicker="kas mainījās")
d.flow("Kā tas strādā", [
    "Vispirms uzrakstu ierakstu",
    "Ieraksta skaitļi nonāk slaidos",
    "Skripts uzzīmē 7-8 slaidus",
    "Par daudz teksta? Slaida nav",
    "Fails tiek pievienots pats"], kicker="bez dizaina darba")
d.statement("Attēlu AI izdomā proporcijas. Kods to nevar.", kicker="kāpēc nezīmē AI",
            sub="Katrs stabiņš katrā slaidā ir īsts skaitlis no ieraksta.")
d.statement("Par garu? Teksts kļūst mazāks. Par daudz? Nekas netiek publicēts.", kicker="drošības pārbaude",
            sub="Katru rindu skripts izmēra, pirms to novieto.")
d.bullets("Ko tas nedara", [
    "Garlaicīgu skaitli interesantu nepadara",
    "Ierakstu Tavā vietā neuzraksta",
    "Īstu fotogrāfiju neaizstāj"], kicker="godīgais slaids")
d.gate("KARUSELIS", "Kā AI sagatavo slaidus, kā tos pārbaudīt un kā uzģenerēt PDF.", extra="Nevis Canva veidne.")
done(d)

# ---------------------------------------------------------------- LEADI
d = DeckLV("leads-038-lv", OUT, "navy")
d.cover("**0,38 €** par leadu. Nopirka 2 %. Gandrīz neko neiemācījos.", "Vebināra piltuve Excel kursam. Lēti leadi, dārga mācība.",
        art=lambda d, x, y, w, h: art_circles2(d, x, y, w, h, (0.38, "0,38 €", "leads"), (29, "29 €", "klients")),
        tools=["Lead forma", "E-pasts", "Excel"])
d.funnel("Visa piltuve", [
    ("reklāmas tēriņi", "1 175 €", 1.0), ("e-pasta pieraksti", "2 000+", 0.86), ("nopirka kursu par 250 €", "~2 %, ap 40", 0.66),
    ("apgrozījums", "~10 000 €", 0.54), ("atdeve", "~8x", 0.44)], kicker="excel kurss",
    note="Noapaļots uz leju. Ne visi pieraksti bija unikāli.")
d.stats([("0,38 €", "par leadu", "skaitlis, ko liek ekrānuzņēmumā"),
         ("29 €", "par klientu", "skaitlis, kas apmaksā rēķinus")], kicker="divas cenas, viena kampaņa")
d.statement("Leada cena neliecina par kvalitāti. Tā ir tikai cena.", kicker="noteikums",
            sub="Ja piekrišana neko nemaksā, atrodi cilvēkus, kuriem tā neko nenozīmē.")
d.bullets("Ko es palūdzu", [
    "Atrast cilvēkus, kas aizpilda formas",
    "Tas to izdarīja lieliski",
    "Par pirkumu es nepateicu ne vārda",
    "Dabūju tieši to, ko prasīju"], kicker="kļūda")
d.table("Ko prasīt tā vietā", ["Ko prasīt", "Piepūle", "Der?"], [
    ["Iepriekš aizpildīta forma", "nekāda", "Nē. Slazds"],
    ["Īsta atbilde", "viens teikums", "Jā"],
    ["Pieteikts zvans", "laiks kalendārā", "Jā, parasti labākais"]], kicker="labojums", widths=(0.38, 0.30, 0.32))
d.statement("Tagad vērtēju, cik maksā viena īsta saruna.", kicker="šodien", sub="Neglītāk. Lēnāk. Ekrānuzņēmumā neliksi.")
d.gate("LEADI", "Kāpēc lētie leadi nepirka un 12 jautājumu pārbaude Tavām reklāmām.")
done(d)

# ---------------------------------------------------------------- 36x pret 13x
d = DeckLV("roas-36-13-lv", OUT, "navy")
d.cover("Mans labākais ROAS: **36x**. Mana labākā kampaņa: **13x**.", "Tas nav viens un tas pats. Starpība starp tiem ir lielākā daļa no tā, ko zinu.",
        art=lambda d, x, y, w, h: art_bars2(d, x, y, w, h, [("36x", 36, "1 000 € tests"), ("13x", 13, "75 000+ € mēnesī")], hot=1))
d.stats([("36x", "1 000 € testā", "zīmolu preces ar atlaidi. Pārdevās pašas"),
         ("13x", "pie 75 000+ € mēnesī", "vairāk nekā 1 milj. € apgrozījuma. Cits darbs")], kicker="divas kampaņas")
d.table("Tā pati prasme, cits darbs", ["", "36x", "13x"], [
    ["Tēriņi", "1 000 € vienreiz", "75 000+ € mēnesī"],
    ["Pircēji", "vieglākie", "izsmelti līdz pusdienām"],
    ["Kas pelnīja", "produkts", "struktūra"]], kicker="blakus", widths=(0.30, 0.30, 0.40))
d.bullets("Pie 20 000 € dienā", [
    "Vieglākie pircēji izsmelti līdz pusdienām",
    "Reklāmas nolietojas katru dienu, ne reizi mēnesī",
    "Uzvar struktūra: budžeta sadalījums, ātra izslēgšana, pirmās 48 stundas"], kicker="lielākais konts, ko vadīju")
d.compare("Kas patiesībā mainīja rezultātu", "Mana gudrākā ideja", ["Pāris procenti", "Gadiem ticēju, ka tas ir mans darbs"],
          "Budžeta pārkārtošana", ["Desmitiem procentu", "Ne pārāk patīkami to atzīt"], kicker="tas pats konts")
d.statement("30x ekrānuzņēmums, kurā nav redzami tēriņi, rēķinās ar to, ka Tu nejautāsi.", kicker="pazīme")
d.statement("ROAS lielākoties nosaka produkts, cena, marža un tēriņi. Griestus prasme nosaka reti.", kicker="noteikums")
d.outro("Kāds ir lielākais dienas budžets, ar ko strādāji, un kas salūza pirmais?", "Saglabā šo nākamajam 30x ekrānuzņēmumam.")
done(d)

# ---------------------------------------------------------------- HOT TAKE
d = DeckLV("empty-ads-library-lv", OUT, "navy")
d.cover("Ja konkurentu nav, tā nav **brīva vieta tirgū**.", "Visbiežāk tas ir tirgus, kas Tev saka nē.",
        art=lambda d, x, y, w, h: art_two_empty(d, x, y, w, h, ("~0", "reklāmas"), ("~0", "meklējumi mēnesī"), "tirgus nav"),
        tools=["Meta ads"])
d.statement("Visi māca pretējo: ja konkurentu nav, Tu apsteidzi citus.", kicker="pārliecība",
            sub="Tas ir dārgākais teikums jebkurā biznesa plānā.")
d.stats([("~0", "reklāmas", "pelējuma likvidēšanai Latvijā"),
         ("~0", "meklējumi mēnesī", "par šo problēmu"),
         ("20 min", "lai uzzinātu", "bez maksas, no klēpjdatora")], kicker="leadu ideja, Latvija, šogad")
d.bullets("Ko parāda katra pārbaude", [
    "Reklāma griežas mēnešiem: kaut kas pārdodas",
    "Cilvēki meklē: viņi grib to atrisināt",
    "Abas pārbaudes tukšas: pircēji un pārdevēji vienisprātis",
    "Šī vienprātība ir Tava atbilde"], kicker="divas bezmaksas pārbaudes")
d.compare("Iespēja vai spriedums?", "Iespēja", ["Reklāmu nav", "Meklējumu daudz", "Reti. Vērts veltīt nedēļu"],
          "Spriedums", ["Reklāmu nav", "Meklējumu nav", "Bieži. Ej prom"], kicker="skaties uz pāri, nevis vienu skaitli")
d.statement("Metodes robeža: tā parāda pieprasījumu, kas ir šodien, nevis to, ko varētu radīt.", kicker="godīgā daļa",
            sub="Katra pilnīgi jauna kategorija šo testu neiztur. Izmanto to pakalpojumiem, nevis izgudrojumiem.")
d.outro("Kuru ideju Tu šogad atmeti, pirms tā Tev kaut ko izmaksāja?",
        "Saglabā šo nākamajai idejai, kas izskatās tukša. Pārbaudi abus skaitļus.")
done(d)

print()
for s, n, p, w in built: print(f"{s:26s} {n} slides  {os.path.getsize(p):6d} B  max {w} words/slide")
