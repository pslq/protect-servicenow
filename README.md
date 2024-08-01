# Idea

This is a snip code to demonstrate how to navigate IBM Storage Protect Operations Center APIs.
Main goal is to capture alerts which clients are at risk, so an incident could be raised in Servicenow.

# DISCLAIMER

This is a DEMO/[Snip](https://en.wikipedia.org/wiki/Snippet_\(programming\)) to demonstrate a simple way to do it.
No Support at any type should be expected to be associated to it.
Use at your own risk and criteria

# Usage

If used as script, by calling *main.py*, it will connect to the Operations Center instance and capture:

- A list of all clients at risk
- A list of all open events at the Operations Center

With this information, it will connect to the target Servicenow instance and table to :

- Collect all open records
- If an event short_description is not find in the list of open records, add the record

## Caveats

If you get an warning "Generating data for a large number of columns (>20) - consider limiting fields" try to tweak how many fields are being fetch by the Servicenow API

# Parameters

All parameters are relevant only to the *main.py* script, and are collected as environment variables.

| Variable | Value   | 
|-------------- | -------------- |
| SN_USERNAME | Servicenow username |
| SN_PASSWORD | Servicenow password |
| SN_CLIENT_ID | Servicenow client id (oauth) |
| SN_SECRET | Servicenow client secret (oauth) |
| SN_TABLE | Servicenow table |
| SN_INSTANCE | Servicenow instance |
| SP_URL | Storage Protect OPS Center URL |
| SP_API_BASE | Storage Protect API Base URL |
| SP_USER | Storage Protect OPC Center user |
| SP_PW | Storage Protect OPC Center password |
| SP_VERIFY_TLS | Verify if Storage Protect OPC tls certificate is signed or not |


## Example

```
export SN_USERNAME='admin'
export SN_PASSWORD='aaaaaaaaaaaa'
export SN_CLIENT_ID='aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
export SN_SECRET='aaaaaaaaaa'
export SN_TABLE='incident'
export SN_INSTANCE='aaaaaaaaa'
export SP_URL="https://127.0.0.1:11090"
export SP_API_BASE="/oc/api"
export SP_USER='root'
export SP_PW='aaaaaaaaaaaaaaaaaaaa'
export SP_VERIFY_TLS='False'
'''
