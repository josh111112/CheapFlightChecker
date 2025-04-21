from serpapi import GoogleSearch
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
from config import *


for arrival_id in ARRIVAL_ID:
    params = {
        "api_key": SERP_API_KEY,
        "engine": "google_flights",
        "hl": "en",
        "gl": "us",
        "departure_id": DEPARTURE_ID,
        "arrival_id": arrival_id,
        "outbound_date": OUTBOUND_DATE,
        "return_date": RETURN_DATE,
        "currency": CURRENCY,
        "sort_by": "2",
        "type": "1",
        "deep_search": "true"
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    lowest_price = float('inf')
    lowest_price_flight = None

    for flight in results.get('other_flights', []):
        if flight.get('price', float('inf')) < lowest_price:
            lowest_price = flight.get('price')
            lowest_price_flight = flight

    price_insights = results.get('price_insights', {})
    low_range = price_insights.get('typical_price_range', [])[0]

    def create_flight_email(flight_data):
        message = MIMEMultipart()
        message['From'] = SMTP_USERNAME
        message['To'] = EMAIL_TO
        message['Subject'] = f'Low Price Alert: ${flight_data["price"]} to {flight_data["flights"][-1]["arrival_airport"]["id"]}'
        
        html_content = f"""
        <html>
        <body>
            <h2>Flight Deal Alert!</h2>
            <p><strong>Price:</strong> ${flight_data["price"]} (Round Trip)</p>
            <p><strong>Total Duration:</strong> {flight_data["total_duration"]//60}h {flight_data["total_duration"]%60}m</p>
            
            <h3>Outbound Journey:</h3>
            <table border="1" cellpadding="5">
                <tr>
                    <th>Date</th>
                    <th>From</th>
                    <th>Departure</th>
                    <th>To</th>
                    <th>Arrival</th>
                    <th>Airline</th>
                    <th>Flight</th>
                </tr>
        """
        
        # Add each flight segment
        for flight in flight_data["flights"]:
            # Parse dates
            dep_datetime = datetime.datetime.strptime(flight["departure_airport"]["time"], "%Y-%m-%d %H:%M")
            arr_datetime = datetime.datetime.strptime(flight["arrival_airport"]["time"], "%Y-%m-%d %H:%M")
            
            # Format for display
            dep_date = dep_datetime.strftime("%b %d")
            dep_time = dep_datetime.strftime("%I:%M %p")
            arr_date = arr_datetime.strftime("%b %d")
            arr_time = arr_datetime.strftime("%I:%M %p")
            
            html_content += f"""
                <tr>
                    <td>{dep_date}</td>
                    <td>{flight["departure_airport"]["id"]}</td>
                    <td>{dep_time}</td>
                    <td>{flight["arrival_airport"]["id"]}</td>
                    <td>{arr_time}</td>
                    <td>{flight["airline"]}</td>
                    <td>{flight["flight_number"]}</td>
                </tr>
            """
        
        html_content += """
            </table>
            <p>Book this deal before prices increase!</p>
        </body>
        </html>
        """
        
        message.attach(MIMEText(html_content, 'html'))
        
        return message

    # If the price is lower than the typical low range, send an email alert
    if lowest_price < low_range and lowest_price_flight:
        message = create_flight_email(lowest_price_flight)
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)

        server.sendmail(SMTP_USERNAME, EMAIL_TO, message.as_string())
        server.quit()
        
        print("Email alert sent successfully!")
