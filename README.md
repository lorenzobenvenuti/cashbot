# cashbot

A Telegram bot to register your expenses/incomes.

## Usage

```bash
$ cashbot.py config.yaml
```

The YAML configuration file is in the form:

```yaml
telegram_token: <telegram_token>
allowed_users:
    - <user_id_1>
    - <user_id_2>
categories:
    - Life
    - House
    - Baby
    - Beer
outputs:
    - type: ifttt
      api_key: <ifttt_api_key>
      expense_event: out
      income_event: in
    - type: csv
      file: /path/to/csv
    - type: excel
      file: /path/to/excel
```

## Usage

Chat with the bot. Basic usage:

```
> /out 20 life Dinner with colleagues
< Done
> /in 500 life Salary
< Done
```

You can use just the first letters of a category

```
> /out 8.5 b Out with friends
< Too many matches: Baby,Beer
> /out 8.5 be Out with friends
< Done
```

You can list the categories:

```
> /cat
< Life
  House
  Baby
  Beer
```

## How to activate a bot

* Start a chat with the [BotFather]https://telegram.me/BotFather)
* Send the `/newbot` command
* Give a name to your robot: for instance "My Accounting Bot"
* Choose a username for your robot, like MyAccountingBot (it must end in "bot")
* Copy the API token in the YAML file

## How to discover your user id

* Start a chat with the bot you've just created (you can just click on the link the BotFather prints after you've created the bot)
* After you've sent the `/start` command, send a `Hi` message
* Launch the script `get_updates.py <telegram_token>`. Or...
* ...you can do the request yourself: `curl -X GET https://api.telegram.org/bot<token_id>/GetUpdates`. The response should be:

```json
{
    "ok": true,
    "result": [
        {
            "message": {
                "chat": {
                    "first_name": "Your first name",
                    "id": <user_id>,
                    "last_name": "Your last name",
                    "type": "private"
                },
                "date": <current_date>,
                "from": {
                    "first_name": "Your first name",
                    "id": <user_id>,
                    "last_name": "Your last name"
                },
                "message_id": 2,
                "text": "Hi"
            },
            "update_id": <update_id>
        }
    ]
}
```

## How to use the IFTTT output

* Find out your API key
  * Go to (https://ifttt.com/maker)
  * Click on the *Settings* button
  * You'll see a link in the form `https://maker.ifttt.com/use/<api_key>`
  * Copy the api key in the yaml configuration file
* Create a new applet to register incomes
  * Select Maker trigger and an event name (for instance: "incomes")
  * Select Google Drive action, *Add row to a spreasheet*.
  * Formatted row:
  `=DATEVALUE(SUBSTITUTE("{{OccurredAt}}"," at ", " ")) ||| {{Value1}} ||| ||| {{Value2}} ||| {{Value3}}`
* Create a new applet to register expensed
  * Select Maker trigger and an event name (for instance: "incomes")
  * Select Google Drive action, *Add row to a spreasheet*. Select the same spreadsheet.
  * Formatted row:
  `=DATEVALUE(SUBSTITUTE("{{OccurredAt}}"," at ", " ")) ||| ||| {{Value1}} ||| {{Value2}} ||| {{Value3}}`

## TODO

* Excel output
* Dockerfile
