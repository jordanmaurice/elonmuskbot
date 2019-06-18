# elonmuskbot

This is a basic Python script used to repost tweets from Elon Musk and the Tesla Twitter account.  

The script can be easily updated to add additional twitter handles.

To use this script you will need to complete a few steps.

First, you'll need to create a webhook for your Microsoft Teams channel:

1. In Microsoft Teams, choose More options (⋯) next to the channel name and then choose Connectors.
2. Scroll through the list of Connectors to Incoming Webhook, and choose Add.
3. Enter a name for the webhook, upload an image to associate with data from the webhook, and choose Create.
4. Copy the webhook to the clipboard and save it. You'll need the webhook URL for sending information to Microsoft Teams.
5. Choose Done.

Once you have the webhook URL, you'll want to set up a twitter account for use with the twitter API.

Follow instructions from https://developer.twitter.com/en/apply-for-access.html to set up your account for use with the Twitter API.

Once you've done both setup steps, simply update the script with the values from Twitter/Microsoft, and it will automatically start posting tweets from the given screen names.