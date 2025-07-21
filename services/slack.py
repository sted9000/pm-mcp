import os
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Load environment variables from .env file
load_dotenv()


class SlackService:
    def __init__(self, token: Optional[str] = None):
        """
        Initialize Slack service with token.
        Token can be passed directly or set as SLACK_BOT_TOKEN environment variable.
        """
        self.token = token or os.environ.get('SLACK_BOT_TOKEN')
        if not self.token:
            raise ValueError("Slack token must be provided or set as SLACK_BOT_TOKEN environment variable")
        
        self.client = WebClient(token=self.token)
    
    def get_conversation_history(
        self, 
        channel_id: str,
        limit: int = 100,
        oldest: Optional[str] = None,
        latest: Optional[str] = None,
        inclusive: bool = True,
        cursor: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Fetch conversation history from a Slack channel.
        
        Args:
            channel_id: The ID of the channel/conversation
            limit: Number of messages to return (max 1000)
            oldest: Only messages after this Unix timestamp
            latest: Only messages before this Unix timestamp
            inclusive: Include messages with oldest or latest timestamps
            cursor: Pagination cursor
            
        Returns:
            Dict containing messages and metadata
        """
        try:
            result = self.client.conversations_history(
                channel=channel_id,
                limit=limit,
                oldest=oldest,
                latest=latest,
                inclusive=inclusive,
                cursor=cursor
            )
            return result.data
        except SlackApiError as e:
            print(f"Error fetching conversation history: {e}")
            raise
    
    def get_all_messages(self, channel_id: str, oldest: Optional[str] = None, latest: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Fetch all messages from a channel, handling pagination automatically.
        
        Args:
            channel_id: The ID of the channel/conversation
            oldest: Only fetch messages after this Unix timestamp
            latest: Only fetch messages before this Unix timestamp
            
        Returns:
            List of all messages in the channel
        """
        messages = []
        cursor = None

        # Turn datetime strings into Unix timestamps
        if oldest:
            print(f"Oldest: {oldest}")
            oldest = int(oldest.timestamp())
            print(f"Oldest: {oldest}")
        if latest:
            print(f"Latest: {latest}")
            latest = int(latest.timestamp())
            print(f"Latest: {latest}")

        
        while True:
            response = self.get_conversation_history(
                channel_id=channel_id,
                limit=1000,
                oldest=oldest,
                latest=latest,
                cursor=cursor
            )
            
            messages.extend(response.get('messages', []))
            
            if not response.get('has_more', False):
                break
                
            cursor = response.get('response_metadata', {}).get('next_cursor')

            print(f"Found {len(messages)} total messages in channel")
            print(messages)
            
        return messages


if __name__ == "__main__":
    # Example usage
    slack = SlackService()
    
    # Replace with your channel ID
    channel_id = "C1234567890"
    
    try:
        # Get recent messages
        history = slack.get_conversation_history(channel_id, limit=10)
        print(f"Found {len(history['messages'])} recent messages")
        
        # Get all messages
        all_messages = slack.get_all_messages(channel_id)
        print(f"Found {len(all_messages)} total messages in channel")
        
    except Exception as e:
        print(f"Error: {e}")