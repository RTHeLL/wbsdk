# API Reference

Автогенерируемое описание публичного API пакета `wbsdk`.

## Клиенты

### WBClient

Синхронный клиент Wildberries API.

::: wbsdk.client.WBClient
    options:
      show_source: false
      show_root_heading: true
      members:
        - request
        - request_raw
        - close

### AsyncWBClient

Асинхронный клиент Wildberries API.

::: wbsdk.async_client.AsyncWBClient
    options:
      show_source: false
      show_root_heading: true
      members:
        - request
        - request_raw
        - close

## Исключения

::: wbsdk.exceptions
    options:
      show_source: false
      show_root_heading: true
      members:
        - WBAPIError
        - WBAuthError
        - WBRateLimitError
        - WBValidationError
        - WBConflictError
        - WBNotFoundError

## Модули API (примеры)

Доступ к разделам API осуществляется через свойства клиента: `client.content`, `client.prices`, `client.marketplace` и др. Ниже — примеры модулей.

### Content API

::: wbsdk.api.content.ContentAPI
    options:
      show_source: false
      show_root_heading: true

### Marketplace API (заказы FBS)

::: wbsdk.api.marketplace.MarketplaceAPI
    options:
      show_source: false
      show_root_heading: true
