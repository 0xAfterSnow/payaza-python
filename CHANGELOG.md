# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-02-21

### Added
- Initial release
- `Collections` resource: initiate, verify, charge card, authorize OTP, list transactions
- `Payouts` resource: single transfer, bulk transfer, verify, resolve account, list banks
- `VirtualAccounts` resource: create static, create dynamic, get, list, deactivate
- `Transactions` resource: get, list with filters
- `Wallets` resource: balance, list
- Sandbox mode support via `sandbox=True`
- Custom exception hierarchy: `PayazaError`, `PayazaAPIError`, `PayazaAuthError`, `PayazaNetworkError`, `PayazaValidationError`
