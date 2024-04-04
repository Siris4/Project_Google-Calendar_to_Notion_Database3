
def sync_notion_to_calendar(notion, service, database_id, calendar_id='primary'):
    # Fetch the current state of the Notion database
    notion_pages = notion.databases.query(database_id=database_id)['results']

    for page in notion_pages:
        page_title = page['properties']['Name']['title'][0]['text']['content']
        # Assuming there's a Date property in Notion
        page_date = page['properties']['Date']['date']['start']

        # Check if this Notion page is already synced with a Google Calendar event
        # This requires a way to match Notion pages with Calendar events, possibly via an identifier or title
        event_id = get_event_id_from_notion_page(page)
        if event_id:
            # Update the existing event in Google Calendar
            update_calendar_event(service, calendar_id, event_id, page_title, page_date)
        else:
            # Create a new event in Google Calendar
            create_calendar_event(service, calendar_id, page_title, page_date)

def update_calendar_event(service, calendar_id, event_id, title, date):
    event = service.events().get(calendarId=calendar_id, eventId=event_id).execute()
    event['summary'] = title
    event['start'] = {'date': date}
    event['end'] = {'date': date}
    updated_event = service.events().update(calendarId=calendar_id, eventId=event_id, body=event).execute()

def create_calendar_event(service, calendar_id, title, date):
    event = {
        'summary': title,
        'start': {'date': date},
        'end': {'date': date},
    }
    created_event = service.events().insert(calendarId=calendar_id, body=event).execute()

