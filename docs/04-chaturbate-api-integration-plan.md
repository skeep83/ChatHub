# Chaturbate API Integration Plan

## Available affiliate API
Base endpoint:
`https://chaturbate.com/api/public/affiliates/onlinerooms/?wm=aoQgT&client_ip=request_ip`

## Immediate goal
Add a curated live-room data module to DirtyChatHub without turning the site into a raw embed dump.

## Recommended approach
### Phase 1
- create a local fetch script for Chaturbate affiliate API
- store normalized JSON snapshots under `implementation/output/`
- build reusable curated blocks from normalized room data
- inject those blocks into a limited set of priority pages

### Priority pages
- best-adult-video-chat-sites
- best-private-cam-sites
- best-anonymous-adult-video-chat

## Why server-side first
- better control over output quality
- avoids raw spammy embed feel
- easier to style into DirtyChatHub brand
- cleaner for future filtering and curation

## Data to prioritize
- username
- room_subject
- current_show
- num_users
- num_followers
- tags
- image_url_360x270
- chat_room_url
- chat_room_url_revshare

## Risks
- do not overfetch
- avoid messy raw iframe dumps as the default UX
- keep adult live-room blocks secondary to page intent, not the whole page
