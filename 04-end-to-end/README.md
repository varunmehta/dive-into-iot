# Step 4 - Bringing it all together

> Approximate Time: 10-15 minutes

## Checklist

 * [x] IoT thing define, and certificate copied over to pi ?
 * [x] Hardware connected ?
 * [x] Test program to verify connections run ?
 * [x] AWS infrastructure deployed ?

If all the above are checked and true for you, lets go ahead and test it now.


## Switching the LED on/off using API

Get the URL of the API gateway from the notepad.

### Payload to turn on LED

```
{ "led" : "on" }
```

### Payload to turn off LED

```
{ "led" : "off" }
```

### cURL command

```
curl -XPOST \
     -H "Content-Type: application/json" \
     -d '{ "led" : "off" }' \
     https://<YOUR_URL>.execute-api.us-east-1.amazonaws.com/lab/flasher
```
