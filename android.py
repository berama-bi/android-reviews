from google_play_scraper import reviews_all, Sort
import json

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

all_rows = []

for app_name, provider, app_id in APPS:

    print(f"Lade {app_name}")

    reviews = []

    for lang in LANGUAGES:

        try:

            result = reviews_all(
                app_id,
                lang=lang,
                country="ch",
                sort=Sort.NEWEST,
                sleep_milliseconds=0
            )

            for r in result:
                r["language"] = lang

            reviews.extend(result)

        except Exception as e:

            print(
                f"Fehler {app_id} {lang}: {e}"
            )

    seen = set()

    for review in reviews:

        review_id = review.get("reviewId")

        if review_id in seen:
            continue

        seen.add(review_id)

        all_rows.append({
            "app_name": app_name,
            "provider": provider,
            "app_id": app_id,
            "language": review.get("language"),
            "review_id": review.get("reviewId"),
            "user": review.get("userName"),
            "score": review.get("score"),
            "date": str(review.get("at")),
            "content": review.get("content"),
            "thumbs_up": review.get("thumbsUpCount"),
            "app_version": review.get(
                "reviewCreatedVersion"
            ),
            "reply": review.get(
                "replyContent"
            )
        })

with open(
    "reviews.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        all_rows,
        f,
        ensure_ascii=False,
        indent=2
    )

print(
    f"reviews.json erstellt ({len(all_rows)} Reviews)"
)
