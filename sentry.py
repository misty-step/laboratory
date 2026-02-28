import sentry_sdk
from sentry_sdk.integrations.grove import GroveIntegration

# Initialize Sentry
sentry_sdk.init(
    dsn="https://your-dsn@sentry.io/project-id",
    integrations=[GroveIntegration()],
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

# Example usage
# try:
#     # Your code here
# except Exception as e:
#     sentry_sdk.capture_exception(e)
