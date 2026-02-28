import posthog

# Initialize PostHog
posthog.api_key = "your-posthog-api-key"
posthog.host = "https://app.posthog.com"

# Example usage
# posthog.capture('user-signup', {
#     'user-id': '12345',
#     'email': 'user@example.com'
# })
