from os import getenv

project_id = getenv('PROJECT_ID', 'ai-moderator')
sub_name = getenv('SUB_NAME', 'new_comment_worker_sub')
topic_name = getenv('TOPIC_NAME', 'new_comment')
bucket_name = getenv('BUCKET_NAME', 'deep-moderator-base')
dir_prefix = getenv('DIR_PREFIX', 'ai-moderator-worker__')
remote_base_path = getenv('REMOTE_BASE_PATH', '/')
