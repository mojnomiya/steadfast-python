# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-01-15

### Added
- Initial release of Steadfast Courier Python SDK
- Order management (create single and bulk orders)
- Order tracking (by consignment ID, invoice, tracking code)
- Balance management
- Return request management
- Payment information retrieval
- Location/police station lookup
- Comprehensive error handling with specific exception types
- Full type hints throughout codebase
- Pre-commit hooks for code quality
- GitHub Actions CI/CD workflows
- Complete documentation and examples
- 169 unit tests with 80%+ coverage

### Features
- Simple API Key/Secret Key authentication
- Order creation (single and bulk up to 500 items)
- Multiple tracking methods
- Return request management
- Balance and payment tracking
- Police station lookup
- Type hints throughout
- Comprehensive error handling
- Retry logic with exponential backoff
- Credential sanitization in logs
