# livisi

# Asynchronous library to communicate with LIVISI Smart Home Controller
Requires Python 3.10+ (might work with versions down to 3.8 but I never tested it) and uses asyncio and aiohttp.

This library started as a fork of the unmaintained aiolivisi lib and was developed inside the [unofficial livisi integration for Home Assistant](https://github.com/planbnet/livisi_unofficial)

The versions starting with `0.0.` are still compatible to the old aiolivisi code, while `1.0.0` will introduce lots of breaking changes besides support for more devices and improved connection stability and error handling.
