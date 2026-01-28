# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2024-01-16

### Added
- ReadTheDocs integration for automatic documentation publishing
- Sphinx documentation with RTD theme
- GitHub Actions workflow for building and publishing documentation
- Comprehensive API reference documentation
- Installation guide with troubleshooting
- Status badges in README (Tests, Publish, PyPI, Python versions, License, Documentation)
- Trusted Publisher support for PyPI (OIDC authentication)
- Manual workflow trigger for publishing

### Changed
- Updated package name to `steadfast-python` on PyPI
- Updated all documentation to reference correct package name
- Improved README with status badges
- Commented out development installation instructions (private repository)

### Fixed
- PyPI Trusted Publisher configuration for secure automated publishing
- Documentation build configuration for ReadTheDocs

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
