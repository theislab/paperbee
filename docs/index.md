# paperbee

paperbee

## Mattermost Integration

Paperbee can now send formatted paper lists to a Mattermost channel.

### Configuration

Add the following section to your `config.yml` (see also `files/config_template.yml`):

```yaml
MATTERMOST:
  is_posting_on: true
  url: "your-mattermost-url"           # e.g. mattermost.example.com
  token: "your-mattermost-access-token"
  team: "your-mattermost-team-name"
  channel: "your-mattermost-channel-name"
```

Alternatively, you can set the following environment variables:
- `MATTERMOST_URL`
- `MATTERMOST_TOKEN`
- `MATTERMOST_TEAM`
- `MATTERMOST_CHANNEL`

### Sending Papers to Mattermost

1. Install the required dependency:
   ```bash
   poetry add python-mattermost-driver
   ```
2. Set your Mattermost credentials as environment variables (see above).
3. Run the script:
   ```bash
   python src/demo_mattermost.py
   ```

The script will format a sample list of papers and post it to your specified Mattermost channel.
