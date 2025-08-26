import requests
from bs4 import BeautifulSoup
from icalendar import Calendar, Event
from datetime import datetime
import pytz

def fetch_events():
    events = []

    # Example sources (placeholder, can be expanded)
    urls = {
        "KICC": "https://kicc.co.ke/events/",
        "Sarit Centre": "https://www.saritcentre.com/events/"
    }

    for venue, url in urls.items():
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Placeholder scraping logic: replace with real selectors
            for item in soup.find_all("div", class_="event-item"):
                title = item.find("h2").get_text(strip=True)
                date_text = item.find("time").get("datetime")
                date = datetime.fromisoformat(date_text)
                
                events.append({
                    "title": f"{title} - {venue}",
                    "start": date,
                    "location": venue,
                    "url": url
                })
        except Exception as e:
            print(f"Failed to fetch {venue}: {e}")

    return events

def build_calendar(events):
    cal = Calendar()
    cal.add("prodid", "-//Events Calendar//mxm.dk//")
    cal.add("version", "2.0")

    tz = pytz.timezone("Africa/Nairobi")
    for ev in events:
        event = Event()
        event.add("summary", ev["title"])
        event.add("dtstart", tz.localize(ev["start"]))
        event.add("dtend", tz.localize(ev["start"]))
        event.add("location", ev["location"])
        event.add("description", f"More info: {ev['url']}")
        cal.add_component(event)

    with open("kicc-sarit-events.ics", "wb") as f:
        f.write(cal.to_ical())

if __name__ == "__main__":
    events = fetch_events()
    build_calendar(events)
