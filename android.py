from google_play_scraper import reviews_all, Sort
import pandas as pd

# --------------------------------------------------
# APPS
# --------------------------------------------------

APPS = [
    ("mywingo", "wingo", "com.swisscom.mywingo"),
    ("wingo tv", "wingo", "com.swisscom.tv2.wingo"),

    ("myswisscom", "swisscom", "com.swisscom.myswisscom"),
    ("blue tv", "swisscom", "com.swisscom.tv2"),

    ("my yallo", "yallo", "ch.yallo.selfcare"),
    ("yallo tv", "yallo", "com.smith.production"),

    ("spusu", "spusu", "com.massresponse.spusuch"),

    ("chmobile", "chmobile", "com.chmobile.selfcareapp"),

    ("mysunrise", "sunrise", "ch.sunrise.mein.konto"),
    ("sunrise tv", "sunrise", "com.lgi.upcch"),

    ("salt", "salt", "ch.salt.my"),
    ("salt tv", "salt", "salt.tv.play"),

    ("coop mobile", "coop mobile", "com.swisscom.coopmobile"),

    ("quickline tv", "quickline", "ch.quickline.tv"),
]

LANGUAGES = ["de", "fr", "it"]

OUTPUT_FILE = r"C:\Users\taarabe2\swiss_telco_reviews.xlsx"

# --------------------------------------------------
# DOWNLOAD
# --------------------------------------------------

all_rows = []

for app_name, provider, app_id in APPS:

    print("\n" + "=" * 60)
    print(f"App: {app_name}")
    print(f"Provider: {provider}")
    print(f"ID: {app_id}")
    print("=" * 60)

    app_reviews = []

    for lang in LANGUAGES:

        print(f"Lade Reviews für Sprache: {lang}")

        try:
            result = reviews_all(
                app_id,
                lang=lang,
                country="ch",
                sort=Sort.NEWEST,
                sleep_milliseconds=0
            )

            print(f"  -> {len(result)} Reviews gefunden")

            for review in result:
                review["language"] = lang

            app_reviews.extend(result)

        except Exception as e:
            print(f"Fehler bei {lang}: {e}")

    # Duplikate entfernen
    unique_reviews = []
    seen = set()

    for review in app_reviews:

        review_id = review.get("reviewId")

        if review_id not in seen:
            seen.add(review_id)
            unique_reviews.append(review)

    print(f"Eindeutige Reviews: {len(unique_reviews)}")

    # Daten für Excel vorbereiten
    for review in unique_reviews:

        all_rows.append({
            "AppName": app_name,
            "Provider": provider,
            "AppID": app_id,
            "Language": review.get("language"),
            "ReviewID": review.get("reviewId"),
            "UserName": review.get("userName"),
            "Score": review.get("score"),
            "Date": review.get("at"),
            "Content": review.get("content"),
            "ThumbsUpCount": review.get("thumbsUpCount"),
            "AppVersion": review.get("reviewCreatedVersion"),
            "ReplyContent": review.get("replyContent"),
            "RepliedAt": review.get("repliedAt"),
        })

# --------------------------------------------------
# EXPORT
# --------------------------------------------------

df = pd.DataFrame(all_rows)

if len(df) > 0 and "Date" in df.columns:
    df = df.sort_values(by="Date", ascending=False)

df.to_excel(
    OUTPUT_FILE,
    index=False,
    engine="openpyxl"
)

print("\n" + "=" * 60)
print("FERTIG")
print(f"Anzahl Reviews: {len(df)}")
print(f"Datei gespeichert unter:")
print(OUTPUT_FILE)
print("=" * 60)