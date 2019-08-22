# Specification for Scraped Components

After successfully scraping a component from some providers status site, a dict representing the component should
returned with the following keys:
- `'name'`:
    - Type: `string`
    - Description: This key should hold a string with the name of the component.
    - Required: The program will probably halt if not supplied and the users of this property do not have to check for
                its existence in order to use it.
- `'status'`:
    - Type: `enum:ComponentStatus`
    - Description: This key should hold the component status as a ComponentStatus enum. See the docs for enums under
                   structures for more information.
    - Required: The program will probably halt if not supplied and the users of this property do not have to check for
                its existence in order to use it.
- `'link'`:
    - Type: `string`
    - Description: Holds a link which is specific to either the component itself or all components of this provider.
    - Optional: Not critical to the program and users must check for its exitence before using it.

