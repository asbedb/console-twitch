# Console Twitch
Console Twitch is a Python project that brings Twitch chat directly into your console.

# Installation

First, ensure you have the necessary dependencies installed. Open your terminal or command prompt and run:

`pip install dotenv requests urllib3 websockets`

Next, you need to set up your Twitch application and configure your `.env` file.

## Twitch Developer App
1. Go to the [Twitch Developer Console](https://dev.twitch.tv/console) and register a new application.
2. When creating the application, set the OAuth Redirect URLs to `https://localhost/`.
3. Once your application is created, navigate to its settings and copy your `Client ID` and `Client Secret`.

## Configure your `.env` file
In the root directory of your project, create a file named .env and add the following information, replacing the <placeholders> with your actual values removing `<>` characters ():

```
TWITCH_CLIENT_ID=<YOUR CLIENT ID>
TWITCH_CLIENT_SECRET=<YOUR CLIENT SECRET>
TWITCH_REDIRECT_URI=https://localhost/
TWITCH_USERNAME=<YOUR TWITCH USERNAME>
TWITCH_CHANNELS_TO_JOIN= < channel1,channel2,channel3 >
```
Note: If you don't specify any channels in `TWITCH_CHANNELS_TO_JOIN`, the monitor will default to `xqc`. Separate multiple channels with a comma (e.g., ludwig,pokimane).

## Authentication
1. Run the authentication script
`py auth.py`
2. A link will be printed to your console. Open this link in your web browser.
3. You will be redirected to a local page with a code in the address bar (after `code=`). Copy this entire code.
4. Paste the copied code back into your console when prompted.

The authentication script will then update your .env file with your authentication token.

# Running the Chat Monitor
Once the authentication is complete, you can start the chat monitor by running:
`py monitor.py`

You should now see Twitch chat for the specified channels appearing in your console!

To stop the program, you can use the `Ctrl+C` command in your terminal.

