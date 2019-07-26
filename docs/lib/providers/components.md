# Specification for Scraped Components

After successfully scraping a component from some providers status site, a dict representing the component should
returned with the following keys:
- `'name'`:
    - Type: `string`
    - Description: This key should hold a string with the name of the component.
- `'description'`:
    - Type: `string`
    - Description: This key should hold the description of the component. A summirised insight to what it denotes.
            - If it is supplied, cachet puts a little question mark besides the component name. Hovering over it reveals the description.
- `'status'`:
    - Type: `enum:ComponentStatus`
    - Description: This key should hold the component status as a ComponentStatus enum. See the docs for enums under structures for more information.
- `'provider'`:
    - Type: `string`
    - Description: Holds the name of the provider to which this component belongs in the correct format.

