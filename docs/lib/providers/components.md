# Specification for Scraped Components

After successfully scraping a component from some providers status site, a dict representing the component should
returned with the following keys:
- `'name'`:
    - Type: `string`
    - Description: This key should hold a string with the name of the component.
- `'status'`:
    - Type: `enum:ComponentStatus`
    - Description: This key should hold the component status as a ComponentStatus enum. See the docs for enums under
                   structures for more information.

