TOPIC=projects/ai-moderator/topics/new_comment
SUB=new_comment_worker_sub

# The number of seconds the system will wait for a subscriber to
# acknowledge receiving a message before re-attempting delivery.
ACK_DEADLINE=600

# The subscription will expire if it is inactive for the given period.
# Valid values are strings of the form INTEGER[UNIT],
# where UNIT is one of "s", "m", "h", and "d" for seconds, minutes, hours, and days, respectively.
# If the unit is omitted, seconds is assumed.
# This flag additionally accepts the special value "never" to indicate
# that the subscription will never expire.
EXPIRATION_PERIOD=never

# How long to retain unacknowledged messages in the subscription's backlog,
# from the moment a message is published.
# If --retain-acked-messages is true, this also configures the retention of acknowledged messages.
# The default value is 7 days, the minimum is 10 minutes, and the maximum is 7 days.
# Valid values are strings of the form INTEGER[UNIT],
# where UNIT is one of "s", "m", "h", and "d" for seconds, minutes, hours, and days, respectively.
# If the unit is omitted, seconds is assumed.
MESSAGE_RETENTION_DURATION=7d

# Whether or not to retain acknowledged messages.
# If true, messages are not expunged from the subscription's backlog
# until they fall out of the --message-retention-duration window.
RETAIN_ACKED_MESSAGES=false

createsub:
	gcloud pubsub subscriptions create $(SUB) \
		--topic=$(TOPIC) \
		--ack-deadline=$(ACK_DEADLINE) \
		--expiration-period=$(EXPIRATION_PERIOD) \
		--message-retention-duration=$(MESSAGE_RETENTION_DURATION)

deletesub:
	gcloud pubsub subscriptions delete $(SUB)

describesub:
	gcloud pubsub subscriptions describe $(SUB)

pullsub:
	gcloud pubsub subscriptions pull $(SUB)
