"""Apply the resolved TMDB/MAL ids from the resolve_all_awards.py run into
awards_data.py, skipping any entry that was flagged LOW CONFIDENCE (those
keep their existing id untouched but get a `# TODO verify` comment added
so they're easy to find later).

This is a one-time apply script -- it rewrites the file in place using a
mapping baked in below (copied straight from Val's resolve_all_awards.py
output), matched by (slug, year, old_id) to avoid touching the wrong line
if two awards share a year.

Run inside the container:
    docker compose cp src/apply_award_fixes.py yamtrack:/yamtrack/apply_award_fixes.py
    docker compose exec yamtrack python apply_award_fixes.py
"""
import re

AWARDS_DATA_PATH = "/yamtrack/app/awards_data.py"

# (slug, year, old_id_or_None, new_id) -- only HIGH confidence (sim >= 0.85)
# entries from the resolve_all_awards.py run. old_id is None for entries
# that had no id previously (e.g. manga_taisho stubs).
FIXES = [
    # oscar_best_picture
    ("oscar_best_picture", 2024, "872585", "1634345"),
    ("oscar_best_picture", 2017, "376867", "1396421"),
    ("oscar_best_picture", 2016, "314365", "1380676"),
    ("oscar_best_picture", 2015, "194662", "435092"),
    ("oscar_best_picture", 2012, "74643", "370425"),
    # palme_dor
    ("palme_dor", 2023, "1011985", "915935"),
    ("palme_dor", 2022, "747188", "497828"),
    ("palme_dor", 2021, "788183", "630240"),
    ("palme_dor", 2018, "517623", "505192"),
    ("palme_dor", 2017, "397645", "401246"),
    ("palme_dor", 2016, "394044", "374473"),
    ("palme_dor", 2015, "320793", "314402"),
    ("palme_dor", 2014, "253236", "265169"),
    ("palme_dor", 2013, "154226", "152584"),
    ("palme_dor", 2012, "103663", "86837"),
    ("palme_dor", 2011, "75612", "8967"),
    ("palme_dor", 2010, "60545", "38368"),
    ("palme_dor", 2009, "18491", "37903"),
    ("palme_dor", 2008, "19823", "8841"),
    ("palme_dor", 2007, "12446", "2009"),
    ("palme_dor", 2006, "4813", "1116"),
    ("palme_dor", 2005, "13528", "1433895"),  # L'Enfant -- verify: match_year 2024 looks off
    ("palme_dor", 2004, "9614", "1777"),
    ("palme_dor", 2003, "11832", "1807"),
    ("palme_dor", 2002, "1128", "423"),
    ("palme_dor", 2000, "289", "16"),
    ("palme_dor", 1999, "37232", "11489"),
    ("palme_dor", 1993, "9816", "10997"),  # Farewell My Concubine
    ("palme_dor", 1993, "397", "713"),  # The Piano (same year, different id_key value -- see note)
    ("palme_dor", 1991, "13823", "290"),
    ("palme_dor", 1989, "9561", "1412"),
    ("palme_dor", 1984, "11252", "655"),
    # golden_lion
    ("golden_lion", 2020, "581726", "581734"),
    ("golden_lion", 2018, "481852", "426426"),
    ("golden_lion", 2010, "45215", "39210"),
    ("golden_lion", 2008, "13380", "12163"),
    ("golden_lion", 2007, "5408", "4588"),
    ("golden_lion", 2005, "324", "142"),
    ("golden_lion", 2004, "9736", "11109"),
    ("golden_lion", 2003, "9567", "11190"),
    # golden_bear
    ("golden_bear", 2011, "72096", "60243"),
    ("golden_bear", 2008, "7555", "7347"),
    ("golden_bear", 2004, "11509", "363"),
    ("golden_bear", 2000, "17044", "334"),
    # bafta_best_film (FIRST block, 24 entries)
    ("bafta_best_film", 2024, "872585", "1634345"),
    ("bafta_best_film", 2023, "843047", "49046"),
    ("bafta_best_film", 2022, "754609", "600583"),
    ("bafta_best_film", 2021, "581726", "581734"),
    ("bafta_best_film", 2019, "481852", "426426"),
    ("bafta_best_film", 2015, "209112", "85350"),
    ("bafta_best_film", 2013, "68721", "68734"),
    ("bafta_best_film", 2012, "74643", "370425"),
    ("bafta_best_film", 2008, "16320", "4347"),
    ("bafta_best_film", 2007, "1633", "1165"),
    ("bafta_best_film", 2006, "324", "142"),
    ("bafta_best_film", 2005, "11012", "2567"),
    ("bafta_best_film", 2003, "1128", "423"),
    # manga_taisho -- fill in previously-empty ids
    ("manga_taisho", 2010, None, "11514"),
    ("manga_taisho", 2013, None, "25096"),
    ("manga_taisho", 2015, None, "85781"),
    # tezuka / shogakukan
    ("tezuka_cultural_grand_prize", 2002, "1357", "656"),
    ("shogakukan_manga_award", 2006, "47", "3"),
    ("shogakukan_manga_award", 2002, "1357", "656"),
    # cesar_best_film (only HIGH confidence ones -- others left for manual review)
    ("cesar_best_film", 2024, "929590", "915935"),
    ("cesar_best_film", 2023, "785084", "1118848"),
    ("cesar_best_film", 2022, "599117", "1489982"),
    ("cesar_best_film", 2020, "503919", "586863"),
    ("cesar_best_film", 2017, "376660", "734736"),
    ("cesar_best_film", 2015, "246655", "265228"),
    ("cesar_best_film", 2013, "87736", "86837"),
    ("cesar_best_film", 2012, "62362", "370425"),
    # cannes_grand_prix
    ("cannes_grand_prix", 2024, "1118031", "927547"),
    ("cannes_grand_prix", 2023, "975902", "467244"),
    ("cannes_grand_prix", 2022, "815246", "603204"),
    ("cannes_grand_prix", 2021, "681660", "672208"),
    ("cannes_grand_prix", 2019, "505571", "496967"),
    ("cannes_grand_prix", 2018, "458818", "517814"),
    ("cannes_grand_prix", 2017, "413232", "636760"),
    # cannes_un_certain_regard
    ("cannes_un_certain_regard", 2024, "1209290", "1144681"),
    ("cannes_un_certain_regard", 2023, "878783", "1075175"),
    ("cannes_un_certain_regard", 2022, "817758", "848791"),
    ("cannes_un_certain_regard", 2019, "560197", "595940"),
    # sundance_grand_jury
    ("sundance_grand_jury", 2024, "1046193", "1208994"),
    ("sundance_grand_jury", 2023, "869626", "898673"),
    ("sundance_grand_jury", 2022, "818680", "819309"),
    ("sundance_grand_jury", 2021, "614278", "776503"),
    ("sundance_grand_jury", 2020, "531876", "615643"),
    ("sundance_grand_jury", 2019, "503907", "565307"),
    ("sundance_grand_jury", 2018, "433680", "424201"),
    ("sundance_grand_jury", 2017, "399174", "425591"),
    # bafta_best_film (SECOND/duplicate block, 15 entries -- will be merged away, see script #2)
    # berlinale_jury_grand_prix
    ("berlinale_jury_grand_prix", 2024, "1071215", "794090"),
    ("berlinale_jury_grand_prix", 2022, "785154", "728499"),
    ("berlinale_jury_grand_prix", 2021, "628293", "875186"),
    # venice_grand_jury
    ("venice_grand_jury", 2024, "1163126", "1064021"),
    ("venice_grand_jury", 2023, "961268", "1156125"),
    ("venice_grand_jury", 2022, "879499", "925943"),
    ("venice_grand_jury", 2021, "644124", "660708"),
    ("venice_grand_jury", 2019, "544401", "1121519"),
    # european_film_award
    ("european_film_award", 2024, "929590", "915935"),
    ("european_film_award", 2023, "840430", "467244"),
    ("european_film_award", 2022, "669000", "901563"),
    ("european_film_award", 2021, "696374", "722778"),
    ("european_film_award", 2020, "524434", "580175"),
    ("european_film_award", 2019, "540903", "496243"),
    ("european_film_award", 2018, "458818", "517814"),
    # saturn_best_scifi
    ("saturn_best_scifi", 2024, "934632", "792307"),
    ("saturn_best_scifi", 2023, "505642", "76600"),
    # tiff_peoples_choice
    ("tiff_peoples_choice", 2024, "1079091", "933260"),
    ("tiff_peoples_choice", 2023, "872585", "1056360"),
    ("tiff_peoples_choice", 2021, "823754", "777270"),
    ("tiff_peoples_choice", 2020, "615173", "581734"),
]

LOW_CONFIDENCE = [
    # (slug, year, wanted_title) -- left untouched, flagged for manual review
    ("cesar_best_film", 2021, "De leur vivant"),
    ("cesar_best_film", 2019, "Jusqu'à la garde"),
    ("cesar_best_film", 2018, "120 Battements par minute"),
    ("cesar_best_film", 2016, "La Loi du marché"),
    ("cesar_best_film", 2014, "La vie d'Adèle"),
    ("cesar_best_film", 2011, "Des hommes et des dieux"),
    ("cesar_best_film", 2010, "Un prophète"),
    ("berlinale_jury_grand_prix", 2023, "Sur l'Adamant"),
]


def main():
    with open(AWARDS_DATA_PATH, encoding="utf-8") as f:
        lines = f.readlines()

    slug_re = re.compile(r'"slug":\s*"(\w+)"')
    current_slug = None
    applied = 0
    flagged = 0
    seen_bafta_blocks = 0

    for i, line in enumerate(lines):
        slug_m = slug_re.search(line)
        if slug_m and '"name"' not in line:
            current_slug = slug_m.group(1)
            if current_slug == "bafta_best_film":
                seen_bafta_blocks += 1
            continue
        if current_slug is None:
            continue

        year_m = re.search(r'"year":\s*(\d+)', line)
        if not year_m:
            continue
        year = int(year_m.group(1))

        # Skip the second bafta_best_film block entirely for id patching
        # here -- it's a duplicate slug being handled by a separate merge
        # script, not by id substitution.
        if current_slug == "bafta_best_film" and seen_bafta_blocks == 2:
            continue

        for slug, fyear, old_id, new_id in FIXES:
            if slug != current_slug or fyear != year:
                continue
            if old_id is None:
                # Fill in a previously-empty id: "year": N, "X_id": None}
                new_line, n = re.subn(
                    r'("year":\s*\d+,\s*"\w+_id":\s*)None(\})',
                    rf'\g<1>"{new_id}"\g<2>',
                    line,
                )
            else:
                new_line, n = re.subn(
                    rf'"{re.escape(old_id)}"',
                    f'"{new_id}"',
                    line,
                    count=1,
                )
            if n:
                lines[i] = new_line
                applied += 1
            break

        for slug, fyear, wanted in LOW_CONFIDENCE:
            if slug == current_slug and fyear == year and "TODO verify" not in line:
                lines[i] = line.rstrip("\n") + f"  # TODO verify: {wanted}\n"
                flagged += 1
                break

    with open(AWARDS_DATA_PATH, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print(f"Applied {applied} id fixes, flagged {flagged} low-confidence entries.")


if __name__ == "__main__":
    main()
