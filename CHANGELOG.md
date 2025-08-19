# Changelog

## 1.2.0

### Changed

- Update documentation with Mattermost integration
- Fixed mattermost integration: added missing pieces to posting functions

## 1.1.1

### Added

- Test with empty papers list in `tests/test_telegrm.py`

### Changed

- Improve handling of papers list when it is empty

## 1.1.0

### Added
 
- Mattermost integration: format and send daily paper digests to Mattermost channels.
- New `MattermostPaperPublisher` class for formatting and posting messages.
- Demo script and unit tests for Mattermost integration.

### Changed

- Updated documentation and config template for Mattermost support. 