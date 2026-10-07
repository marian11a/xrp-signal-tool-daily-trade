CRYPTO PRICE WATCHER
====================

What it does
------------
- Uses Revolut X public market data.
- Default market: XRP/USD.
- You enter your last action (BUY or SELL) and the exact transaction price.
- If last action was BUY: red until current price is ABOVE your buy price; green when above.
- If last action was SELL: red until current price is BELOW your sell price; green when below.
- Browser favicon and tab title change red/green.
- Plays one sound when the status crosses from red to green.
- Includes a Mute / Sound on button.
- Saves the trade setup in browser localStorage, so reopening the page remembers it.

Windows quick start
-------------------
1. Install Python if needed.
2. Double-click start.bat.
3. Your browser opens http://127.0.0.1:5000

Manual start
------------
python -m pip install -r requirements.txt
python app.py

Then open:
http://127.0.0.1:5000

Example
-------
Last BUY: XRP at $1.4951
Current:  $1.4600 -> RED
Current:  $1.5000 -> GREEN + one alert sound

Last SELL: XRP at $1.4951
Current:   $1.5200 -> RED
Current:   $1.4800 -> GREEN + one alert sound

Notes
-----
Browsers restrict audio until the page has received a user interaction. Clicking Start watching satisfies that on normal browser configurations.
