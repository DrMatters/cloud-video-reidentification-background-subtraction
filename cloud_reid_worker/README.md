## Usage
1. [Get credentials](https://googleapis.github.io/google-cloud-python/latest/core/auth.html)
2. Define environment variable ```GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json```
3. Create subscriptions
   ```
   gcloud pubsub subscriptions create --topic projects/ai-moderator/topics/new_comment new_comment_sub
   gcloud pubsub subscriptions create --topic projects/ai-moderator/topics/delete_comment delete_comment_sub
   ```
